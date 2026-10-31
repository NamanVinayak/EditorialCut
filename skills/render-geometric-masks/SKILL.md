---
name: render-geometric-masks
description: Invoke for renderer-native mask mechanics — difference flashes, cut bridges, circular reveals, before/after sliders, or the cinematic 3D screen-capture treatment. Do NOT hand-roll these with ad-hoc ffmpeg overlays; this is frame-exact CSS/DOM compositing in Remotion (or HyperFrames), no ML.
---

# Render Geometric Masks

## Overview

Apply the five accepted geometric/procedural mask primitives. All timing is frame-exact via `useCurrentFrame()` integer comparisons — never seconds, never CSS animations (seek-safety).

## Primitives

1. **Difference flash** — white rect, `mix-blend-mode: difference`, on/off at exact frames. Default event length **4–5 frames** (the project lead's recorded taste; shorter reads too fast). Stack = successive 3–4-frame events, ≤1-frame overlap, varied positions/sizes, clean plate after. Never show all stack rects simultaneously.
2. **Cut bridge** — 3-frame flash ending on the last frame before a hard cut + 3-frame flash starting on the first frame after. The cut frame itself is deterministic and never moves.
3. **Circular reveal** — expanding `clip-path: circle()` exposing a treated state of the same footage; ~1 s sweep, then hold. For "this became that" beats.
4. **Before/after slider** — 4 px vertical line at constant speed; treated state on one side, clean on the other, halves pixel-aligned.
5. **Cinematic screen capture** — screen/document content as a floating filmed object: `perspective: 1200px`; panel `scale(0.62) rotateX(12deg) rotateZ(2deg)`; rotateY drift ~5° per 4 s via `interpolate`; duplicated 28 px-blur layer + linear-gradient mask *inside* the panel (sharp center ~40 %); 2 px/10 % scanlines; `#0b0b0d` canvas + faint 120 px grid; all four corners in frame throughout the drift. Use for narrated screen recordings — blur everything except the passage being discussed.

## Workflow

1. Confirm footage + event map (which primitive, which absolute frames). Record source fingerprints; never modify inputs.
2. Isolated Remotion project; hard-link assets into `public/` (`ln`, not `ln -s`).
3. Author with integer frame windows; render `--muted --color-space=bt709`.
4. Verify: exact frame count/raster/fps/duration; **flash-timing proof** — extract each event window ±2 frames as stills and confirm first/last active frame; sliders/reveals: boundary alignment stills; screen rig: first/last drift frames show the angle change with no corner clipping.
5. Deliver MP4 + proof frames + manifest (event windows, settings, checksums, pass/fail).

## Gotchas

- Remotion 4.0.489: `clamp` not exported — inline it.
- ffmpeg `xstack`: cumulative-sum layout syntax (`w0+w1_0`), not arithmetic.
- No `drawtext` in some ffmpeg builds — generate text cards with Pillow.
- Slider/reveal treated states in diagnostics must be unmistakable (negate/grayscale, not subtle grain).

## Boundaries

- Concept-accepted, design-deferred: one coherent design pass will restyle all primitives after the concept library completes (the project lead, 2026-07-13). Don't restyle per project before then.
- Diagnostic label slates and gray styling are evidence packaging, not part of any primitive.
- Cursor/point tracking HUDs and subpixel zoom belong to later capabilities (jobs 5+), not this skill.
- Accepted decision: `docs/capabilities/geometric-masks.md`; evidence: `research/geometric-masks/`.
