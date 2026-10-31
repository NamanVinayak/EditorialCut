---
title: Presenter World
aliases:
  - Presenter-World Composition
  - In-Scene Graphics
  - 2.5D Presenter Compositing
type: capability
status: accepted-v2
updated: 2026-07-16
---

# Presenter World

## Decision

**Accepted for v2 (2026-07-16): a Remotion composition places generated graphic elements *inside* a presenter's scene — behind the head, in front of the torso, riding transcript words — with a locked plate/cutout pair, a differential-parallax camera pull, a designed-canvas page swap under a persistent cutout, and virtual camera travel (discrete station hops and continuous diagonal/lateral travel) constrained to prevent boundary leaks.** the project lead reviewed and accepted all camera travel proofs on 2026-07-16.

**Scope honesty:** the full virtual camera travel capability is now fully proven, verified, and accepted in two modes:
1.  **Discrete station hops** (source reference style) — travelling between discrete destinations mapped to narration beats.
2.  **Continuous travel** (source reference style) — executing a diagonal push-in to focus on an element, followed by a continuous lateral slide to another element while zoomed.

Both modes require strict mathematical bounds checking on camera translation coordinates (`cx`, `cy`) relative to zoom scale `s` to guarantee the video plate never leaks boundaries to reveal background canvas grids or borders.

## What this capability actually is (the project lead, 2026-07-14)

Not an asset library. The ribbon, pill row, crossroads, and canvas page built here are worked examples, deliberately disposable. The durable capability is the **method for deriving new in-scene elements for footage the system has never seen**: measure the subject, author geometry relative to the subject, assign depth per segment, bind text to spoken words, and keep the scene rigid under camera motion. A future director agent looks at the footage and the narration, decides what *should* exist, and instantiates it from these recipes — it must never be limited to elements someone pre-built.

## Editorial purpose

- Make graphics feel like they share the room with the presenter (source reference/09/19 register) instead of floating on top like watermarks.
- Let one element cross depth: behind the head, in front of the chest — the source reference ribbon mechanic, proven on project footage.
- Put narration words on moving shapes, timed to the spoken word (source reference integrated-caption intro).
- Swap the real room for a designed canvas "page" while the presenter persists (source reference chapter swap; the bridge toward source reference's designed world).

## Proven local implementation

- Renderer: Remotion (`@remotion/media` `<Video>` for both plate and ProRes 4444 alpha; same contract as [`alpha-compositing.md`](alpha-compositing.md))
- Footage: accepted RVM clip (source 270.0–290.0 s, 1920×1080, 30 fps, 600 frames); word timestamps from a local mlx_whisper pass on the excerpt audio
- Renders: ~12–27 s per beat window, ~69 s for the full 600-frame timeline (M4 Pro)
- Implementation and evidence: `research/presenter-world/` (`engines/remotion/src/beats.tsx`, `engines/remotion/src/Compositions.tsx`, `render.py`, `verify.py` — 38 checks green, input hashes unchanged, audio muxed)
- Reusable procedure: [`skills/compose-presenter-world/SKILL.md`](../../skills/compose-presenter-world/SKILL.md)

## The generalized recipes (the durable knowledge)

1. **Silhouette-relative authoring.** Extract the subject's alpha (`ffmpeg … alphaextract`) at representative frames; read head span, face center, shoulder line off the mask. All element geometry is authored against these measurements, never against blind canvas coordinates. (This footage: head x 820–1240, face center ~(1030, 320), shoulder line y ~860–940 at 1920×1080.)
2. **Scene lock.** The background plate and the subject cutout are one physical scene: identical transforms at every frame, no exceptions. Depth cues come from transforming *graphics* layers only.
3. **Per-segment depth split.** One visible curve can be two SVG paths — the upper segment rendered in the rear layer (occluded by the head), the lower in the front layer (crossing the torso). Split where the curve crosses the silhouette.
4. **Text on a path, on a word.** SVG `textPath`; author paths in reading direction (left→right) or the text renders flipped; `pathLength={1000}` normalizes dash-based draw-in/retract regardless of true length; a word appears at `round(word.start × fps)` from the transcript JSON.
5. **Differential parallax.** Camera pull = root scale with center origin; rear graphics get `rearScale = 1 + (scale − 1) × k` (k ≈ 1.5) so they move slightly more than the locked scene — depth feel with zero risk of plate/cutout separation.
6. **Canvas page swap.** The designed page (flat color + grid or any canvas) lives in the background slot and swipes in under the persistent cutout; the subject never flickers because the cutout layer is untouched.

## Field-tested failure modes (both shipped once; check for them)

- **Double presenter.** Any transform applied to the plate but not the cutout (or vice versa) renders a second, offset copy of the subject — most visible as doubled ears/shoulders on one side. Cause of the round-2 rejection. The scene-lock rule exists because of this.
- **Invisible layers in chromium-headless.** `<Video>` not wrapped in `AbsoluteFill` collapses to inline flow and renders empty; a graphics wrapper `div` without absolute positioning collapses to height 0. Both shipped in round 1 — every layer must be an `AbsoluteFill` (or explicitly absolutely positioned).
- **Flipped textPath text** (path authored right→left) and **truncated dash animation** (`strokeDasharray` without `pathLength` normalization on paths longer than the dash value).
- A worker's "verified correct layering" prose passed while every one of these bugs was live — mechanical checks (frame counts, hashes) cannot see them. Only boundary-crop inspection catches them.

## Verification checklist (all passed in the accepted run)

- Frame counts exact per render window; assembled = 600 frames / 20.000 s with source audio muxed; raster/fps exact; input SHA-256 unchanged
- Occlusion both directions at silhouette contacts (hair over rear band, front band over shirt), checked on extracted full-res crops from the *deliverable* MP4s, not the preview
- **Single-silhouette check during camera motion** (crop at a shoulder edge mid-pull — no doubling)
- Words appear within their spoken windows

## Process lesson (recorded 2026-07-14)

Scaffold, rendering, and batch work delegate fine (Antigravity worker). Composition and motion logic did not survive two delegated rounds — geometry and depth reasoning need the head session's pixel loop. Keep authored-motion code in-session; delegate mechanical bulk.

## Design boundary

Muted purple bands, white system-font words, cream grid page — all diagnostic surfaces, not design. The one coherent design pass over all primitives comes after the concept library completes. Do not restyle this slice ad hoc.

## Project continuation

Masking-family and presenter-world mechanics are closed. Next: **audio/music intelligence** (beat/downbeat/section mapping, speech/music/silence timing, ducking evidence — videos 03, 13, 15, 19), then wiki/skill extraction across the 24 canonical docs, then the beat-map planner. Order and resume point live in the project review log.
