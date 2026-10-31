---
title: Dialogue-Aware Music Ducking / EQ Carving
aliases:
  - Vocal Ducking
  - Frequency Carving
  - Music Under Speech
type: capability
status: accepted-v1
updated: 2026-07-15
---

# Dialogue-Aware Music Ducking / EQ Carving

## Decision

**Accepted for v1. Move on.** Keep a music bed from burying the voice the professional way: a **source reference frequency carve + a gentle broad duck, both gated to the speech regions from Job B**. the project lead compared pure-duck, pure-carve, and two carve+duck combos on a clean test and chose **carve + a −6 dB duck**. The duck depth stays a taste dial.

Grounded in the reference private derivation evidence (not distributed) ("just lowering the music volume is not professional editing; carve a notch where the vocals sit").

## Editorial purpose

During speech, make room for the voice in the music — not by dulling the whole track, but by scooping the vocal frequency band out of the music (so bass and highs stay full) and stepping the music down a little. During music-only stretches the music plays untouched.

## Accepted method & settings

Applied to the **separated music stem** (from Job B's Demucs split), **only during speech** (gated by Job B's speech intervals):

- **Frequency carve** — parametric EQ notch in the vocal band. Male/general voice: `equalizer=f=1350:width_type=o:width=1.5:g=-6` (700 Hz–2 kHz band). Female voice: center ~2500 Hz (1–4 kHz), per source reference.
- **Gentle broad duck** — `−6 dB` volume reduction (the accepted taste; a dial — more for punchy vlogs, less for calm).
- Re-mix voice + treated music (`amix normalize=0`, `alimiter` to catch peaks).
- ffmpeg gating: `...:enable='between(t,s0,e0)+between(t,s1,e1)+…'`. Audio-filter timeline `enable` works reliably (unlike the video drawbox geometry expressions — see speech-music-segmentation limits).

Reuses the **Demucs vocal/music separation** built for Job B — no new heavy tooling.

## The testing lesson (the important part)

**You cannot test ducking on a source whose music was already ducked by the editor.** the project lead's vlogs have the music keyframed down under his voice in Final Cut — that automation is baked into the separated music stem, so an "untreated" A version already ducks, and A/B/C become indistinguishable. It is impossible to tell if the treatment is working.

**Fix — test on a constructed mix:** clean **voice stem** (Demucs already stripped the music) + a **fresh royalty-free music track at a constant, un-ducked level**, deliberately set to compete (here ~3 dB under the voice). Now the "flat" A version genuinely does not duck, so every improvement in B/C is 100% attributable to the treatment. This is the only honest way to evaluate this capability.

## Confirmed evidence

vlog1 constructed mix (clean voice stem + constant lo-fi bed), treatment gated to speech (6.7–17.4s, 40.2–60s). Spectral verification on the music stem:

| Version | Lows 100–400 | Vocal 700–2k | Highs 4–8k | During music-only |
| --- | ---: | ---: | ---: | --- |
| B duck −12 | −12 dB | −12 dB | −12 dB | untouched (gated) |
| C carve | −0.3 dB | −4 dB | −0.5 dB | untouched (gated) |
| **Cplus (accepted)** | small | notch + duck | small | untouched (gated) |

Carve reduces the vocal band only; duck lowers broadband; both apply only while speaking. Accepted by ear: **carve + −6 dB duck**.

## Human-observed limits

1. **Vocal band is voice-type dependent** — male ~1350 Hz center, female ~2500 Hz (source reference). Pick per speaker; inaSpeechSegmenter can detect gender if needed.
2. **The −6 dB duck depth is the project lead's taste on one clip.** It is a dial, validate per material.
3. **Separation artifacts and boundary precision (±1–2 s)** carry over from the Job-B separation.
4. **When the creator's voice and music are already separate assets** (not a pre-mixed export), skip separation and treat the music track directly.

## Reference implementation

[`research/audio-intelligence/make_ducking.py`](../../research/audio-intelligence/make_ducking.py) (build A/B/C/combos on a constructed mix) and [`verify_ducking.py`](../../research/audio-intelligence/verify_ducking.py) (spectral band-energy check). Skill: [`skills/duck-music-under-speech/SKILL.md`](../../skills/duck-music-under-speech/SKILL.md).

## Operating rule

Confirm the clip and its intended use with the project lead. Always evaluate on a constructed mix (clean voice + constant bed), never on editor-pre-ducked audio. Keep sources immutable, review by ear, and stop tuning once accepted — the duck depth remains an editorial dial.
