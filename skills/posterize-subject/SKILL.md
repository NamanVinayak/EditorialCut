---
name: posterize-subject
description: Invoke to turn an isolated presenter (existing ProRes 4444 alpha) into a live editorial duotone poster — one accent color on dark/shadow regions, paper-white elsewhere, grain, clean canvas (the source-reference selective-luminance subject-poster treatment). Do NOT hand-roll a threshold/posterize filter chain; run this treatment.
---

# Posterize Subject

## Overview

Apply the accepted inner-luminance duotone to a person who is already isolated. Deterministic math only — no models, no new masking. Produces the treated live portrait plus the inner-mask asset.

## Prerequisites

A ProRes 4444 alpha master from `skills/track-and-mask/SKILL.md` (straight alpha; confirm by checking RGB in fully-transparent regions is non-uniform). Never modify it.

## Workflow

1. **Confirm inputs and record fingerprints** (SHA-256/size/mtime) of the alpha master.
2. **Decode once**: FFmpeg rawvideo pipe at `rgba64le` into numpy — preserves ProRes 12-bit precision; one decode can feed several concurrent encoder subprocesses.
3. **Per frame:**
   - `Y = 0.2126R + 0.7152G + 0.0722B` (normalized) on the person RGB;
   - `sel = 1 − smoothstep(lo, hi, Y)`; **accepted default `lo=0.20, hi=0.55`** (conservative `0.10/0.35`, aggressive `0.35/0.75` are measured alternatives);
   - inner mask `= sel × alpha` — must be exactly zero wherever alpha is zero;
   - duotone: mix accent (default `#B3271E`) toward white (`#F7F4EE`) as Y rises; shade the accent side by underlying luminance so dark regions keep structure — a flat accent slab is a rejection condition;
   - grain: `default_rng(seed=frame_index)` gaussian ±6/255, multiplied by the inner mask;
   - composite over a paper canvas (default `#F5F2EC`) using the person alpha.
4. **Render** H.264 `yuv420p`, frame-exact. Export the inner mask as a grayscale video too — **losslessly** (`crf=0`); lossy encoding bleeds edge-ringing past the silhouette and fails containment.
5. **Verify:** exact frame count/raster/fps/duration; containment (sample ≥20 frames: no inner-mask pixel >2/255 where alpha <2/255); face-crop stills to confirm structure readability; input fingerprints unchanged.
6. **Deliver** treatment video(s), matte video, contact sheets, face crops, `manifest.json` with all parameters and per-check results.

## Accepted envelope

Proven on the accepted 600-frame 1080p/30 RVM clip; three variants + matte in ~121 s on the M4 Pro. the project lead chose the reference variant as default from a same-frame side-by-side (2026-07-13).

## Boundaries

- Requires an existing subject alpha; producing one is `skills/track-and-mask/SKILL.md`.
- Colors and thresholds are parameters; the red/paper defaults match the source reference reference, not a brand rule.
- Typography, layout, and reframing around the portrait are downstream design decisions (see private derivation evidence (not distributed) for the reference composition language).
- Read `docs/capabilities/inner-luminance-mask.md` for the accepted decision and `research/luminance-mask/` for evidence.
