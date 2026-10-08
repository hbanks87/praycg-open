# Analysis Forge: Gamma Scalpel and optical exploration

Choose a completed recording folder in **Recording**. Stop LabRecorder before analysis so the XDF closes. The selected recording stays visible while you move between **Recording**, **Analyze** and **Results**.

## Gamma Scalpel

1. Open **Analyze** and choose **Gamma Scalpel**.
2. Let the Workbench identify the recorded EEG and any compatible EOG/EMG references. The report shows which references were usable and why others were omitted.
3. Open the completed report in **Results**. Compare the original method, measured-reference screening, retained duration and available condition comparisons.

EMG describes muscle activity; EOG describes eye activity. These references help identify windows in which scalp gamma may be affected. The report uses measured channels, actual coverage and declared timing support. Quiet references do not establish that all remaining gamma is neural. The four Athena electrodes cannot provide outcomes requiring additional measured regional electrodes.

The default is a measured-reference comparison. The original recording remains available alongside each derived result. Advanced reference profiles describe source assignments, participant identity, timing evidence or explicit analysis blocks where automatic metadata is insufficient. They are optional for the ordinary EEG-only fallback.

## Explore optical signals

1. Choose **Explore optical signals** in **Analyze**.
2. Use the default whole-recording scope and automatic spectral windows. If more than one optical source is recorded, select the intended source under **Details**.
3. Review raw trends, normalized changes where supported, quality annotations, full-data spectra and screened spectra in **Results**.

The action works across protocols and independently of EEG quality. It requires optical data saved in the XDF. An EEG-only recording cannot supply missing optical measurements later.

Automatic analysis prefers 30-second windows and uses labeled 10- or 5-second alternatives when needed. The report explains the selected window, frequency spacing, supported duration and gaps. Very short or irregular segments can still provide raw trends and statistics without a spectrum. Optional task scope and fixed windows are under **Details**. Compare recordings using the same source semantics and spectral settings.

## Hemoglobin estimates

Fixed instrument facts belong in a reusable, versioned profile. Each recording supplies its own source identity, baseline, coverage and binding to the original bytes. The conversion report identifies its profile and assumptions.

The bundled Athena profile currently supports raw exploration. Its missing channel mapping, source-detector geometry and intensity/firmware information are listed individually. HbO/HbR remains unavailable for that profile; raw optical analysis still completes. The [Athena source review](ATHENA_OPTICAL_SOURCE_REVIEW_ALPHA_10_5_2.md) describes what was established from public documentation.

## Long operations and results

The Forge shows the current operation and its progress. Cancel stops the current worker. Retry creates a new analysis attempt. Completed reports remain connected to their original recording and settings; selecting another recording does not silently open a previous recording's report.
