---
title: Inner Luminance Mask
aliases:
  - Selective Luminance Subject Poster
  - Duotone Presenter Treatment
  - Luminance Posterization
type: capability
status: accepted-v1
updated: 2026-07-13
---

# Inner Luminance Mask

## Decision

**Accepted for v1: deterministic luminance thresholding inside the person alpha, with the `reference` variant (lo=0.20, hi=0.55) as the documented default.** the project lead compared three threshold variants on the same frame side-by-side and in motion on 2026-07-13 and chose the middle intensity: red claims the shadow side of the face while the lit side keeps pale highlights. Thresholds remain tunable parameters per use, not fixed constants.

This closes masking-family job 2 (source reference's "selective luminance subject poster" treatment). No ML model is involved — the capability is pure math on top of an existing subject alpha.

## Editorial purpose

Elevate an important person or quote into a live editorial poster: the isolated presenter is rendered in one deep accent color plus paper-white, keeps moving and talking, and reads as a designed graphic rather than footage. The two-mask structure is the capability:

1. outer temporal person alpha (from `skills/track-and-mask/SKILL.md`) creates the canvas;
2. inner luminance-derived mask decides which regions inside the person receive the accent.

## Proven local implementation

- Pipeline: single FFmpeg `rgba64le` rawvideo decode (preserves 12-bit ProRes precision, straight alpha confirmed) → numpy per-frame math → concurrent H.264 encodes
- Selection: `sel = 1 − smoothstep(lo, hi, Y709)` on the person's RGB, multiplied by alpha; inner mask is exactly zero outside the person (verified: 0 violations across ~29M sampled low-alpha pixels)
- Duotone: accent `#B3271E` → white `#F7F4EE` as luminance rises, with the accent side luminance-shaded so dark regions keep tonal structure (never a flat slab — source reference's core rejection rule)
- Grain: seeded per-frame gaussian (±6/255), gated to the accent regions only
- Canvas: warm paper `#F5F2EC`, full frame, no repositioning
- Accepted default thresholds: `lo=0.20, hi=0.55`; measured alternatives: conservative `0.10/0.35`, aggressive `0.35/0.75`
- Wall time: ~121 s for all three 600-frame variants + matte in one pass on the M4 Pro
- Implementation and evidence: `research/luminance-mask/` (`process.py`, `verify.py`, `results/`, `manifest.json`)
- Reusable procedure: [`skills/posterize-subject/SKILL.md`](../../skills/posterize-subject/SKILL.md)

## Verification checklist (all passed in the accepted run)

- Exact frame count/raster/fps/duration on all outputs
- Inner-mask containment: no selection outside the person alpha (matte artifact must be encoded lossless — normal H.264 edge-ringing bleeds ~23/255 past the silhouette and fails this check)
- Structure readability: full-resolution face crops show facial modeling surviving inside accent regions
- Source fingerprint unchanged

## Design boundary

Accent color, canvas color, thresholds, and any typography/layout around the portrait are downstream taste decisions. This capability delivers the treated live portrait and the inner-mask asset; source reference's text lockup and composition rules live in the reference doc, not here. The red default matches the saved reference and is a parameter, not a brand rule.

## Project continuation

Job 2 is closed. Next: job 3 — renderer-native geometric/procedural masks (Difference flash, circular reveal, before/after slider, texture wipe, gradient focus band) proven as one conformance reel. Order and resume point live in the project review log.
