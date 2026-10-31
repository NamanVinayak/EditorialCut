---
title: Speech / Music / Silence Segmentation
aliases:
  - Audio Scene Segmentation
  - Speech Music Detection
  - Voice Activity vs Music
type: capability
status: accepted-v1
updated: 2026-07-14
---

# Speech / Music / Silence Segmentation

## Decision

**Accepted for v1. Move on.** A separation-based, two-layer pipeline labels an audio timeline into **music-only / speech+music / speech-only / silence**, and it generalized across four stylistically different vlogs on one fixed configuration. Do not reopen unless a real project exposes a blocking failure.

Acceptance is by ear: the project lead reviewed a colored state timeline with a live "NOW: …" label against four of his own vlogs and confirmed the labels match what he hears. vlog1 also matched a detailed spoken ground truth he gave in advance.

## Editorial purpose

Produce a per-moment map of *what kind of audio is playing* so later steps (ducking/EQ, caption placement, beat-aware pacing) know where the voice is, where music plays, and where they overlap.

### The design decision that makes it work (learned the hard way)

**Detect speech and music as two INDEPENDENT layers, never one label per moment.** In real vlogs the music bed plays continuously and the voice sits on top of it — so the common case is *speech AND music at once*. A single-label segmenter (which must pick one winner) is structurally wrong for this: it will flatten "talking over music" to just one, and it reads quiet music as silence. Two independent tracks (a speech track and a music track) represent all four states — music-only, speech+music, speech-only, silence — natively.

This was proven by failure first: a single-label tool (inaSpeechSegmenter, see Rejected below) got the macro-structure roughly right but could not represent overlap, mislabeled quiet intro music as silence, and fragmented on natural speech pauses.

### Use it for

- Locating voice vs. music vs. overlap for dialogue-aware ducking/EQ (Job C prerequisite)
- Knowing when a music bed is present (including quiet continuous beds)
- Timeline context for captions and pacing

### Do not use it as

- A single mutually-exclusive label per moment — overlap is the norm, not an edge case
- A precise word/phrase boundary tool (that is transcription/VAD at finer scale)
- A guarantee on rubato/near-silent beds below the music floor (see limits)

## Proven implementation

- Workspace: `research/audio-intelligence/`
- Analysis env: `.venv` (CPython 3.12, PyTorch 2.13 MPS) with **Demucs 4.1** + **silero-vad** + soxr
- Pipeline ([`analyze_layers.py`](../../research/audio-intelligence/analyze_layers.py)):
  1. **Source-separate** the mix into a vocal stem + music stem — `demucs --two-stems=vocals -n htdemucs -d mps` (~14s/clip on Apple-Silicon GPU).
  2. **Speech track** = silero-VAD run on the *isolated vocal stem* (`min_silence_duration_ms=600`, `min_speech_duration_ms=250`). VAD on a clean vocal is far more reliable than on the mix — this is what makes it universal, not voice-loudness-dependent.
  3. **Music track** = 50 ms-frame RMS on the *music stem*, on where RMS > **−50 dBFS**. One global floor for all videos (on a voice-removed stem), not per-clip tuning.
  4. **Smooth** both (bridge natural pauses / brief dips): music merge-gap 1.5 s / min 0.5 s; speech merge-gap 0.8 s / min 0.25 s.
  5. **Combine** into four states per moment.
- Review surface ([`make_two_lane.py`](../../research/audio-intelligence/make_two_lane.py)): a colored state timeline + mix waveform + legend, rendered to a video with the original audio, a moving red playhead, and a live "NOW: <state>" caption. Playhead frames are drawn per-frame in PIL and streamed to ffmpeg (see the ffmpeg gotcha in limits).
- Sources remained read-only; separated stems live under `separated/htdemucs/`.

The reusable procedure is [`skills/segment-speech-music/SKILL.md`](../../skills/segment-speech-music/SKILL.md).

## Confirmed benchmark

First 60 s of four of the project lead's vlogs, one fixed config:

| Clip | Detected | Verified |
| --- | --- | --- |
| vlog1 "I AM BACK" | silence intro → speech+music 6.7–17.4 → music-only → speech+music 40.2–60 | matched spoken ground truth exactly, incl. the opening silence |
| vlog2 "the audio benchmark" | ~continuous music, many talk-over-music stretches | accepted by ear |
| vlog3 "the audio benchmark" | continuous music, sparse speech (~34s, ~52–57s) | accepted by ear |
| vlog4 "the prototype worked example" | music-only most of the minute, speech+music near the end | accepted by ear |

## Rejected alternative — inaSpeechSegmenter

The 2026-07 research named it primary, and it *runs*, but it was rejected for this job:
- **Single-label** (speech / music / noise / noEnergy) — cannot represent speech+music overlap, the dominant real case.
- **Level-sensitive** — tagged quiet intro music as silence.
- **Fragments** speech on natural pauses.
- **Install fragility** — an old tool on a modern stack; required ~6 rounds of version surgery (numpy<2 vs TF, `numpy.lib.pad`/`np.vstack(generator)` shims, `tf_keras` legacy-Keras) in its own isolated `.venv-seg`. Kept only as the renderer's matplotlib/PIL host, not in the analysis path.

## Human-observed limits

1. **The −50 dBFS music floor is a global heuristic.** A bed quieter than that reads as no-music; unusually loud non-music noise on the music stem could read as music. Validated across 4 vlogs; re-check on very different material.
2. **Speech VAD can fragment or catch short blips** (talky clips show many short pieces). Smoothing mitigates it; some pieces are real short utterances, some are twitches — human ear resolves.
3. **Silence only appears when both tracks are off.** Vlogs rarely have true silence (music is continuous); absence of grey is usually correct, not a miss.
4. **Boundary precision ≈ ±1–2 s**, and separation adds ~14 s/clip of compute plus possible stem artifacts.
5. **Tooling gotchas (durable):** ffmpeg `drawbox`/expression `t`/`n` were unreliable in this ffmpeg 8.1 build on looped-image input (playhead stuck at x=0) — draw moving overlays per-frame in PIL instead. Verify cut/marker positions with frame-number extraction or perceptual scene detection, never exact frame hashing (libx264 is lossy).

## Shared foundation with Job C

The Demucs vocal/music separation here is the same split Job C (dialogue-aware ducking/EQ) needs — once voice and music are separated, ducking is trivial and clean. Build the separator once; both jobs consume it.

## Operating rule

Confirm the exact clips and their intended use with the project lead before a new benchmark. Keep source audio immutable, store stems/outputs under `research/audio-intelligence/`, review by ear against a live state timeline, state uncertainty honestly, and stop tuning once accepted. The layer/state map is a reusable analysis asset; rendering and editorial choices are downstream.
