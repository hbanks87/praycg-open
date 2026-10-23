# Alpha 11.9 integration guide

This release consolidates Athena workflow corrections, supported paired-result viewing, breathing-task support checks and compact Cerelog capture review. It does not claim new physical validation, artifact-removal superiority or autonomous scientific discovery.

## Athena protocols

Select the actual Athena hardware before choosing a protocol. Atlas distinguishes whether the task can acquire this stream from whether its intended endpoint is supported. Exploratory EEG is not excluded merely because it is noisy. Missing task-critical physical channels, equipment or timing evidence are different limitations and remain explicit.

The current catalogs and software qualification are bound to this release. Historical qualification evidence remains historical; the carry-forward records no new device test. Older locally approved AI protocols are not silently reapproved after an engine change. Use the existing review workflow for an incompatible extension. For legacy Zuna tasks requiring 16 physical EEG channels, choose the dedicated Athena variant rather than inventing channels or weakening its declaration.

## Paired processing results

Open a registered paired processing result from the processing-results area. Its comparison viewer checks the saved registration, source receipt and array hashes before displaying anything. Choose Original or Processed and compare the same supported samples using fixed original calibration and scales. New results retain recording-clock origin; an older result without adequate timing metadata may require a new comparison derivative rather than a guessed origin.

The CAI/SID display reports the implemented, supported condition summaries. It does not turn a per-condition estimate into the legacy 10-second occupancy calculation. Missing autonomic position stays missing, and four-channel Athena does not become a full-montage CAI/SID recording. The viewer does not alter the original recording, locked plan or reviewed candidate.

## Breathing-task support

Cardiac measurements and measured respiration are checked separately against their duration, finite-data, gap and adjacency requirements. The report can describe supported respiration while marking unsupported cardiac endpoints unavailable. A completed worker is not proof that every measurement was estimable. Operational minimums are not universal scientific validity thresholds.

## Compact Cerelog capture review

Use the compact-review action in the existing Cerelog panel and select a closed standalone capture. Review reads the closed capture and checks its identity. Choose Export explicitly to create a new provenance-bound derivative directory. Neither action opens a serial port, flashes firmware, starts recording, publishes LSL or manufactures an XDF.

The compact layout is CH3 left temporalis, CH4 right temporalis, CH6 right frontalis, CH7 horizontal EOG, CH8 vertical EOG and CH5 ALS. CH1/CH2 remain raw packet slots but are disabled physiological inputs. Export preserves recorded device/host timing and observed gaps without inventing missing samples or synchronized timing.

The existing five-EMG pilot route remains separate. Compact live acquisition continues through its separately reviewed standalone capture tool. Hardware response, temple leads, eye cross-axis response, rail events and cross-device timing still need physical validation. No device-specific identity, raw body recording, firmware binary or private validation history is included in this release.

## Preserve an existing installation

Install beside the current application, not over it. Keep settings, study workspaces, recordings, reports and any externally stored models. If Zuna already uses a verified shared runtime/model location, retain that binding and location; do not reinstall or copy model weights just to update Workbench. Zuna reuse remains conditional on its pinned contract passing verification.

Public includes the independent PRAYCG AI Assistant, not AUL. The separate private AUL edition retains its existing history location and approval rules. Report approval is not evidence freshness, completed analysis, scientific validity or permission to modify a protocol. New pending reports need their own review.
