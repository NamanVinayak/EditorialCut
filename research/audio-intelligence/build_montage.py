#!/usr/bin/env python3
"""Visual beat proof: cut a random-image montage on beat_this's detected beats.

For an excerpt window of a track, each detected beat triggers a hard cut to the
next image; each downbeat adds a brief white flash. If the cuts ride the music,
detection is good. Usage: python build_montage.py <track_stem> <start> <end> [img_offset]
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
IMAGES = sorted((HERE / "images").glob("*.jpg"))
OUT = HERE / "beat-proof"
OUT.mkdir(exist_ok=True)
MEDIA = HERE / "benchmark-media"


def build(stem, start, end, img_offset=0, mode="beats"):
    """mode='beats' cuts on every beat (flashes mark downbeats);
    mode='downbeats' cuts only on the strong 'big beats' an editor would cut on."""
    bm = json.load(open(HERE / "beatmaps" / f"{stem}.beats.json"))
    dur = end - start
    cuts = [b for b in bm[mode] if start < b < end]  # bm['beats'] or bm['downbeats']
    downs = [d - start for d in bm["downbeats"] if start < d < end]  # relative to window
    # Segment boundaries: window start -> each cut -> window end
    bounds = [start] + cuts + [end]
    segs = [(bounds[i + 1] - bounds[i]) for i in range(len(bounds) - 1)]
    n = len(segs)

    # concat list, cycling the image pool so consecutive frames always differ
    concat = HERE / f"_concat_{stem}.txt"
    lines = []
    for i, d in enumerate(segs):
        img = IMAGES[(i + img_offset) % len(IMAGES)]
        lines.append(f"file '{img.resolve()}'")
        lines.append(f"duration {d:.4f}")
    lines.append(f"file '{IMAGES[(n - 1 + img_offset) % len(IMAGES)].resolve()}'")  # concat tail quirk
    concat.write_text("\n".join(lines) + "\n")

    silent = OUT / f"_{stem}_silent.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-vf", "fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,"
               "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-r", "30", "-c:v", "libx264", "-preset", "veryfast", str(silent),
    ], check=True, capture_output=True)

    # in beats mode, flash the downbeats so they're distinguishable; in downbeats mode
    # every cut IS a downbeat, so no flash is needed.
    enable = ("+".join(f"between(t,{d:.3f},{d + 0.06:.3f})" for d in downs) or "0") if mode == "beats" else "0"
    out = OUT / f"{stem}_{'beatcut' if mode == 'beats' else 'downbeatcut'}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(silent),
        "-ss", str(start), "-t", str(dur), "-i", str(MEDIA / f"{stem}.wav"),
        "-filter_complex",
        f"[0:v]drawbox=x=0:y=0:w=iw:h=ih:color=white@0.33:t=fill:enable='{enable}'[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(out),
    ], check=True, capture_output=True)
    silent.unlink(); concat.unlink()
    print(f"{stem} [{mode}]: {len(cuts)} cuts over {dur:.0f}s (~1 per {dur/max(len(cuts),1):.1f}s) -> {out.name}")


if __name__ == "__main__":
    stem, start, end = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    off = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    mode = sys.argv[5] if len(sys.argv) > 5 else "beats"
    build(stem, start, end, off, mode)
