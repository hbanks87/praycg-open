# Patch Notes — v1.2 Port Helper Edition

## Added

- `praycg_identify_openbci_port_v1_2.py`
- `--list-ports` support inside the bridge
- `--auto-port` support inside the bridge
- interactive COM-port prompt if omitted
- Tkinter launcher GUI
- Windows BAT files

## Preserved from v1.1

- BrainFlow-to-LSL bridge
- reconstructed timestamp mode
- `OpenBCIStatusMarkers`
- `OpenBCIDiagnostics`
- packet/backlog/gap/rate markers
- EEG watchdog
- XDF timing-grade verifier

## Fixed user-facing failure mode

Running the bridge without `--serial-port COMx` no longer throws an opaque error. The script lists candidate ports and prompts for a port unless `--no-interactive` is used.
