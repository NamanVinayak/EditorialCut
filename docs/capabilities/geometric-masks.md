---
title: Geometric Masks
aliases:
  - Renderer-Native Masks
  - Difference Flash
  - Wipes and Reveals
  - Cinematic Screen Capture
type: capability
status: accepted-v1-concept
updated: 2026-07-13
---

# Geometric Masks

## Decision

**Accepted for v1 at concept level (the project lead, 2026-07-13): all five renderer-native mask mechanics are correct and proven frame-exact in Remotion. Design polish is explicitly deferred** — the project lead's verdict: "the concept of the basic effect is right… not the best design work right now, and that is okay." A dedicated design pass over all primitives happens after the concept library is complete. Do not restyle these ad hoc per project before that pass.

Closes masking-family job 3. No ML models involved — pure renderer capability (CSS/DOM in Remotion; equally expressible in HyperFrames).

## The five primitives and their accepted parameters

| Primitive | Mechanic | Accepted parameters / rules |
| --- | --- | --- |
| Difference flash | White rect over footage, `mix-blend-mode: difference`, frame-exact on/off | **Default 4–5 frames per event (the project lead taste rule — tutorial's 2–3 frames read as too fast).** Stacked: successive 3–4-frame events with at most 1-frame overlap — never simultaneous (source reference's "one flashing in, one flashing out"). Clean plate restored after. |
| Cut bridge | Flash pair straddling a hard cut | 3-frame event ending on the last pre-cut frame; 3-frame event starting on the first post-cut frame; the cut frame itself never moves. Reads best when the two scenes are visually distinct. |
| Circular reveal | Expanding `clip-path: circle()` swaps footage for a treated state | Complete over ~1 s, then hold. Editorial home: "this became that" beats — before/after of a design, grade, or thumbnail (source reference's critique→fix transform). |
| Before/after slider | Vertical line sweeps; treated state one side, clean the other | 4 px line, constant speed, halves always aligned. Diagnostic lesson: the treated state must be unmistakable (film grain was invisible; negate/grayscale read instantly). |
| Cinematic screen capture | Screen content as a filmed 3D object with focus band | Landscape recipe (adapted from source reference's portrait values): `perspective: 1200px`; panel `scale(0.62) rotateX(12deg) rotateZ(2deg)`; continuous rotateY drift ~5° per 4 s (−12°→−7°) via `interpolate` (seek-safe, no CSS animations); DoF = duplicated 28 px-blurred layer with linear-gradient mask **inside** the panel; 2 px scanlines at 10 % overlay; canvas `#0b0b0d` with 120 px grid at 8 %; panel fully in frame, all corners visible. Home use: screen recordings/documents — blur all but the passage being narrated. |

## Taste rules recorded from the project lead's review (2026-07-13)

- Flash events: slightly longer than tutorial default — 4–5 frames at 30 fps.
- Partial-region inversions read as a deliberate, likeable style; **variant inversions/conversions per region are a welcome stylistic space** for the future design pass.
- Demo/evidence content must make an effect's purpose legible: focus-band on a talking head demonstrated nothing; on dense text it was obvious. Choose diagnostic content per primitive.

## Field-tested gotchas

- Remotion 4.0.489 does not export `clamp`; inline `Math.min(Math.max(...))`.
- Frame-exact events must use `useCurrentFrame()` integer comparisons, never seconds.
- ffmpeg `xstack` layout needs cumulative-sum syntax (`w0+w1_0`); arithmetic (`2*w0`) silently mis-lays the grid.
- System ffmpeg may lack `drawtext`; Pillow is the fallback for text-card generation.
- All prior Remotion render flags still apply (hard links into `public/`, `--muted`, `--color-space=bt709`).

## Evidence

`research/geometric-masks/`: conformance reel (600 frames exact), flash-proof frame sequences proving every event window to the frame, drift-proof frames, contact sheets, `manifest.json`, `verify.py` (20 checks). Built via the delegated-worker model (spec + fix instructions from the head session; three iterations: stack retiming → reviewer legibility fixes → screen-rig reframing). Source plates untouched throughout (SHA-256 verified).

## Design boundary

Concept ≠ design (same rule as the cyan banner): these primitives are mechanically accepted evidence surfaces. Typography, color, easing character, and composition get one coherent design pass across the whole primitive library later — not incremental restyling per benchmark.

## Project continuation

Job 3 closed. Next: job 4 — prompted arbitrary-object silhouette + temporal propagation (EdgeTAM on one non-human object). Reusable procedure: [`skills/render-geometric-masks/SKILL.md`](../../skills/render-geometric-masks/SKILL.md). Order and resume point: the project review log.
