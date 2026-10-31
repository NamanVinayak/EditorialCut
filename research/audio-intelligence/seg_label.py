#!/usr/bin/env python3
"""Job B: label an audio file into speech / music / silence / noise with inaSpeechSegmenter.

Usage: python seg_label.py <audio.wav>
Writes <name>.segments.json and prints a readable region list.
"""
import os
# inaSpeechSegmenter's CNN is a Keras-2 model; TF 2.16+ defaults to Keras 3. Route to legacy Keras.
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")

import json
import sys
from pathlib import Path

import numpy as np
# --- compat shims for inaSpeechSegmenter 0.7.6 + ancient pyannote-algorithms on a modern stack ---
# 1) numpy.lib.pad was removed (now numpy.pad)
if not hasattr(np.lib, "pad"):
    np.lib.pad = np.pad
# 2) pyannote viterbi passes a generator to np.vstack, which modern numpy rejects; coerce to list
_orig_vstack = np.vstack
def _vstack_coerce(tup, *a, **k):
    if not isinstance(tup, (list, tuple, np.ndarray)):
        tup = list(tup)
    return _orig_vstack(tup, *a, **k)
np.vstack = _vstack_coerce

from inaSpeechSegmenter import Segmenter

HERE = Path(__file__).parent
OUT = HERE / "segmaps"
OUT.mkdir(exist_ok=True)

LABEL_MAP = {"speech": "speech", "music": "music", "noEnergy": "silence", "noise": "noise"}


def main(path):
    path = Path(path)
    seg = Segmenter(vad_engine="smn", detect_gender=False)
    raw = seg(str(path))  # list of (label, start, end)
    regions = [
        {"label": LABEL_MAP.get(lab, lab), "start": round(s, 3), "end": round(e, 3), "dur": round(e - s, 3)}
        for lab, s, e in raw
    ]
    out = OUT / (path.stem + ".segments.json")
    out.write_text(json.dumps({"track": path.name, "regions": regions}, indent=2))
    # readable dump
    print(f"{path.name}: {len(regions)} regions -> {out.name}")
    for r in regions:
        bar = {"speech": "SPEECH", "music": "music ", "silence": "  ·   ", "noise": "noise "}.get(r["label"], r["label"])
        print(f"  {r['start']:6.2f}–{r['end']:6.2f}s  ({r['dur']:5.2f}s)  {bar}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else HERE / "benchmark-media/vlog-1min.wav")
