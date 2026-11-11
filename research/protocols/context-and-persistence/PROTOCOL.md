# Context and persistence: protocol, rubric and construction recipe

Public companion to `Contact_Context_Persistence_Pilot_v1`, version 1.0.0, November 10, 2026. The [materials ZIP](context_persistence_public_materials.zip) preserves the original protocol specification, but supplies only newly generated synthetic examples. This guide is not a turnkey replacement for the local film-based instrument.

## Study design

Randomize viewers to coherent or disrupted ordering in balanced blocks of four, two assignments per arm. The local pilot stops after 48 first assignments, retaining withdrawals and missing outcomes; 48 is a feasibility choice, not a power calculation. Each viewer sees one arm, with no crossover. Record familiarity and pre-exposure arousal before assignment. Keep allocation and source identities private from participants and scorers.

| First-visit phase | Duration |
|---|---:|
| Neutral baseline | 60 seconds |
| Assigned context | 180.18 seconds |
| Common neutral pre-ending interval | 15 seconds |
| Identical shared ending | 118.585133 seconds |
| Neutral washout, without questions/responses | 90 seconds |
| Attention, arousal and coherence ratings; return instructions | Self-paced |

The fixed stimulus/quiet time is 463.765133 seconds. Use the same display, audio level, instructions and acquisition setup across arms. Retain playback warnings and actual exposure histories. File identity does not prove identical delivered frames, acoustic onset or viewing attention.

The delayed visit targets 24 hours after recorded ending completion, with a primary window of 20–28 hours. Collect late answers with their timing labels. Give no immediate content test or correctness feedback. The fixed order is two near-transfer scenarios, two far-transfer scenarios, four causal-understanding questions, two literal-recall questions, then confidence and intervening exposure/discussion checks. Transfer-first reduces one source of coaching but can influence later understanding answers.

## Generic scoring rubric

Two independent condition-blind human raters receive masked responses, prompts, content-specific anchors and the authorized source material. They do not receive allocation, physiology, participant identity or one another's ratings. Response content can still reveal clues to assignment. The local content-specific film key is not included here.

The following framework describes the task; freeze item-specific examples and acceptable alternatives before enrollment.

| Score | General anchor for a submitted understanding/transfer answer |
|---|---|
| 0 | Explicit lack of knowledge, contradiction of the relevant evidence, or no relevant reasoning |
| 1 | Identifies a relevant element but omits or misstates the key relation |
| 2 | Gives the main supported relation with incomplete explanation or an important qualification missing |
| 3 | Explains the relevant relation using specific evidence and appropriately bounded inference |

Accept supported alternative interpretations. Belief, eloquence, confidence, emotional intensity and research vocabulary are not scoring criteria. Literal-recall items need their own factual anchors. A skipped, blank, absent or unsubmitted answer is **missing**, not 0. An explicitly submitted “I do not know” may receive 0.

Average the two ratings within each item, then average complete items within a domain. The primary score requires all four U1–U4 items, each with two ratings. Near transfer (T1–T2), far transfer (T3–T4) and literal recall (R1–R2) are separate secondary means. Preserve original ratings and disagreements; never substitute a single rater, fill blanks or select adjudication based on the outcome.

The primary contrast is the unadjusted coherent-minus-disrupted mean among complete valid in-window outcomes, explicitly labeled observed-case when outcomes are missing. Retain every assignment in flow counts. Do not adjust out post-exposure arousal, coherence or pre-ending state in that primary contrast: they may be part of the contextual effect.

For each arm with N assignments, observed score sum S and m missing primary outcomes, the possible all-assigned mean lies in `[S/N, (S + 3m)/N]`. The treatment-difference limits are `[lower_coherent − upper_disrupted, upper_coherent − lower_disrupted]`. These bounded-score limits are not confidence intervals. The local analysis additionally uses a block bootstrap conditional on valid observed outcomes, only with at least three allocation blocks and two observed participants per arm. The compact public demonstration calculates no inferential interval.

## Stimulus construction recipe

1. Use audiovisual material you are permitted to adapt and present. Freeze the source hash, rights statement, frame rate, decoded pixel format, audio sample rate, channels and cut boundaries. Changing source content requires new questions, rubric review and a new study identity.
2. For the local geometry, use 8,954 frames at 30,000/1,001 fps. The first 5,400 frames form twelve 450-frame context segments (15.015 seconds each); the remaining 3,554 frames form the shared ending.
3. Coherent order is `0,1,2,3,4,5,6,7,8,9,10,11`. Disrupted order is `0,8,3,10,5,1,9,4,2,7,6,11`. Preserve the first and last segments and use every segment exactly once.
4. Decode audio once to canonical 44,100 Hz, 16-bit stereo PCM. Round each video boundary to the nearest native audio sample. Preserve those samples in a lossless format. Preserve decoded native pixels losslessly; the local pilot used H.264 video and FLAC audio in MP4 and tested playback in Edge.
5. Encode only one ending file and bind both arms to its hash. Add the same 15-second neutral interval in the presenter. Verify decoded frame/audio inventories, order, durations and the common ending, not just filenames or container hashes.
6. Rehearse the actual display/audio environment and record buffering, drops, interruptions and measured delivery where available. Digital equality and headless playback checks do not establish physical timing. Reordering still changes transitions, sensory history, predictability and difficulty.

The ZIP's twelve text labels and shared-ending string demonstrate permutation and hash bookkeeping only. They generate no film, audio, sensor signal or timing qualification.

## Optional physiology and limits

The local exploratory feature is mean channel log 8–13 Hz power over O1/O2/Pz, using nonoverlapping 2-second detrended symmetric-Hann windows. Declared intervals include initial baseline 30–60 seconds, pre-ending 0–15 seconds, last 30 seconds of the ending, and washout 0–30 and 30–90 seconds. The late window avoids interpreting the immediate washout-start light pulse as persistence. Feature units, montage, gain, artifact screens and sensor timing must be documented independently.

Software/XDF markers alone support descriptive extraction. Prediction eligibility requires reviewed sensor-derived intervals and independent eye/muscle screens. The optional local prediction route needs at least 40 complete eligible viewers and participant-held-out folds with training-only scaling. It remains within-film prediction, not causal mediation or unseen-film validation. Calibration and synthetic software checks establish neither physical timing nor neural validity.

One excerpt and unvalidated candidate transfer measures cannot establish a general meaning effect. There are no human outcomes from this new randomized pilot in this publication.
