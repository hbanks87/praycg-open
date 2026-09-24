# Hardware support in Alpha 10.2.1

The Workbench's software routes and the repository's [physical hardware projects](../../hardware/README.md) answer different questions. An available connector does not certify an attached device, electrode placement, electrical safety, calibration or stimulus synchronization.

This index reflects the preserved Alpha 10.2.1 documentation. For the complete route contract, read `app/docs/HARDWARE_ROUTES_ALPHA_10_2_1.md` inside the [application ZIP](../releases/alpha-10.2.1/PRAYCG_ControlCenter_v1_0_0_alpha_10_2_1.zip), together with sections 5–7 of the [workflow guide](releases/alpha-10.2.1/WORKFLOW_ALPHA_10_2_1.md).

## Route categories

| Category | Routes described by the release | Operating boundary |
| --- | --- | --- |
| Managed connectors | Neurosity Crown OSC through BrainFlow; Muse S Athena through BrainFlow; Polar H10 ECG; GazePoint GP3 and GP3 HD | Route-specific PRAYCG launchers/publishers are supplied. These newly integrated routes remain experimental pending physical-device and timing validation. |
| External publishers | OpenMuse Athena EEG, motion, optics and battery; Pupil Core scene gaze and pupillometry; Pupil Neon gaze; OpenViBE LSL | Install and manage the publisher separately, review its live outlet and preserve the exact outlet metadata. |
| Retained routes | OpenBCI with or without ALS, Polar RR, Vernier and existing generic LSL routes | The release's route-specific evidence and readiness requirements still apply. |
| Withheld route | Cerelog 16 | The release does not expose a runnable profile because its exact transport, scaling, timing and physical contract are insufficiently established. |

Newly integrated Alpha 10.2.1 routes require an `EXPERIMENTAL_EVALUATION` profile and **Bench Test Mode (no participant)**. An installation pass does not change this status.

## Details that affect interpretation

- Crown uses the reviewed BrainFlow OSC route; do not substitute another signal identity in reports.
- Muse S Athena supplies no ALS. Its raw optical values are not validated fNIRS or hemoglobin measurements.
- An OpenMuse p1041 EEG outlet may include four named electrode channels and four AUX channels. Preserve that distinction.
- Polar H10 ECG and the irregular RR stream are separate routes. Concurrent BLE clients can be unsupported by the device or operating system.
- GazePoint requires GazePoint Control and calibration. GP3 and GP3 HD have separate route identities.
- Restarting a publisher can change its outlet identity. Re-review the outlet in a fresh equipment session instead of retaining a stale lock.

The [Cerelog EMG + ALS firmware project](../../hardware/cerelog-emg-als/README_FOR_SIMON.md) is a separate custom hardware review package. Its presence does not add a supported route to the preserved Alpha 10.2.1 application or resolve the withheld Cerelog 16 contract.

[Workbench](../README.md) · [Installation](installation.md) · [Workflow](workflow.md) · [Hardware projects](../../hardware/README.md)
