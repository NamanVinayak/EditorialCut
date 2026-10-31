#!/usr/bin/env python3
"""Verify Job C treatments on the MUSIC stem alone (no voice) by band energy.

Expect, vs A: B down broadband during speech; C down in the vocal band (700-2k) but not
lows/highs during speech; both ≈ A during a music-only stretch (gating works).

Usage: python verify_ducking.py [stem_name]
"""
import json
import re
import subprocess
import sys
from pathlib import Path
import numpy as np
import soundfile as sf

HERE = Path(__file__).parent
STEM = sys.argv[1] if len(sys.argv) > 1 else "vlog-1min"
MUSIC = HERE / "separated" / "htdemucs" / STEM / "no_vocals.wav"
CARVE = "equalizer=f=1350:width_type=o:width=1.5:g=-6"


def mean_vol(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[0-9.]+) dB", out).group(1))


speech = json.load(open(HERE / "layermaps" / f"{STEM}.layers.json"))["speech"]
enable = "+".join(f"between(t,{s},{e})" for s, e in speech)
mg = 10 ** (((mean_vol(HERE/'separated/htdemucs'/STEM/'vocals.wav') - 6) - mean_vol(MUSIC)) / 20)
duck = 10 ** (-12 / 20)
filt = {
    "A": f"volume={mg:.4f}",
    "B": f"volume={mg:.4f},volume=volume={duck:.4f}:enable='{enable}'",
    "C": f"volume={mg:.4f},{CARVE}:enable='{enable}'",
}
for name, f in filt.items():
    subprocess.run(["ffmpeg", "-y", "-i", str(MUSIC), "-af", f, "-t", "60", str(HERE/f"_mus_{name}.wav")],
                   check=True, capture_output=True)


def band_db(name, t0, t1, lo, hi):
    sig, sr = sf.read(str(HERE / f"_mus_{name}.wav"))
    if sig.ndim > 1:
        sig = sig.mean(axis=1)
    seg = sig[int(t0 * sr):int(t1 * sr)] * np.hanning(int((t1 - t0) * sr))
    F = np.abs(np.fft.rfft(seg)) ** 2
    fr = np.fft.rfftfreq(len(seg), 1 / sr)
    return 10 * np.log10(F[(fr >= lo) & (fr < hi)].sum() + 1e-9)


print(f"{'':10} {'low 100-400':>12} {'VOCAL 700-2k':>13} {'high 4-8k':>11}")
print("SPEECH window (t=44-49s), dB relative to A:")
for n in "ABC":
    lo = band_db(n, 44, 49, 100, 400); vo = band_db(n, 44, 49, 700, 2000); hi = band_db(n, 44, 49, 4000, 8000)
    a_lo = band_db("A", 44, 49, 100, 400); a_vo = band_db("A", 44, 49, 700, 2000); a_hi = band_db("A", 44, 49, 4000, 8000)
    print(f"  {n:8} {lo-a_lo:>+11.1f} {vo-a_vo:>+12.1f} {hi-a_hi:>+10.1f}")
print("MUSIC-ONLY window (t=25-30s), dB relative to A (should be ~0 for all = no treatment):")
for n in "ABC":
    vo = band_db(n, 25, 30, 700, 2000); a_vo = band_db("A", 25, 30, 700, 2000)
    print(f"  {n:8} vocal-band {vo-a_vo:>+.1f}")

for n in "ABC":
    (HERE / f"_mus_{n}.wav").unlink()
