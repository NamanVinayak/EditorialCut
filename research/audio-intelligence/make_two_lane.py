#!/usr/bin/env python3
"""Render a combined speech/music STATE timeline (music-only / speech+music / speech-only /
silence) with the mix waveform, then a review video with the original audio, a moving red
playhead, and a live 'NOW: <state>' caption. Usage: python make_two_lane.py <clip_stem> ..."""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).parent
OUT = HERE / "beat-proof"
OUT.mkdir(exist_ok=True)
DUR = 60.0

COL = {"silence": "#9aa0a6", "music": "#3aa0ff", "speech": "#2ecc71", "both": "#9b59b6"}
COL_RGB = {"silence": (154, 160, 166), "music": (58, 160, 255), "speech": (46, 204, 113), "both": (155, 89, 182)}
NAME = {"silence": "SILENCE", "music": "MUSIC ONLY", "speech": "SPEECH ONLY", "both": "SPEECH + MUSIC"}


def state_at(t, music, speech):
    m = any(s <= t < e for s, e in music)
    sp = any(s <= t < e for s, e in speech)
    return "both" if (m and sp) else "music" if m else "speech" if sp else "silence"


def combined_segments(music, speech, dur, step=0.02):
    segs, t, cur, start = [], 0.0, state_at(0, music, speech), 0.0
    while t <= dur:
        st = state_at(t, music, speech)
        if st != cur:
            segs.append((start, t, cur)); cur, start = st, t
        t = round(t + step, 3)
    segs.append((start, dur, cur))
    return segs


def strip(stem):
    layers = json.load(open(HERE / "layermaps" / f"{stem}.layers.json"))
    music, speech = layers["music"], layers["speech"]
    mix = HERE / "benchmark-media" / f"{stem}.wav"
    sig, sr = sf.read(str(mix))
    if sig.ndim > 1:
        sig = sig.mean(axis=1)
    st = max(1, len(sig) // 4000)
    t = np.arange(0, len(sig), st) / sr
    w = sig[::st] / (np.abs(sig).max() + 1e-9)

    fig = plt.figure(figsize=(16, 3.6), dpi=100)  # 1600x360
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, DUR); ax.set_ylim(0, 1); ax.axis("off")
    # header band (top ~0.82-1.0) reserved for the live caption drawn per-frame
    ax.axhline(0.82, color="#000", lw=0.5, alpha=0.15)
    # STATE bar (0.50-0.79)
    for s, e, lab in combined_segments(music, speech, DUR):
        ax.axvspan(s, e, ymin=0.50, ymax=0.79, color=COL[lab], alpha=0.92, lw=0)
        if e - s >= 2.2:
            ax.text((s + e) / 2, 0.645, NAME[lab], ha="center", va="center",
                    fontsize=8.5, weight="bold", color="white")
    # mix waveform (0.20-0.46 band, centered ~0.33)
    ax.plot(t, 0.33 + w * 0.13, color="#222", lw=0.4, alpha=0.6)
    # legend swatches + time ticks (bottom)
    for i, lab in enumerate(["music", "both", "speech", "silence"]):
        lx = 2 + i * 15
        ax.add_patch(Rectangle((lx, 0.04), 1.1, 0.06, color=COL[lab], lw=0))
        ax.text(lx + 1.6, 0.07, NAME[lab], ha="left", va="center", fontsize=8, color="#333")
    for s in range(0, int(DUR) + 1, 5):
        ax.axvline(s, ymin=0.5, ymax=0.79, color="#000", lw=0.3, alpha=0.12)
        ax.text(s, 0.16, f"{s}s", ha="center", va="bottom", fontsize=7, color="#555")
    png = HERE / f"_lane_{stem}.png"
    fig.savefig(png); plt.close(fig)
    return png, mix, music, speech


def build(stem, fps=30):
    png, mix, music, speech = strip(stem)
    out = OUT / f"{stem}-layers.mp4"
    base = Image.open(png).convert("RGB")
    W, H = base.size
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
    except Exception:
        font = ImageFont.load_default()
    hdr = int(0.18 * H)  # header height in px (matches the reserved top band)
    n = int(DUR * fps)
    proc = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
        "-i", "pipe:0", "-i", str(mix), "-map", "0:v", "-map", "1:a", "-t", str(DUR),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(out),
    ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for i in range(n):
        ct = i / fps
        stt = state_at(ct, music, speech)
        x = int(i / (n - 1) * (W - 1))
        fr = base.copy()
        d = ImageDraw.Draw(fr, "RGBA")
        if x > 0:
            d.rectangle([0, hdr, x, H], fill=(0, 0, 0, 40))                 # dim played region (below header)
        d.rectangle([max(0, x - 3), 0, min(W - 1, x + 3), H], fill=(230, 0, 0, 255))  # playhead
        cap = f"NOW: {NAME[stt]}"
        tb = d.textbbox((0, 0), cap, font=font)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        d.rectangle([12, 8, 12 + tw + 24, 8 + th + 16], fill=(*COL_RGB[stt], 245))
        d.text((24, 14), cap, fill="white", font=font)
        proc.stdin.write(fr.tobytes())
    proc.stdin.close(); proc.wait()
    png.unlink()
    print(f"{stem} -> {out.name}")


if __name__ == "__main__":
    for s in (sys.argv[1:] or ["vlog-1min"]):
        build(s)
