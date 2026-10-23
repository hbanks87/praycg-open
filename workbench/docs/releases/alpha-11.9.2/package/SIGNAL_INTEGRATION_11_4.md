# Signal review integration in Alpha 11.4.0

This release strengthens offline signal review without replacing raw recordings or changing a locked analysis plan. It adds more precise event-window support, explicit annotation bindings, reviewed comparison playback and delayed SPAR recording replay. The ordinary recording and analysis workflow remains available; these review tools do not add a new acquisition gate.

## Event windows need measured support

An event comparison now checks the baseline and response separately. Each reports its requested interval, usable intervals and duration, largest unsupported gap, accepted observations and known availability time. Gaps are not compressed, and a few finite samples cannot stand in for an adequately recorded window. Unknown timing uncertainty remains unknown.

Default review policy requires a 10-second window, at least 80 percent usable duration and no unsupported gap longer than 3 seconds. Adjacent sampled observations must also satisfy the declared step limits. These are configurable, versioned operational choices, not universal physiological minimums. They apply to descriptive event comparisons, not to whether an exploratory Athena recording may start. Beat-based measurements retain their original adjacency rules and require documented beat-clock semantics.

The sampled estimator remains an unweighted mean of retained finite observations. Its duration qualification is a separate check, not a time-weighted estimator. Retrospectively filtered values cannot be presented as having been available before the samples they required. Processing and sensor delays are not invented when they were not measured.

## Exclusions and reviewed inputs

Select a particular saved annotation version. Its source identity, file hash and active exclusions must agree with the recording and the comparison. Changing exclusions invalidates an older computed branch; it does not edit that branch or silently revise a locked plan. Corrections and retractions remain later, traceable annotation versions.

Saving a reviewed candidate records an explicit selection with its source, method, settings, support and annotation identity. Reopening checks those bindings. A candidate being reviewable does not establish that it is artifact-free, that it preserves a particular endpoint or that it is suitable for spatial analysis.

The Signal Review worker also accepts an explicitly selected annotation file and hash. This does not imply that every historical worker automatically consumes this ledger. A result must identify the version it actually used; absent integration is not silently described as applied exclusion.

## Compare and replay without changing the study

From Analysis Forge, open **Signal Quality & Cleaning Review**. In its processing-research controls, use **Open saved reviewed comparison** to inspect a selected derivative, or **Run delayed SPAR recording replay** for a deliberately selected interval of at most 60 seconds. Longer recordings are not silently shortened. Heavy processing runs outside the interface thread; cancellation is checked between processing chunks.

The comparison window offers playback, pause, rewind and seeking. It displays available original, current-recipe preview, candidate and difference traces. A source-verified linked cursor can coordinate inspection with compatible Visual Analysis views. It does not recalculate CAI fabric, SID residence, autonomic position or TFR merely by moving a cursor. A derived metric needs its own explicitly run, source-bound comparison.

Delayed replay uses the saved recording. Calibration windows and incomplete tails stay unchanged, unsupported samples remain visible as unsupported, and each declared continuous piece resets calibration even when timestamps happen to be adjacent. The report separates recording-clock availability from measured wall-clock processing time. Playback of this completed derivative is not a live acquisition filter, and it cannot change a protocol runner.

Replay arrays are private telemetry. They are saved separately from their compact receipt, with exact hashes, and are not automatically sent to an AI provider. Original samples, timestamps and study identity remain unchanged.

## SPAR preservation results

An explicit **leave unchanged** control preserves the input and runs no detector. It does not claim that the signal is clean. The optional independent-evidence policy permits correction only under reviewed, source-bound sensor masks. Validating a mask's declared provenance does not establish that its artifact interpretation is correct. That offline policy is not available in delayed replay.

The new frozen synthetic collection separates development and held-out waveform families and reports both incremental pass changes and cumulative changes. It does not choose a winning cleaner automatically. The earlier benchmark remains available unchanged.

The results include a serious limitation: the slow pass can remove wanted low-frequency synthetic activity. Both the reference candidate and preservation-focused variant also alter some other clean controls. The preservation-focused name describes its design, not demonstrated superiority. Do not promote a cleaner merely because the output looks smoother.

See [the frozen preservation benchmark](app/tools/Signal_Review_v1_0/validation/SPAR_FROZEN_PRESERVATION_BENCHMARK_v1.json) and [method records](app/tools/Signal_Review_v1_0/methods_spar_v1.json). MATLAB numerical agreement remains unestablished because authentic reference outputs have not been evaluated. No synthetic result establishes preservation of human gamma or theta events, connectivity, or a narrative-related endpoint.

## What still needs evidence

Independent review of real shielded controls, beat and artifact annotations, and frozen held-out Arrival or Contact evaluations remains necessary. Zuna is a comparison, not ground truth. Full processing-branch integration into CAI, SID and every visual estimator remains incomplete. Physical live cleaning, specialist source modeling and EEGPrep integration are not enabled by this release.

Use [BUILD_REPORT.md](BUILD_REPORT.md) for the actual software verification scope and [RELEASE_SCOPE_37.md](RELEASE_SCOPE_37.md) for the recommendation ledger. Preserve previous releases and results; a new explanation or software test does not retroactively validate an experiment.
