// Adapted locally from Cerelog V1_special_differential_fw, upstream commit
// af1a56e0127e71606afdc7e7ddf0ca831715e09c. This is NOT the unmodified vendor build.
// CH1-4 and CH6: differential EMG gain 24; CH5: divided ALS gain 1.
// CH7-8: differential EOG gain 24. All eight channels enabled; off-body bench first.
// 1000 SPS; Cerelog BIAS amplifier off. Use the accompanying host reader.

#include <Arduino.h>
#include <SPI.h>

// #define DEBUG_ENABLED // Uncomment when debugging ONLY - will corrupt data otherwise

#ifdef DEBUG_ENABLED
#define DEBUG_PRINT(...) Serial.print(__VA_ARGS__) // accepts variable arguments
#define DEBUG_PRINTLN(...) Serial.println(__VA_ARGS__)
#else
#define DEBUG_PRINT(...)
#define DEBUG_PRINTLN(...)
#endif

// --- Packet/Protocol Global Variables ---
const uint8_t ADS1299_NUM_STATUS_BYTES = 3;
const uint8_t ADS1299_NUM_CHANNELS = 8;
const uint8_t ADS1299_BYTES_PER_CHANNEL = 3;
const uint8_t ADS1299_TOTAL_DATA_BYTES = ADS1299_NUM_STATUS_BYTES + (ADS1299_NUM_CHANNELS * ADS1299_BYTES_PER_CHANNEL);
const uint8_t PACKET_TIMESTAMP_BYTES = 4;
const uint8_t PACKET_START_MARKER_BYTES = 2;
const uint8_t PACKET_END_MARKER_BYTES = 2;
const uint8_t PACKET_LENGTH_FIELD_BYTES = 1;
const uint8_t PACKET_CHECKSUM_BYTES = 1;
const uint8_t PACKET_MSG_LENGTH = PACKET_TIMESTAMP_BYTES + ADS1299_TOTAL_DATA_BYTES;
const uint8_t PACKET_TOTAL_SIZE = PACKET_START_MARKER_BYTES + PACKET_LENGTH_FIELD_BYTES + PACKET_MSG_LENGTH + PACKET_CHECKSUM_BYTES + PACKET_END_MARKER_BYTES;
const uint8_t PACKET_IDX_START_MARKER = 0;
const uint8_t PACKET_IDX_LENGTH = PACKET_IDX_START_MARKER + PACKET_START_MARKER_BYTES;
const uint8_t PACKET_IDX_TIMESTAMP = PACKET_IDX_LENGTH + PACKET_LENGTH_FIELD_BYTES;
const uint8_t PACKET_IDX_ADS1299_DATA = PACKET_IDX_TIMESTAMP + PACKET_TIMESTAMP_BYTES;
const uint8_t PACKET_IDX_CHECKSUM = PACKET_IDX_ADS1299_DATA + ADS1299_TOTAL_DATA_BYTES;
const uint8_t PACKET_IDX_END_MARKER = PACKET_IDX_CHECKSUM + PACKET_CHECKSUM_BYTES;

// --- Pin Mapping ---
static const uint8_t pin_MOSI_NUM = 23;
static const uint8_t pin_CS_NUM = 5;
static const uint8_t pin_MISO_NUM = 19;
static const uint8_t pin_SCK_NUM = 18;
static const uint8_t pin_PWDN_NUM = 13;
static const uint8_t pin_RST_NUM = 12;
static const uint8_t pin_START_NUM = 14;
static const uint8_t pin_DRDY_NUM = 27;
static const uint8_t pin_LED_DEBUG = 17;

// --- SPI instance ---
SPIClass *vspi = NULL;

// Query Timing Setup
unsigned long _last_query_time = 0;
static const int SPI_FREQ = 4000000;
static const int SAMPLE_FREQ = 1000;
static const float SAMPLE_PRD_us = (1.0 / SAMPLE_FREQ) * 1000000;

// --- ADS1299 State Management ---
int _ADS1299_MODE = -2;
int ADS1299_MODE_SDATAC = 1;
int ADS1299_MODE_RDATAC = 2;
int _ADS1299_PREV_CMD = -1;
int _CMD_ADC_WREG = 3;
int _CMD_ADC_RREG = 4;
int _CMD_ADC_SDATAC = 17;
int _CMD_ADC_RDATAC = 16;
int _CMD_ADC_START = 8;

// --- Interrupt Flag & Timestamp ---
volatile bool dataReady = false;
unsigned long _unix_timestamp_reference = 0;
unsigned long _millis_reference = 0;
bool _timestamp_initialized = false;

// --- Function Prototypes ---
void ADS1299_WREG(uint8_t regAdd, uint8_t *values, uint8_t numRegs);
void ADS1299_RREG(uint8_t regAdd, uint8_t *buffer, uint8_t numRegs);
void ADS1299_SETUP(void);
void ADS1299_SDATAC(void);
void ADS1299_RDATAC(void);
void ADS1299_START(void);
byte SPI_SendByte(byte data_byte, bool cont);
void read_ADS1299_data(byte *buffer);
void IRAM_ATTR onDRDYFalling(void);
void print_all_ADS1299_registers_from_setup(void);
uint32_t get_baud_rate_from_config(uint8_t config_val);

// --- Register Setup ---
typedef struct Deez { int add; int reg_val; } regVal_pair;
static const regVal_pair ADS1299_REGISTER_LS[] = {
  {0x01, 0b10110100}, {0x02, 0b11010000}, {0x03, 0b11101000}, {0x04, 0},
  {0x05, 0b01100000}, {0x06, 0b01100000}, {0x07, 0b01100000}, {0x08, 0b01100000},
  {0x09, 0b00000000}, {0x0A, 0b01100000}, {0x0B, 0b01100000}, {0x0C, 0b01100000},
  {0x0D, 0b00000000}, {0x0E, 0b00000000}, {0x0F, 0}, {0x10, 0}, {0x11, 0},
  {0x15, 0b00000000}, {0x16, 0}, {0x17, 0}
};
const int size_reg_ls = sizeof(ADS1299_REGISTER_LS) / sizeof(ADS1299_REGISTER_LS[0]);
uint8_t register_readback[24] = {0};
bool register_readback_ok = false;

// --- Host control, at 9600 baud before streaming ---
// Retains the 12-byte Cerelog envelope; type 0x03 queries configuration.
// Only 460800/921600 streaming is accepted: 37 bytes * 1000 Hz needs 370 kbit/s.
uint8_t handshake[12] = {0};
uint8_t handshake_count = 0;

void report_configuration() {
  Serial.print("CERELOG_CFG {\"firmware\":\"CERELOG_V1_EMG5_EOG2_ALS1_1K_V1\",");
  Serial.print("\"rate_hz\":1000,\"stream_baud\":460800,\"gains\":[24,24,24,24,1,24,24,24],");
  Serial.print("\"active_channels\":[1,2,3,4,5,6,7,8],\"bias_driver\":false,\"readback_ok\":");
  Serial.print(register_readback_ok ? "true" : "false");
  Serial.print(",\"registers\":[");
  for (uint8_t i = 0; i < sizeof(register_readback); i++) {
    if (i) Serial.print(',');
    Serial.print(register_readback[i]);
  }
  Serial.println("]}");
}

bool waitForTimestamp() {
  while (Serial.available() > 0) {
    uint8_t value = Serial.read();
    if (handshake_count < sizeof(handshake)) {
      handshake[handshake_count++] = value;
    } else {
      memmove(handshake, handshake + 1, sizeof(handshake) - 1);
      handshake[sizeof(handshake) - 1] = value;
    }
    if (handshake_count != sizeof(handshake)) continue;
    if (handshake[0] != 0xAA || handshake[1] != 0xBB ||
        handshake[10] != 0xCC || handshake[11] != 0xDD) continue;
    uint8_t checksum = 0;
    for (uint8_t i = 2; i <= 8; i++) checksum += handshake[i];
    if (checksum != handshake[9]) continue;
    const uint8_t message_type = handshake[2];
    handshake_count = 0;
    if (message_type == 0x03) {
      report_configuration();
      continue;
    }
    if (message_type != 0x02 || handshake[7] != 0x01) continue;
    uint32_t new_baud_rate = get_baud_rate_from_config(handshake[8]);
    if (new_baud_rate < 460800) {
      Serial.println("CERELOG_ERROR streaming_requires_at_least_460800_baud");
      continue;
    }
    if (!register_readback_ok) {
      Serial.println("CERELOG_ERROR register_readback_failed");
      continue;
    }
    _unix_timestamp_reference =
        (uint32_t)handshake[3] << 24 | (uint32_t)handshake[4] << 16 |
        (uint32_t)handshake[5] << 8 | (uint32_t)handshake[6];
    Serial.flush();
    delay(100);
    Serial.begin(new_baud_rate);
    delay(100);
    _millis_reference = millis();
    _timestamp_initialized = true;
    return true;
  }
  return false;
}

void IRAM_ATTR onDRDYFalling(void) { dataReady = true; }

byte SPI_SendByte(byte data_byte, bool cont) {
  if (!cont) { digitalWrite(pin_CS_NUM, LOW); delayMicroseconds(1); }
  byte received = vspi->transfer(data_byte);
  if (!cont) { delayMicroseconds(1); digitalWrite(pin_CS_NUM, HIGH); }
  return received;
}

void ADS1299_WREG(uint8_t regAdd, uint8_t *values, uint8_t numRegs) {
  if (_ADS1299_MODE != ADS1299_MODE_SDATAC) ADS1299_SDATAC();
  digitalWrite(pin_CS_NUM, LOW);
  delayMicroseconds(1); // FIX #1: Enforce CS setup time
  SPI_SendByte(0b01000000 | regAdd, true);
  SPI_SendByte(numRegs - 1, true);
  for (uint8_t i = 0; i < numRegs; i++) SPI_SendByte(values[i], true);
  delayMicroseconds(1); // FIX #1: Enforce CS hold time
  digitalWrite(pin_CS_NUM, HIGH);
  _ADS1299_PREV_CMD = _CMD_ADC_WREG;
}

void ADS1299_RREG(uint8_t regAdd, uint8_t *buffer, uint8_t numRegs) {
  if (_ADS1299_MODE != ADS1299_MODE_SDATAC) ADS1299_SDATAC();
  digitalWrite(pin_CS_NUM, LOW);
  delayMicroseconds(1); // FIX #1: Enforce CS setup time
  SPI_SendByte(0b00100000 | regAdd, true);
  SPI_SendByte(numRegs - 1, true);
  for (uint8_t i = 0; i < numRegs; i++) buffer[i] = SPI_SendByte(0x00, true);
  delayMicroseconds(1); // FIX #1: Enforce CS hold time
  digitalWrite(pin_CS_NUM, HIGH);
  _ADS1299_PREV_CMD = _CMD_ADC_RREG;
}

void ADS1299_SDATAC(void) {
  digitalWrite(pin_CS_NUM, LOW);
  delayMicroseconds(1); // FIX #1
  SPI_SendByte(_CMD_ADC_SDATAC, true);
  delayMicroseconds(1); // FIX #1
  digitalWrite(pin_CS_NUM, HIGH);
  _ADS1299_MODE = ADS1299_MODE_SDATAC;
  _ADS1299_PREV_CMD = _CMD_ADC_SDATAC;
}

void ADS1299_RDATAC(void) {
  digitalWrite(pin_CS_NUM, LOW);
  delayMicroseconds(1); // FIX #1
  SPI_SendByte(_CMD_ADC_RDATAC, true);
  delayMicroseconds(1); // FIX #1
  digitalWrite(pin_CS_NUM, HIGH);
  _ADS1299_MODE = ADS1299_MODE_RDATAC;
  _ADS1299_PREV_CMD = _CMD_ADC_RDATAC;
}

void ADS1299_START(void) {
  digitalWrite(pin_CS_NUM, LOW);
  delayMicroseconds(1); // FIX #1
  SPI_SendByte(_CMD_ADC_START, true);
  delayMicroseconds(1); // FIX #1
  digitalWrite(pin_CS_NUM, HIGH);
  _ADS1299_PREV_CMD = _CMD_ADC_START;
}

void ADS1299_SETUP(void) {
  digitalWrite(pin_PWDN_NUM, LOW);
  digitalWrite(pin_RST_NUM, LOW);
  delay(100);
  digitalWrite(pin_PWDN_NUM, HIGH);
  digitalWrite(pin_RST_NUM, HIGH);
  delay(1000);
  ADS1299_SDATAC();
  uint8_t refbuf[] = {0b11101000};
  ADS1299_WREG(0x03, refbuf, 1);
  delay(10);
  uint8_t value[1];
  uint8_t i = 0;
  while (i < size_reg_ls) {
      const regVal_pair temp = ADS1299_REGISTER_LS[i];
      if (temp.add == -2) { i++; continue; }
      value[0] = {(uint8_t)temp.reg_val};
      ADS1299_WREG(temp.add, value, 1);
      delayMicroseconds(10);
      i++;
  }
}

void read_ADS1299_data(byte *buffer) {
  digitalWrite(pin_CS_NUM, LOW);
  delayMicroseconds(1); // FIX #1
  for (int i = 0; i < ADS1299_TOTAL_DATA_BYTES; i++) {
      buffer[i] = SPI_SendByte(0x00, true);
  }
  delayMicroseconds(1); // FIX #1
  digitalWrite(pin_CS_NUM, HIGH);
}

void print_all_ADS1299_registers_from_setup(void) {
  DEBUG_PRINTLN("---- ADS1299 Register Dump ----");
  for (int i = 0; i < size_reg_ls; i++) {
      int reg_addr = ADS1299_REGISTER_LS[i].add;
      if (reg_addr == -2) { i++; continue; }
      uint8_t reg_val[1];
      ADS1299_RREG((uint8_t)reg_addr, reg_val, 1);
      DEBUG_PRINT("Register 0x");
      if (reg_addr < 0x10) DEBUG_PRINT("0");
      DEBUG_PRINT(reg_addr, HEX);
      DEBUG_PRINT(" : ");
      uint16_t val_for_print = 0x100 | reg_val[0];
      DEBUG_PRINTLN(val_for_print, BIN);
      delayMicroseconds(2);
  }
  DEBUG_PRINTLN("-------------------------------");
}

uint32_t get_baud_rate_from_config(uint8_t config_val) {
  switch (config_val) {
      case 0x00: return 9600;   case 0x01: return 19200;  case 0x02: return 38400;
      case 0x03: return 57600;  case 0x04: return 115200; case 0x05: return 230400;
      case 0x06: return 460800; case 0x07: return 921600; default: return 0;
  }
}

void setup() {
  Serial.begin(9600);
  #ifdef DEBUG_ENABLED
      delay(5000);
  #endif
  pinMode(pin_PWDN_NUM, OUTPUT);
  pinMode(pin_RST_NUM, OUTPUT);
  pinMode(pin_START_NUM, OUTPUT);
  pinMode(pin_CS_NUM, OUTPUT);
  pinMode(pin_DRDY_NUM, INPUT_PULLUP);
  pinMode(pin_LED_DEBUG, OUTPUT);
  digitalWrite(pin_CS_NUM, HIGH);
  delay(2000);
  digitalWrite(pin_LED_DEBUG, LOW);

  vspi = new SPIClass(VSPI);
  vspi->begin(pin_SCK_NUM, pin_MISO_NUM, pin_MOSI_NUM, pin_CS_NUM);
  vspi->beginTransaction(SPISettings(SPI_FREQ, MSBFIRST, SPI_MODE1));
  delay(500);

  ADS1299_SETUP();

  ADS1299_RREG(0x00, register_readback, sizeof(register_readback));
  register_readback_ok = register_readback[0] != 0 && register_readback[0] != 0xFF;
  for (int i = 0; i < size_reg_ls; i++) {
    const regVal_pair pair = ADS1299_REGISTER_LS[i];
    const uint8_t mask = pair.add == 0x03 ? 0xFE : 0xFF; // CONFIG3 bit 0 is status.
    if ((register_readback[pair.add] & mask) != (pair.reg_val & mask)) {
      register_readback_ok = false;
    }
  }
  // Do not start conversions until a compatible host requests streaming.
  while (!waitForTimestamp()) delay(1);

  // --- FIX #2: Corrected Startup Sequence ---
  DEBUG_PRINTLN("Setup complete.");
  digitalWrite(pin_START_NUM, HIGH);
 
  // Add a brief delay BEFORE the START command to allow the chip to settle.
  delay(10);
  ADS1299_START();

  // Allow the ADC digital filter to settle before streaming (20 samples at 1 kHz).
  delay(20);
  ADS1299_RDATAC();
  // A DRDY event from before RDATAC does not guarantee a readable output frame.
  // Begin listening only after continuous-read mode is ready, then wait for
  // a fresh completed conversion instead of sending a stale/zero first frame.
  dataReady = false;
  attachInterrupt(digitalPinToInterrupt(pin_DRDY_NUM), onDRDYFalling, FALLING);
  // --- End of Fix ---

  digitalWrite(pin_LED_DEBUG, HIGH);
}

void loop() {
  // Reset the board to stop acquisition or start a new host session.
  //got rid of the micro check because it was causing 6 second spics, this check is a redundancy to the data ready flag check
  //unsigned long currentMicros = micros();
 // if (currentMicros - _last_query_time >= SAMPLE_PRD_us) {
   //   _last_query_time = currentMicros;
      if (dataReady) {
          dataReady = false;
     
          byte raw_data[ADS1299_TOTAL_DATA_BYTES];
          read_ADS1299_data(raw_data);

          const uint16_t START_MARKER = 0xABCD;
          const uint16_t END_MARKER = 0xDCBA;
          byte packet[PACKET_TOTAL_SIZE];

          packet[PACKET_IDX_START_MARKER] = (START_MARKER >> 8) & 0xFF;
          packet[PACKET_IDX_START_MARKER + 1] = START_MARKER & 0xFF;
          packet[PACKET_IDX_LENGTH] = PACKET_MSG_LENGTH;

           //New way of timestamping added 8_22
          // 1. Perform the calculation using 'double' for maximum precision.
         uint32_t millis_since_sync = millis() - _millis_reference;

         // 2. Pack this integer into the packet in BIG-ENDIAN order, which BrainFlow expects.
         packet[PACKET_IDX_TIMESTAMP]     = (millis_since_sync >> 24) & 0xFF;
         packet[PACKET_IDX_TIMESTAMP + 1] = (millis_since_sync >> 16) & 0xFF;
         packet[PACKET_IDX_TIMESTAMP + 2] = (millis_since_sync >> 8) & 0xFF;
         packet[PACKET_IDX_TIMESTAMP + 3] =  millis_since_sync & 0xFF;

          for (uint8_t i = 0; i < ADS1299_TOTAL_DATA_BYTES; i++) {
              packet[PACKET_IDX_ADS1299_DATA + i] = raw_data[i];
          }
          uint8_t checksum = 0;
          for (uint8_t i = PACKET_IDX_LENGTH; i < PACKET_IDX_CHECKSUM; i++) {
              checksum += packet[i];
          }
          packet[PACKET_IDX_CHECKSUM] = checksum;
          packet[PACKET_IDX_END_MARKER] = (END_MARKER >> 8) & 0xFF;
          packet[PACKET_IDX_END_MARKER + 1] = END_MARKER & 0xFF;

          Serial.write(packet, sizeof(packet));
      }
 
}
