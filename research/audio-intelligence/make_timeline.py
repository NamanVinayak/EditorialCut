#!/usr/bin/env python3
"""Render a speech/music/silence timeline strip PNG from a segments JSON (full-bleed so a
playhead maps linearly to time). Usage: python make_timeline.py <segments.json> <audio.wav>"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
COL = {"speech": "#2ecc71", "music": "#3aa0ff", "silence": "#9aa0a6", "noise": "#e67e22"}
DUR = 60.0


def main(seg_json, audio):
    data = json.load(open(seg_json))
    regions = data["regions"]
    sig, sr = sf.read(str(audio))
    if sig.ndim > 1:
        sig = sig.mean(axis=1)
    t = np.arange(len(sig)) / sr
    sig = sig / (np.abs(sig).max() + 1e-9)

    fig = plt.figure(figsize=(16, 3), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])  # full-bleed: x in [0,DUR] maps to [0,width]
    ax.set_xlim(0, DUR); ax.set_ylim(-1.15, 1.15); ax.axis("off")

    for r in regions:
        ax.axvspan(r["start"], r["end"], color=COL.get(r["label"], "#555"), alpha=0.45, lw=0)
    ax.plot(t, sig * 0.9, color="#111", lw=0.35, alpha=0.55)
    for r in regions:
        if r["end"] - r["start"] >= 1.2:
            ax.text((r["start"] + r["end"]) / 2, 1.02, r["label"].upper(), ha="center",
                    va="bottom", fontsize=9, weight="bold", color=COL.get(r["label"], "#555"))
    for s in range(0, int(DUR) + 1, 5):
        ax.axvline(s, color="#000", lw=0.4, alpha=0.15)
        ax.text(s, -1.1, f"{s}s", ha="center", va="bottom", fontsize=7, color="#444")

    out = HERE / "timeline_strip.png"
    fig.savefig(out)
    print("wrote", out)


if __name__ == "__main__":
    seg = sys.argv[1] if len(sys.argv) > 1 else HERE / "segmaps/vlog-1min.segments.json"
    aud = sys.argv[2] if len(sys.argv) > 2 else HERE / "benchmark-media/vlog-1min.wav"
    main(seg, aud)
