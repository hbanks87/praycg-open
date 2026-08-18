# PRAYCG1.9C Patch Notes — Anchor Registration UX

## Problem fixed

The anchor field existed in prior runner versions but could be missed. This led to runs where anchors existed in planning notes but were not machine-registered in StasisMarkers/XDF.

## Fix

- Prominent LOCKED anchor file field.
- Auto-detect from cue schedule folder.
- Explicit validation warning if anchors are absent.
- Anchor file SHA-256 emitted into run config and markers.
- Draft files tolerated but not interpreted as confirmatory.

## Scientific classification

- **Conceptually predeclared:** anchor existed in notes/planning.
- **Runner-registered predeclared:** LOCKED anchor file loaded in runner before acquisition and emitted into the run logs.
- **Exploratory:** event found after looking at physiology.

Only the second can support strict preregistration-style claims.
