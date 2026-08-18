# PRAYCG MediaPrep v1.6Q GUI Button Hotfix Method Note

## Purpose

The v1.6Q build fixes a usability failure mode in which clicking the GUI run button could appear to do nothing. The media-prep logic remains the v1.6P control-validity pipeline, but the interface now exposes immediate operator feedback and error logging.

## Operator-visible changes

- A **Validate Inputs** button checks the selected master MP4 and output folder.
- The **Run Stimulus Media Suite v1.6Q** button immediately writes `RUN BUTTON CLICKED` to the log.
- The run button disables while the worker is running and re-enables on completion or error.
- Progress messages are routed through a thread-safe queue instead of updating Tkinter directly from the worker thread.
- If the run fails, the traceback is shown in the log and written to a crash file when an output root is available.
- The **Open Last Output Folder** button activates after successful completion.

## Scientific behavior unchanged from v1.6P

The pipeline still follows the current PRAYCG stimulus logic:

1. optional visual cleanup is applied to the master before branching;
2. cue-embedded Target is rendered;
3. cue-embedded Override is copied from Target so the two files are bit-identical;
4. phase-scrambled Control is generated from the cue-embedded Target;
5. cue schedule JSON/CSV, manifest, report, and QC checklists are written.

## Failure standard

If the GUI does not visibly log `RUN BUTTON CLICKED` after pressing the button, the Python process or Tkinter event loop is not responding. Run the script from Command Prompt using the example BAT so console errors remain visible.
