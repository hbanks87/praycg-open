import asyncio
import struct
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from pylsl import StreamInfo, StreamOutlet

HR_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

print("Initializing Polar H10 LSL Outlet...")
info = StreamInfo('PolarHRV', 'ECG', 1, 0, 'float32', 'polar_h10_mac_01')
outlet = StreamOutlet(info)
print("LSL Stream 'PolarHRV' established.")

def hr_data_handler(sender, data):
    try:
        flags = data[0]
        is_16bit_hr = (flags & 0x01) != 0
        current_hr = struct.unpack_from("<H", data, 1)[0] if is_16bit_hr else data[1]
        
        energy_present = (flags & 0x08) != 0
        rr_present = (flags & 0x10) != 0
        
        print(f"[DIAGNOSTIC] Raw HR: {current_hr} bpm | RR Present: {rr_present}")
        
        if rr_present:
            offset = 1  
            offset += 2 if is_16bit_hr else 1  
            if energy_present:
                offset += 2  
            
            while offset + 1 < len(data): 
                rr_raw = struct.unpack_from("<H", data, offset)[0]
                rr_ms = (rr_raw / 1024.0) * 1000.0
                
                outlet.push_sample([rr_ms])
                print(f"  -> Beat Caught: {rr_ms:.2f} ms")
                offset += 2
                
    except Exception as e:
        print(f"[ERROR] Callback Error during unpack: {e}")

async def run_polar_bridge():
    while True:
        print("\nScanning for Polar H10...")
        devices = await BleakScanner.discover(timeout=5.0)
        polar_device = next((d for d in devices if d.name and "Polar H10" in d.name), None)

        if not polar_device:
            print("Polar H10 not found. Retrying in 3 seconds...")
            await asyncio.sleep(3)
            continue

        print(f"Found {polar_device.name}. Attempting connection...")
        
        try:
            async with BleakClient(polar_device, timeout=15.0) as client:
                print(f"Connection Status: {client.is_connected}")
                
                if client.is_connected:
                    print("Stabilizing connection...")
                    await asyncio.sleep(1.0)
                    
                    services = client.services
                    
                    print("Subscribing to Heart Rate notifications...")
                    await client.start_notify(HR_MEASUREMENT_UUID, hr_data_handler)
                    print("Successfully subscribed! Waiting for data...")
                    
                    while True:
                        await asyncio.sleep(1)
                        if not client.is_connected:
                            print("Connection dropped by adapter. Restarting loop...")
                            break
                            
        except BleakError as e:
            print(f"Bleak Connection Error: {e}. Retrying...")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"General Connection Error: {e}. Retrying...")
            await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(run_polar_bridge())
    except KeyboardInterrupt:
        print("\nScript terminated by user.")