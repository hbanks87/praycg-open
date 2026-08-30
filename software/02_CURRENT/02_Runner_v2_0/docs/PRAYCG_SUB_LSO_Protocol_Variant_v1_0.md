# LSO / SPM: Lexical-Subtitle Override and Subtitle Phase Mapping

**Status:** optional protocol variant. Not part of the default clean PRAYCG1.9 run unless explicitly selected.

## Purpose

Subtitle Override tests whether the same narrative payload changes its physiological trajectory when semantic access is routed through forced visual lexical decoding instead of natural audiovisual absorption.

## Conditions

Recommended first-pass design:

1. Phase-scrambled Control - no intelligible story.
2. Natural Target - original audio, no subtitles.
3. Math Override - same target video, running-sum cue task.
4. Subtitle-only Override - audio muted, subtitles visible, no number cues.
5. Optional Subtitle Visual-Control - muted, nonsemantic or scrambled text matched to subtitle timing.

Do not combine number cues and subtitles in the first version. That creates too many simultaneous manipulations.

## Lexical Extraction Cost

For subtitle line \(i\):

\[
LEC_i=w_c z(CharsPerSec_i)+w_w z(WordsPerSec_i)+w_l z(LineLoad_i)+w_s z(SegmentationDifficulty_i)+w_g z(GazeRevisits_i)
\]

## Subtitle-MRED update

\[
MR^{sub}_j=0.30z(MeaningGamma_j)+0.30z(TSP_j)+0.20z(K_{local,j})+0.20z(LexicalRecognition_j)-0.20z^+(Artifact_j)
\]

\[
ENC^{sub}_j=0.55z(H_{\theta,j})+0.15z(API_A)+0.15z(Novelty)-0.20z(Familiarity)-0.25z(LEC_j)-0.20z(TaskGamma_j)-0.15z^+(Artifact_j)
\]

## Subtitle choke flag

\[
SubtitleChoke_j=1[MR^{sub}_j>\theta_{MR}]\cdot1[ENC^{sub}_j<\theta_{ENC}]\cdot1[LEC_j>\theta_{LEC}]
\]

Interpretation: semantic recognition survived, but lexical-extraction cost may have reduced or delayed integration.

## Subtitle Phase Mapping

Subtitle reading can occur before or after the actor finishes speaking. Therefore, the semantic anchor should not automatically be the audio line marker.

\[
\phi_i = t_{semantic,i}-t_{audio,i}
\]

Preferred timing source:

- gaze completion inside subtitle bounding box, if eye tracker exists.

Fallback:

\[
t_{0,i}=\arg\max_{t\in[t_{on,i}-2.0,t_{off,i}+1.0]} [TSP(t)+MeaningGamma(t)-Artifact(t)]
\]

This fallback must be frozen before analysis.

## Boundary

Gaze completion is a timing proxy for text ingestion, not proof of comprehension. TSP argmax is a semantic-timing estimate, not true reading time.
