---
name: duck-music-under-speech
description: Invoke whenever a music bed is added under dialogue so it never buries the voice — applies the source-reference treatment (frequency-carve a notch in the vocal band + a gentle broad duck) gated to the moments the speaker is talking. Do NOT hand-roll a static volume envelope; it reuses the voice/music separation from speech-music segmentation.
---

# Duck Music Under Speech

## Overview

Keep a music bed out of the voice's way the pro way (per private derivation evidence (not distributed)): during speech, scoop the vocal frequency band out of the music (so bass/highs stay full) AND step the music down a little. During music-only stretches the music is untouched. See [`docs/capabilities/dialogue-aware-ducking.md`](../../docs/capabilities/dialogue-aware-ducking.md).

## Inputs

- Separated **voice stem** + **music stem** (from `skills/segment-speech-music`, same Demucs split), or an already-separate voice track + music track.
- Speech regions (from Job B's layers map) to gate the treatment.
- Speaker voice type (male/female) to pick the carve band.

## Workflow

1. **Gate to speech.** Build `enable='between(t,s0,e0)+between(t,s1,e1)+…'` from the speech regions. Audio-filter timeline `enable` works reliably.
2. **Carve** the music's vocal band (source reference): male/general `equalizer=f=1350:width_type=o:width=1.5:g=-6` (700 Hz–2 kHz); female `f≈2500` (1–4 kHz).
3. **Gentle duck** the music broadband during speech — default **−6 dB** (accepted taste; a dial: more for punchy vlogs, less for calm).
4. **Re-mix** voice + treated music (`amix=inputs=2:normalize=0`, then `alimiter=limit=0.98` for peaks).
5. **Review by ear** — offer pure-duck / pure-carve / carve+duck combos so the creator can pick the depth.

## Accepted envelope

Proven 2026-07-15 on a constructed vlog mix: carve (`f=1350, 1.5 oct, −6 dB`) + **−6 dB broad duck**, gated to speech, was chosen over pure duck and pure carve. Spectrally verified: carve reduces only the vocal band, duck is broadband, both apply only during speech.

## Boundaries

- **Never evaluate on editor-pre-ducked audio.** If the source's music was already keyframed down under the voice (typical of a finished edit), that automation is baked into the separated stem and makes A/B/C indistinguishable. **Test on a constructed mix**: clean voice stem + a fresh music track at a *constant* level (set to compete). Only then is any improvement attributable to the treatment.
- Duck depth and carve band are dials, not fixed constants — pick per speaker and per material.
- Evidence and reference implementation: `research/audio-intelligence/` (`make_ducking.py`, `verify_ducking.py`).
