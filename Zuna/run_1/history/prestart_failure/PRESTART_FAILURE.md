> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Stopped before any model context because priority verification failed; later attempt completed separately.

# Preserved pre-start launcher failure

The launch at 2026-09-27 03:14:35 UTC stopped at the Windows priority-setting
check before execution claim creation, input preparation, model imports or model
inference. Zero contexts were processed. See execution_stderr.log and the frozen
full_comparison_plan.json; these files and the original wrapper remain unchanged.

Cause: ctypes declarations for the Windows process HANDLE were not explicit;
the call's default integer conversion did not provide the correct 64-bit handle.
The corrected launcher declares argument and return types and verifies observed
priority before any model work. The next sibling directory ending in attempt1
records this startup-only correction. It is not a retry after scientific results,
nor a change to data, masks, seeds, methods, endpoints or candidate app code.

The previously completed short-comparison wrapper called the same Windows API
without checking its return value. Its report's below-normal-priority statement
was therefore not verified. Two numerical threads and all model settings/results
were independently verified. This runtime-priority qualification does not change
the saved EEG, predictions or comparison metrics.
