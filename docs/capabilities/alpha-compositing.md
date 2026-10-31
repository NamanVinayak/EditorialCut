---
title: Alpha Compositing
aliases:
  - Alpha-Compositing Bridge
  - Layer Sandwich
  - Rear/Front Graphics Around a Matted Subject
type: capability
status: accepted-v1
updated: 2026-07-13
---

# Alpha Compositing

## Decision

**Accepted for v1: a Remotion composition consumes the accepted RVM ProRes 4444 alpha master as-is and renders the four-layer stack — background → rear graphic → presenter alpha → front graphic — with correct occlusion.** the project lead watched the three neutral layer tests (rear typography only, front badge only, both) on 2026-07-13 and accepted them as clean. No format conversion, re-matting, or custom decode work was needed.

This closes masking-family job 1 (the bridge from analysis asset to renderer). It proves the handoff contract, not any visual design: the gray diagnostic layers are evidence surfaces, never style templates.

## Editorial purpose

Turn a presenter matte into working depth compositing so an editor can:

- route large typography or graphics behind the presenter (source reference, source reference, source reference pattern);
- keep badges, captions, and accents unoccluded in front;
- choose behind vs. in front per element, not per composition (source reference's single-frame proof);
- build on a stable, verified layer stack instead of re-deriving it per project.

## Proven local implementation

- Renderer: Remotion (local render, `@remotion/media`)
- Alpha playback: `<Video>` from `@remotion/media`; it auto-falls back to `<OffthreadVideo transparent>` for ProRes 4444 sources (confirmed in render logs — no manual wiring)
- Benchmark composition: three tests over the accepted RVM clip (source 270.0–290.0 s, 1920×1080, 30 fps, 600 frames)
- Render time: ~39–43 s per 20 s composition at concurrency 4 on the M4 Pro
- Implementation and evidence: `research/alpha-compositing/` (`engines/remotion/src/`, `results/`, `manifest.json`, `verify.py`)
- Reusable procedure: [`skills/composite-alpha/SKILL.md`](../../skills/composite-alpha/SKILL.md)

## Asset contract (proven by consumption)

| Input | Contract |
| --- | --- |
| Presenter alpha | ProRes 4444 (`ap4h`, `yuva444p*`), same raster and fps as the delivery composition, exact frame count |
| Background plate | Any decodable video at the same raster/fps/frame count (H.264 proxy is fine) |
| Rear/front graphics | Renderer-native elements (DOM/SVG/text) declared per element as behind or in front of the alpha layer |

The alpha master produced by `skills/track-and-mask/SKILL.md` satisfies this contract with zero conversion.

## HyperFrames asset-contract check (passed 2026-07-13)

The same two-file contract was consumed **as-is** by HyperFrames (globally installed CLI v0.7.46 / npm v0.7.56 — the vendored `engines/hyperframes/` clone was not used, built, or modified). A plain `<video class="clip" src="assets/cutout-alpha.mov">` layered with CSS `z-index` produced correct per-pixel occlusion — verified down to text showing between individual raised fingers, not a bounding-box approximation. HyperFrames extracts video frames through its own FFmpeg path rather than browser `<video>` decode, which is why ProRes 4444 alpha works at all. Evidence: `research/alpha-compositing/hyperframes-check/` (5 s render + three proof frames; findings recorded here in lieu of a report file).

HyperFrames-specific gotchas:

- `hyperframes check` flags intentional behind-subject text as `text_occluded`/contrast errors (it reasons from DOM bboxes, not pixels); mark such elements with `data-layout-allow-occlusion`.
- Unlike Remotion's file server, HyperFrames accepted symlinked assets.
- `hyperframes init` writes/updates its skill folders globally (`~/.claude/skills/`, `~/.agents/skills/`) as default CLI behavior — a global side effect to expect when scaffolding.
- The render warned that the background plate `background-270-290.mp4` has sparse keyframes (~8.3 s interval), which risks seek failures in longer compositions. Re-encode with dense keyframes (`-g 30 -keyint_min 30`) before reusing that plate in anything beyond straight linear playback. This is a plate-encoding concern, not an alpha-contract concern.

## Render gotchas (field-tested, will recur)

- **Remotion's static file server 404s symlinks** (`serve-handler` disables symlink resolution). Hard-link assets into `public/` instead — same inode, no copy, originals untouched.
- **Add `--muted` when sources have no audio.** Otherwise Remotion attaches a silent AAC track whose 1024-sample quantization stretches container duration past frame-exact tolerance (20.053 s vs. 20.000 s).
- **Pin `--color-space=bt709`** to get plain `yuv420p` (tv range); the default produced `yuvj420p` (full range).
- Use the dedicated `objectFit` prop on `<Video>`, not the `style` prop (deprecation warning).

## Verification checklist (all passed in the accepted run)

- Output: exact frame count, raster, fps, and duration (±1 frame)
- Occlusion: rear element visibly occluded by the subject; front element never occluded — checked on extracted frames and full-resolution hair-edge crops
- Edges: no halo or hard cutout line where bright rear elements cross dark hair
- Sources: SHA-256/size/mtime of alpha master and original footage unchanged
- Manifest: input checksums, renderer/node versions, settings, timings, output checksums

## Design boundary

Same rule as subject masking: this capability delivers a correct layer stack, not a design. Which words go behind the presenter, their typeface, color, motion, and timing are downstream editorial/taste decisions. Diagnostic layers stay neutral gray.

## Project continuation

Job 1 of the masking family is closed. A small HyperFrames asset-contract check (can it consume the same ProRes 4444 layer?) runs separately and updates this page when it lands; it does not gate the next job. Next: job 2, the inner luminance mask (source reference treatment). Order and resume point live in the project review log.
