#!/usr/bin/env python3
"""Job A benchmark: run beat_this on the benchmark tracks, save beat/downbeat maps as JSON.

Usage: python detect_beats.py [track.wav ...]
Defaults to the three music tracks in benchmark-media/.
"""
import json
import sys
import time
from pathlib import Path

from beat_this.inference import File2Beats

HERE = Path(__file__).parent
MEDIA = HERE / "benchmark-media"
OUT = HERE / "beatmaps"
OUT.mkdir(exist_ok=True)

DEFAULT_TRACKS = [
    MEDIA / "music-easy-edm.wav",
    MEDIA / "music-medium-hiphop.wav",
    MEDIA / "music-hard-ambient.wav",
]


def infer_tempo(beats):
    """Median inter-beat interval -> BPM. Robust to a few missed/extra beats."""
    if len(beats) < 2:
        return None
    import statistics
    diffs = [b - a for a, b in zip(beats[:-1], beats[1:])]
    med = statistics.median(diffs)
    return round(60.0 / med, 1) if med > 0 else None


def main(tracks):
    # 'final0' is one of the released checkpoints; dbn=False uses the fast peak-picker.
    f2b = File2Beats(checkpoint_path="final0", device="mps", dbn=False)
    for track in tracks:
        track = Path(track)
        if not track.exists():
            print(f"SKIP (missing): {track}")
            continue
        t0 = time.time()
        beats, downbeats = f2b(str(track))
        dt = time.time() - t0
        beats = [round(float(x), 4) for x in beats]
        downbeats = [round(float(x), 4) for x in downbeats]
        data = {
            "track": track.name,
            "n_beats": len(beats),
            "n_downbeats": len(downbeats),
            "inferred_bpm": infer_tempo(beats),
            "duration_covered": beats[-1] if beats else None,
            "infer_seconds": round(dt, 2),
            "beats": beats,
            "downbeats": downbeats,
        }
        out = OUT / (track.stem + ".beats.json")
        out.write_text(json.dumps(data, indent=2))
        print(
            f"{track.name}: {len(beats)} beats, {len(downbeats)} downbeats, "
            f"~{data['inferred_bpm']} BPM, {dt:.1f}s infer -> {out.name}"
        )


if __name__ == "__main__":
    main(sys.argv[1:] or DEFAULT_TRACKS)
