---
name: composite-alpha
description: Invoke to composite a presenter alpha matte (ProRes 4444) with graphics behind and/or in front of the subject — the contract-checked background → rear graphic → subject alpha → front graphic layer stack. Do NOT hand-roll the layer stack or eyeball depth order; run the checked compositor.
---

# Composite Alpha

## Overview

Render the accepted four-layer depth stack in Remotion using a presenter alpha produced by `skills/track-and-mask/SKILL.md`. This skill owns layer mechanics and verification; it does not decide what the graphics say or how they look.

## Layer stack

```text
composition (same raster/fps/frame count as the alpha)
├── background plate (bottom)          — original footage or replacement canvas
├── rear graphics                      — occluded by the subject
├── subject alpha video                — ProRes 4444 via <Video> from @remotion/media
└── front graphics (top)               — never occluded
```

Behind vs. in front is declared **per element** (source reference rule), not once per composition.

## Workflow

1. **Confirm inputs.** Alpha master (ProRes 4444, `yuva444p*`) and background plate must share raster, fps, and frame count with the delivery composition. Record SHA-256/size/mtime of both; never modify them.
2. **Set up an isolated Remotion project** (local `npm install` only). **Hard-link** (`ln`, not `ln -s`) the two videos into `public/` — Remotion's render server 404s symlinks.
3. **Author the composition.** `<Video>` from `@remotion/media` for both video layers (it auto-falls back to `<OffthreadVideo transparent>` for ProRes alpha). Use the `objectFit` prop, not `style`. Place rear elements between background and alpha layer, front elements above the alpha layer.
4. **Render frame-exact.** `npx remotion render <Comp> out.mp4 --muted --color-space=bt709` — `--muted` when sources carry no audio (else AAC padding stretches duration), `bt709` to get plain `yuv420p`.
5. **Verify before delivery:**
   - ffprobe: exact frame count, raster, fps, duration ±1 frame;
   - occlusion frames: extract stills where the subject crosses a rear element (must be occluded) and where front elements sit (must be intact);
   - full-resolution edge crop where a bright rear element meets hair — no halo, no hard line;
   - input fingerprints unchanged.
6. **Deliver** the MP4(s), extracted proof frames/contact sheet, and a `manifest.json` (input checksums, versions, settings, timings, output checksums, per-check pass/fail).

## Accepted envelope

Proven on the accepted RVM clip: 1920×1080, 30 fps, 600 frames, three neutral layer tests, all verification green, accepted by the project lead 2026-07-13. Renders ~40 s per 20 s composition on the M4 Pro (concurrency 4).

## Boundaries

- Graphics content, typography, color, motion, and timing are downstream taste decisions — diagnostic layers stay neutral gray.
- This skill assumes an existing alpha master; producing one is `skills/track-and-mask/SKILL.md`.
- HyperFrames consumes the same contract as-is (checked 2026-07-13): plain `<video class="clip">` + CSS `z-index`, per-pixel occlusion confirmed. Mark intentional behind-subject text with `data-layout-allow-occlusion` or `hyperframes check` fails it; HyperFrames accepts symlinked assets (Remotion does not). See the capability page for details.
- Evidence and implementation live in `research/alpha-compositing/`.
