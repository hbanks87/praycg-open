# Patch Notes — PRAYCG MediaPrep v1.6Q

- Keeps v1.6P control-validity logic.
- Fixes the apparent no-op Run button issue by adding visible run-click logging.
- Adds input validation before spawning the media-prep worker.
- Adds thread-safe GUI logging via queue polling.
- Fixes delayed exception reporting by avoiding unsafe exception-variable closure behavior in Tk callbacks.
- Adds crash-file writing to the output root when possible.
- Adds an Open Last Output Folder button.
