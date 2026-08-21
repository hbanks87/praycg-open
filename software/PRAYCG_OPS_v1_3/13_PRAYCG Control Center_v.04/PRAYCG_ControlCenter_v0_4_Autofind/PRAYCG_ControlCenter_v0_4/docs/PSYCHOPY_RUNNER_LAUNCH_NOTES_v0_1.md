# PsychoPy Runner Launch Notes v0.4

## Problem

On some Windows systems the PRAYCG2.0 runner does not behave correctly when launched with ordinary Python. The working workflow may be to open PsychoPy Coder and run the script from there.

## Control Center design choice

The Control Center defaults to a safe mode:

```text
Open PsychoPy Coder + open/show PRAYCG2.0 runner file/folder
```

This avoids claiming that direct launch is solved.

## Available modes

1. **Open PsychoPy Coder + runner file/folder**
   - recommended default.
   - user runs the runner from Coder.

2. **PsychoPy app + file argument**
   - experimental.
   - may work if PsychoPy accepts the script path from the shell.

3. **PsychoPy Python interpreter**
   - experimental.
   - use if you know the path to PsychoPy's Python interpreter.

4. **Regular Python**
   - least recommended for systems where the runner has failed outside PsychoPy.

## Recommended public documentation language

The Control Center is a launcher and folder manager. PsychoPy remains the authoritative runtime for the protocol runner until the runner is refactored and tested as a standalone application.
