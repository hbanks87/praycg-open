# Decoder Gate v3: researcher protocol and scoring

Snapshot: November 10, 2026. This is a public procedural companion to the `DecoderGate_Pilot_Pack_v3_20261110` package (instrument version `DecoderGate_Pilot_v3_20261110`), not the complete runner or participant bank. The [materials ZIP](decoder_gate_v3_public_materials.zip) includes the exact settings file and a deliberately separate synthetic example.

## Design and presentation

The Comparison profile crosses coherent/reordered structure with narrative/analytic stance: CN, CA, RN and RA. Eight frozen lists cross each main passage with the four conditions and two immediate-fact assignments. Each 16-item main session contains four trials per condition, and each source author contributes once to every condition in that session. This balances assignment; it does not make texts equally difficult or produce equal exposure durations.

Natural reading uses coherent narrative without digits. It cannot estimate the four-condition contrast. Do not pool the profiles or migrate historical v1 records into v3.

Coherent texts retain complete contiguous source paragraphs with layout whitespace normalized. Reading uses a variable number of cumulative reveal units; earlier text remains visible and may be reread. The reordered version fixes the first and last unit and left-rotates the interior once. Paragraph breaks follow presentation positions, while source paragraph identity remains recorded. This rearrangement can alter grammar, reference continuity and processing difficulty along with coherence.

In Comparison, each passage has one fixed digit per presentation position and the same digit sequence across assignments. Sum only under analytic instructions. The participant does not repeat that passage under another assignment.

## Visits and outcomes

1. Select and retain the profile. Complete two distinct practice and four distinct calibration passages.
2. Complete Main Session 1 and Main Session 2, 16 new passages each with a halfway break.
3. Each trial uses an 8-second baseline, self-paced reading with explicit finish, 10-second post-reading quiet interval, responses and a 20-second washout. There is no reading deadline or visible countdown.
4. Return for each session's title-cued factual follow-up, targeting 24 hours, with a 22–26-hour pilot window. Both factual forms are asked for each main passage. Preserve actual delay, source visit, prompt exposure and timing flags.

Immediate comprehension and factual responses, delayed facts, analytic-task checks and optional clarity/flow/engagement/pressure/familiarity feedback remain distinct. “First-probed” identifies a factual form not previously asked; it does not prove the related content was never rehearsed. Delayed testing is not independent replication of immediate testing.

The primary software delay origin is the saved reading-finished event, with a separately flagged trial-start fallback if needed. These are software observations, not physical display-onset measurements. The optional standalone `DG_PILOT_V3_MARKERS` stream is disabled by default and does not start or qualify acquisition hardware. No fixed v1 critical-action neural window transfers to this self-paced design.

## Manual scoring

Use the version-bound researcher key and accept concise supported paraphrases. Do not grade by keywords, eloquence, confidence or agreement with an interpretation. Preserve a rater's uncertainty for adjudication; AI-assisted review is provisional and unblinded.

| Code | Meaning | In scored-accuracy denominator? |
|---|---|---|
| 1 | Correct, supported nonempty answer | Yes |
| 0 | Incorrect nonempty answer, including an explicit lack-of-knowledge answer when appropriate | Yes |
| U | Nonempty answer needing adjudication | No |
| M | Missing/blank answer | No |
| Empty score | Not yet scored | Only after a 0 or 1 is assigned |

Scored accuracy is `100 × correct / (correct + incorrect)`; report planned, missing, uncertain and unscored counts alongside it. A blank answer cannot be marked 0 or 1, and a nonempty answer cannot be marked M. Keep interrupted/unattempted trials in planned counts. A follow-up not yet created is absent follow-up coverage, not a zero memory score.

Summaries retain participant, material version, profile, stage family, source visit, condition and timing status. Combined rows already include their component condition rows. Do not sum both or silently pool versions/participants. The supplied synthetic script demonstrates only one descriptive group, with no hypothesis test or gate score.

## Constructing a new bank

Use texts you may reproduce; preserve exact source wording and original author credit. Freeze source edition, paragraph boundaries, reveal units, passage hash, digit sequence, two factual forms and answer criteria before collection. Review question premises and cross-question answer leakage. Freeze lists before assigning participants and keep the answer key away from participant routes. New text, timing, prompts or profiles require a new instrument identity and renewed qualification; this public example is not a replacement v3 bank.

## Evidence boundary

Standalone qualification recorded 88 Python checks, a complete synthetic Natural workflow and 64 delayed answers, four additional Comparison trials, recovery checks and fresh-extraction startup. It did not complete a 32-trial Comparison participant acquisition. The local 11.12.0 adapter separately records synthetic full workflows for both profiles; that is software evidence for a local candidate, not a public release or participant result. Neither establishes a real 24-hour effect, human norms, inter-rater agreement, physical timing or neuroscience validity.
