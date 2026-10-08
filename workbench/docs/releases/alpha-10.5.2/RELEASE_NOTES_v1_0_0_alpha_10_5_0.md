# PRAYCG Workbench Alpha 10.5.0 release notes

The Workbench previously offered EEG traces, a channel-mean live spectrum and saved numerical analyses. Alpha 10.5.0 adds optional electrode-specific spectral history to Live Monitor and an offline Time–Frequency Explorer in Analysis Forge.

The shared viewer presents electrode heatmaps and a rotatable categorical-channel volume. Live data are calculated from the observer's full-resolution samples. Offline views keep source-aligned support, quality reasons, missing intervals, processing labels and actual recording conditions. Saved event-related results retain their original method and eligibility.

The viewer and numerical adapter are original Workbench implementations. The concept was reviewed from eeg-tfr-volume; upstream code and example human EEG are excluded from the software package.

The complete distribution includes INSTALL.bat, INSTALL_ZUNA.bat, START_PRAYCG.bat and app/. Current release evidence covers the full installation, software regression, numeric fixtures, shared viewer and live observer behavior. Physical headset acquisition and physiological artifact ground truth are separate qualification scopes.

See the [changelog](CHANGELOG.md), [installation guide](INSTALL_AND_WORKFLOW_ALPHA_10_5_0.md), and [feature guide](TIME_FREQUENCY_EXPLORER_ALPHA_10_5_0.md).
