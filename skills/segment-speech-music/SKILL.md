---
name: segment-speech-music
description: Invoke to map where voice, music, and their overlap occur along an audio timeline (music-only / speech+music / speech-only / silence). Do NOT infer speech regions from a raw amplitude gate; it separates speech and music as two INDEPENDENT layers via source separation, so talking-over-music is represented natively.
---

# Segment Speech / Music / Silence

## Overview

Map an audio track into per-moment states — **music-only, speech+music, speech-only, silence** — by detecting speech and music as two *independent* layers. The key idea: in real footage the music bed is continuous and the voice sits on top, so a single-label segmenter (one winner per moment) is structurally wrong. Separate the voice from the music first, then detect each independently. See [`docs/capabilities/speech-music-segmentation.md`](../../docs/capabilities/speech-music-segmentation.md).

## Inputs

- An audio file (or a clip's audio; extract with ffmpeg, source untouched).
- The proven env: `research/audio-intelligence/.venv` (CPython 3.12, PyTorch MPS, Demucs 4.1, silero-vad, soxr).

## Workflow

1. **Separate** the mix into a vocal stem + music stem: `demucs --two-stems=vocals -n htdemucs -d mps -o separated <clip.wav>` (~14 s/clip on Apple-Silicon GPU). This is the same separation Job C (ducking) uses — do it once.
2. **Speech track** = silero-VAD on the *vocal stem* (`min_silence_duration_ms=600`, `min_speech_duration_ms=250`). Load audio via soundfile + soxr-resample to 16 kHz and pass the tensor directly (torchaudio 2.11 needs `torchcodec` for its own loader — bypass it). VAD on an isolated vocal is reliable regardless of how loud the voice was in the mix.
3. **Music track** = 50 ms-frame RMS on the *music stem*; on where RMS > **−50 dBFS**. One global floor for all videos (it's on a voice-removed stem) — do NOT tune it per clip.
4. **Smooth** both to bridge natural pauses / brief dips: music merge-gap 1.5 s + min 0.5 s; speech merge-gap 0.8 s + min 0.25 s.
5. **Combine** per moment into the four states; emit a layers JSON (`music: [[s,e]…]`, `speech: [[s,e]…]`).
6. **Review, when a human must judge:** render a colored state timeline + waveform with the original audio, a moving playhead, and a live "NOW: <state>" caption. Verify by ear that the segments and the live label match what's heard.

## Accepted envelope

Proven 2026-07-14 on the first 60 s of four different vlogs (talky, music-heavy, sparse-speech), one fixed config. vlog1 matched a detailed spoken ground truth including its opening silence; the others accepted by ear.

## Boundaries

- **Two independent layers, never one label.** Overlap (speech+music) is the norm — a single-winner label was tried and rejected.
- **Rejected: inaSpeechSegmenter** — single-label, level-sensitive (quiet music → silence), fragments on pauses, and an install-fragility sink (numpy2/TF/Keras version surgery). Not in the analysis path.
- The −50 dBFS floor and smoothing windows are global; re-check on very different material, don't tune per clip.
- **Rendering gotcha:** ffmpeg `drawbox`/`overlay` time-expressions (`t`,`n`) were unreliable in this ffmpeg build on looped-image input — draw moving playheads per-frame in PIL and stream raw frames; verify positions by frame-number, not exact hashing (libx264 is lossy).
- Evidence and reference implementation: `research/audio-intelligence/`.
