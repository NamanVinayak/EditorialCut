#!/usr/bin/env python3
"""Job C: dialogue-aware music treatment — CONSTRUCTED MIX.

Build a clean mix from Demucs-separated stems + a royalty-free music bed, then
produce ducked and EQ-carved comparison variants gated to speech regions.

Usage: python make_ducking.py <stem> [music_track.wav] [background_video.mp4]

  <stem>               Stem name under separated/htdemucs/<stem>/
  [music_track.wav]    Path to a music bed (default: benchmark-media/music-medium-hiphop.wav)
  [background_video.mp4]  Silent background, 1920×1080, 30 fps (default: first *.mp4 in cwd)

Output: job-c/ with A-flat (untreated), B-duck (broad duck), C-carve (EQ notch)
comparison videos.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
STEM = sys.argv[1] if len(sys.argv) > 1 else "vlog-1min"
VOICE = HERE / "separated" / "htdemucs" / STEM / "vocals.wav"      # clean voice, no music
MUSIC_SRC = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "benchmark-media" / "music-medium-hiphop.wav"
OUT = HERE / "job-c"; OUT.mkdir(exist_ok=True)

CARVE = "equalizer=f=1350:width_type=o:width=1.5:g=-6"   # male-vocal notch
DUCK_DB = -12
MUSIC_BELOW_VOICE_DB = 3   # constant bed sits just under the voice so it genuinely competes


def mean_vol(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[0-9.]+) dB", out).group(1))


def main():
    speech = json.load(open(HERE / "layermaps" / f"{STEM}.layers.json"))["speech"]
    enable = "+".join(f"between(t,{s},{e})" for s, e in speech)

    # fresh 60s constant bed (skip the track's intro for a steady groove)
    bed = OUT / "_bed.wav"
    subprocess.run(["ffmpeg", "-y", "-ss", "10", "-t", "60", "-i", str(MUSIC_SRC),
                    "-ac", "2", "-ar", "44100", str(bed)], check=True, capture_output=True)

    vmean, mmean = mean_vol(VOICE), mean_vol(bed)
    gain_db = (vmean - MUSIC_BELOW_VOICE_DB) - mmean
    mg = 10 ** (gain_db / 20)
    print(f"voice {vmean:.1f} dB, bed {mmean:.1f} dB -> bed set {gain_db:+.1f} dB; speech gated at {enable}")

    def mfilt(duck_db=None, carve=False):
        parts = [f"[1:a]volume={mg:.4f}"]
        if duck_db is not None:
            parts.append(f"volume=volume={10 ** (duck_db / 20):.4f}:enable='{enable}'")
        if carve:
            parts.append(f"{CARVE}:enable='{enable}'")
        return ",".join(parts) + "[m]"

    # Background video: third CLI arg, or first .mp4 in the working directory.
    bg_video = Path(sys.argv[3]) if len(sys.argv) > 3 else next(Path.cwd().glob("*.mp4"))
    vid = OUT / "_video.mp4"
    subprocess.run(["ffmpeg", "-y", "-ss", "0", "-t", "60", "-i", str(bg_video), "-an",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(vid)],
                   check=True, capture_output=True)

    versions = {
        "B-duck12":     mfilt(duck_db=-12),           # pure broad duck
        "C-carve":      mfilt(carve=True),            # pure video-13 carve
        "Cplus-duck6":  mfilt(duck_db=-6, carve=True),   # carve + gentle 6 dB duck
        "Cplus-duck10": mfilt(duck_db=-10, carve=True),  # carve + stronger 10 dB duck
    }
    for name, mfilt in versions.items():
        a = OUT / f"_a_{name}.wav"
        fc = f"{mfilt};[0:a][m]amix=inputs=2:normalize=0,alimiter=limit=0.98[out]"
        subprocess.run(["ffmpeg", "-y", "-i", str(VOICE), "-i", str(bed), "-filter_complex", fc,
                        "-map", "[out]", "-t", "60", str(a)], check=True, capture_output=True)
        out = OUT / f"jobc-{name}.mp4"
        subprocess.run(["ffmpeg", "-y", "-i", str(vid), "-i", str(a), "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", "60", str(out)],
                       check=True, capture_output=True)
        print(f"  {name} -> {out.name}")
    vid.unlink(); bed.unlink()


if __name__ == "__main__":
    main()
