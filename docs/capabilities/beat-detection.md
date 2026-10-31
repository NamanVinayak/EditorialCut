---
title: Music Beat Detection
aliases:
  - Beat and Downbeat Detection
  - Detect Beats
  - Show Music Beats
type: capability
status: accepted-v1
updated: 2026-07-14
---

# Music Beat Detection

## Decision

**Accepted for v1. Move on.** `beat_this` detects beats and downbeats accurately, locally on Apple Silicon, fast enough to be a routine pipeline step. It is the automated equivalent of DaVinci Resolve's "Show Music Beats" for a scriptable editing system. Do not add competing beat trackers (madmom, BeatNet, librosa) unless a real project exposes a blocking failure.

No formal accuracy percentage was established — there is no per-beat human-labelled ground truth. Acceptance is by ear: the project lead reviewed downbeat-cut montages on three stylistically different tracks and called the result perfect.

## Editorial purpose

Produce a **beat + downbeat + tempo map** for a music track so later steps can synchronize cuts, graphic accents, and pacing to the music. This is the *detection* layer only.

### The two-layer distinction (the actual capability)

Music has two layers of beat: many small beats, and the stronger "big beat" that starts each bar (the **downbeat**). Editors cut on the big beats by default, not on every small subdivision. `beat_this` returns **both** layers. Choosing which layer to cut on — every beat (frantic), every downbeat (calm, the default), every other beat (medium), or phrase boundaries — is an **editorial/director decision, separate from detection.** The tool finds where the beats are; the planner decides how densely to cut.

This distinction was learned the hard way (2026-07-14): a first montage that cut on *every* beat was rejected as busy and wrong; the identical detection, re-cut on **downbeats only**, was accepted immediately. The detection was never the problem — the cut-density choice was.

### Use it for

- Beat-synced montage / cut timing (default: cut on downbeats)
- Timing graphic accents, flashes, and reveals to the music
- Tempo-aware pacing decisions downstream

### Do not use it as

- A fixed "cut on every beat" rule — cut density is chosen per edit, not by the detector
- A song-structure segmenter (intro/verse/chorus/drop) — that is **not** provided here; see "Parked" below
- A trustworthy beat grid on rubato / percussion-free material without human review
- A source of a canonical BPM number (see limit 2)

## Proven implementation

- Workspace: `research/audio-intelligence/`
- Local isolated environment: `.venv` with CPython 3.12.13, PyTorch 2.13.0 (MPS/Metal), `beat-this` 1.1.0
- Model: `beat_this` checkpoint `final0`, `device="mps"`, `dbn=False` (fast peak-picker), with `PYTORCH_ENABLE_MPS_FALLBACK=1`
- Scripts: [`detect_beats.py`](../../research/audio-intelligence/detect_beats.py) (audio → beat/downbeat/tempo JSON) and [`build_montage.py`](../../research/audio-intelligence/build_montage.py) (visual proof: cut an image montage on beats or downbeats)
- Performance: three full tracks (~2.5–4 min each) analysed in ~5s total on the GPU
- Review surface: image-montage MP4s cut on the detected downbeats, judged by ear
- Sources remained read-only

The reusable agent procedure is [`skills/detect-beats/SKILL.md`](../../skills/detect-beats/SKILL.md).

## Confirmed benchmark

Three royalty-free tracks chosen for a deliberate difficulty spread (`research/audio-intelligence/benchmark-media/`):

| Track | Character | Beats | Downbeats | Grid | Downbeat-cut result |
| --- | --- | ---: | ---: | --- | --- |
| easy-edm (NCS "On & On") | 4-on-the-floor EDM | 300 | 75 | rock-steady ~88 BPM | accepted |
| medium-hiphop ("Cruising") | lo-fi boom-bap | 212 | 62 | steady ~83 BPM, syncopated | accepted (the fair real-world test) |
| hard-ambient (Scott Buckley "Snowfall") | solo rubato piano, no drums | 274 | 94 | ~79 BPM with a 36s beatless intro correctly left empty | accepted, with the music-dependent caveat below |

Cut-alignment verification (perceptual scene detection vs. the detected times): exactly one cut per downbeat, **median error 13ms, all within one frame (33ms).**

## Human-observed limits

1. **Rubato / percussion-free music has weak, ambiguous downbeats.** On the solo-piano track the cuts can feel loose — this is the *music* lacking strong big beats, not the tool mis-detecting. Human review before trusting the grid for such material.
2. **The BPM number is a derived median, not a canonical tempo.** The EDM track reads ~88 BPM where a listener might count 176 (double-time). The *grid* is correct and usable; the absolute number and metrical level are not authoritative.
3. **Genuinely beatless passages return no beats — that is correct behaviour.** `beat_this` left a 36-second ambient intro empty rather than hallucinating a pulse. Do not treat gaps as failure; steer excerpts around them or hold on a shot through them.
4. **Verify cut alignment perceptually, not by exact frame hashing.** libx264 is lossy, so a held image differs pixel-by-pixel every frame; exact-hash diffing reports spurious "cuts." Use scene-change detection (`select='gt(scene,T)'`) to measure real cut times.

## Parked (not part of this capability)

- **Song-structure segmentation** (intro / verse / chorus / drop labels). The candidate tool, `All-In-One`, depends on NATTEN, whose fused kernels are documented CUDA-only — Apple-Silicon support unverified. Revisit only when an edit genuinely needs section labels, and smoke-test NATTEN on the M4 Pro before committing. `BeatNet` (explicit MPS support) is the fallback beat tracker if `beat_this` ever fails.

## Operating rule

Confirm the exact tracks and their intended use with the project lead before running a new benchmark. Keep source audio immutable, store outputs under `research/audio-intelligence/`, review by ear, state uncertainty honestly, and stop improving once accepted. Cut-density remains a downstream editorial choice — do not bake "cut on every beat" into any tool.
