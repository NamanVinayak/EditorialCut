#!/usr/bin/env python3
"""Job B (v2, universal): two INDEPENDENT layers per clip.
  speech track = silero-VAD on the separated vocal stem (VAD is reliable on isolated voice)
  music  track = energy on the separated music stem (catches quiet continuous beds)
Both smoothed so natural pauses don't fragment a region. Overlap (speech+music) is
represented natively because the two tracks are independent.

Usage: python analyze_layers.py <clip_stem> [clip_stem ...]   (default: the 4 vlogs)
"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import soxr
import torch
from silero_vad import load_silero_vad, get_speech_timestamps

HERE = Path(__file__).parent
SEP = HERE / "separated" / "htdemucs"
OUT = HERE / "layermaps"
OUT.mkdir(exist_ok=True)

MUSIC_FLOOR_DB = -50.0   # on the *separated* music stem; one value for all videos, not per-clip
DEFAULT = ["vlog-1min"]  # pass your own stem names as CLI args to override


def smooth(intervals, merge_gap, min_dur):
    """Merge on-intervals separated by < merge_gap, then drop any shorter than min_dur."""
    if not intervals:
        return []
    intervals = sorted([list(i) for i in intervals])
    merged = [intervals[0]]
    for s, e in intervals[1:]:
        if s - merged[-1][1] <= merge_gap:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [[round(s, 2), round(e, 2)] for s, e in merged if e - s >= min_dur]


def music_track(no_vocals_path):
    sig, sr = sf.read(str(no_vocals_path))
    if sig.ndim > 1:
        sig = sig.mean(axis=1)
    win, hop = int(0.05 * sr), int(0.025 * sr)
    times, mask = [], []
    for i in range(0, len(sig) - win, hop):
        frame = sig[i:i + win]
        rms = np.sqrt(np.mean(frame ** 2)) + 1e-9
        db = 20 * np.log10(rms)
        times.append(i / sr)
        mask.append(db > MUSIC_FLOOR_DB)
    # frames -> on-intervals
    intervals, run_start = [], None
    for t, m in zip(times, mask):
        if m and run_start is None:
            run_start = t
        elif not m and run_start is not None:
            intervals.append((run_start, t)); run_start = None
    if run_start is not None:
        intervals.append((run_start, times[-1]))
    return smooth(intervals, merge_gap=1.5, min_dur=0.5)


def speech_track(vocals_path, vad):
    sig, sr = sf.read(str(vocals_path))
    if sig.ndim > 1:
        sig = sig.mean(axis=1)
    sig16 = soxr.resample(sig, sr, 16000).astype(np.float32)
    wav = torch.from_numpy(sig16)
    ts = get_speech_timestamps(wav, vad, sampling_rate=16000, return_seconds=True,
                               min_silence_duration_ms=600, min_speech_duration_ms=250)
    return smooth([(t["start"], t["end"]) for t in ts], merge_gap=0.8, min_dur=0.25)


def main(stems):
    vad = load_silero_vad()
    for stem in stems:
        d = SEP / stem
        speech = speech_track(d / "vocals.wav", vad)
        music = music_track(d / "no_vocals.wav")
        data = {"clip": stem, "music": music, "speech": speech}
        (OUT / f"{stem}.layers.json").write_text(json.dumps(data, indent=2))
        sm = sum(e - s for s, e in music); ss = sum(e - s for s, e in speech)
        print(f"{stem}: music {len(music)} regions ({sm:.0f}s on), speech {len(speech)} regions ({ss:.0f}s on)")
        for s, e in speech:
            print(f"    speech {s:5.1f}–{e:5.1f}s")


if __name__ == "__main__":
    main(sys.argv[1:] or DEFAULT)
