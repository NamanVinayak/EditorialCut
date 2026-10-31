---
name: detect-beats
description: Invoke to get a beat / downbeat / tempo map of a music track for cut-to-beat montages, beat-synced graphics, or tempo-aware pacing. Do NOT estimate tempo by ear or hand-roll onset detection; it finds both the small beats and the strong downbeats, and choosing which to cut on is a separate editorial decision.
---

# Detect Beats

## Overview

Turn a music track into a beat + downbeat + tempo map with `beat_this`, then let the editorial layer decide how densely to cut. Detection and cut-density are separate concerns: the tool finds every beat *and* the downbeats; the director/planner picks which layer to cut on. This is the automated equivalent of DaVinci Resolve's "Show Music Beats." See [`docs/capabilities/beat-detection.md`](../../docs/capabilities/beat-detection.md).

## Inputs

- A music audio file (wav/mp3/m4a). Full track is fine; analysis is ~1–2s per track on Apple-Silicon GPU.
- The proven environment: `research/audio-intelligence/.venv` (CPython 3.12, PyTorch MPS, `beat-this` 1.1.0).

## Workflow

1. **Detect.** Run `beat_this` via `File2Beats(checkpoint_path="final0", device="mps", dbn=False)` with `PYTORCH_ENABLE_MPS_FALLBACK=1` in the env. It returns two arrays of timestamps: `beats` (every beat) and `downbeats` (the strong "big beat" starting each bar). `detect_beats.py` wraps this and writes a JSON map with derived tempo. Re-measure per track.
2. **Choose the cut layer — editorial, not automatic.** Default to **downbeats** (calm, ~1 cut per bar, the accepted default). Use **every beat** only for a deliberately frantic montage, **every other beat** for medium pace, or **phrase boundaries** for slow builds. This choice belongs to the beat plan / director, not the detector.
3. **Derive tempo** as `60 / median(inter-beat interval)`. Treat it as a rough label, not a canonical BPM (metrical level can be half/double a human's count).
4. **Prove it visually when a human must judge.** Cut a random-image montage on the chosen layer (`build_montage.py <stem> <start> <end> <offset> <beats|downbeats>`) and review by ear. A cut-to-beat montage exposes misalignment instantly.
5. **Verify cut alignment perceptually.** Measure real cut times with ffmpeg scene detection (`select='gt(scene,0.25)',showinfo`), NOT exact frame hashing — libx264 is lossy and a held image changes pixels every frame, so hashing reports false cuts.

## Accepted envelope

Proven 2026-07-14 on three stylistically different royalty-free tracks (EDM / lo-fi hip-hop / rubato piano). Downbeat-cut montages landed one cut per downbeat, median 13ms error (within one frame), and were accepted by ear. `beat_this` correctly emitted no beats through a genuinely beatless 36s passage.

## Boundaries

- **Detection only.** Never bake "cut on every beat" into a tool — cut density is an upstream editorial dial. A first demo that cut on every beat was rejected; the identical detection re-cut on downbeats was accepted.
- **No song-structure labels** (intro/verse/chorus/drop). That is parked (`All-In-One` / NATTEN CUDA risk); `BeatNet` is the MPS-capable fallback beat tracker if `beat_this` ever fails.
- **Rubato / percussion-free material** has weak downbeats — flag for human review rather than trusting the grid.
- Evidence and reference implementation: `research/audio-intelligence/`.
