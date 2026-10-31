"""Step A — footage sourcing benchmark.

Drives the Pexels adapter directly (no framework) to prove the plumbing: for
each test beat, search Pexels video, download the top N
candidates, extract a representative frame, and record a manifest.

Run from the sandbox root:
    .venv/bin/python source_clips.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from vendored.base import SearchFilters  # noqa: E402
from vendored.pexels import PexelsSource  # noqa: E402

PER_BEAT_DOWNLOAD = 6      # how many clips to pull per beat for ranking
SEARCH_PER_PAGE = 15       # how many candidates to ask Pexels for


def load_env() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def extract_frame(clip: Path, out_jpg: Path, duration: float) -> bool:
    """Grab one representative frame ~1/3 into the clip (skips black intros)."""
    ts = max(0.5, duration / 3.0)
    cmd = [
        "ffmpeg", "-nostdin", "-y", "-ss", f"{ts:.2f}", "-i", str(clip),
        "-frames:v", "1", "-vf", "scale=480:-2", str(out_jpg),
    ]
    r = subprocess.run(cmd, capture_output=True)
    return r.returncode == 0 and out_jpg.exists()


def main() -> None:
    load_env()
    if not os.environ.get("PEXELS_API_KEY"):
        sys.exit("PEXELS_API_KEY missing from the environment or local .env")

    beats = json.loads((ROOT / "beats.json").read_text())["beats"]
    src = PexelsSource()
    print(f"Pexels available: {src.is_available()}")

    filters = SearchFilters(
        kind="video", orientation="landscape", min_width=1280,
        min_duration=3.0, max_duration=30.0, per_page=SEARCH_PER_PAGE,
    )

    manifest = []
    for beat in beats:
        bid, query = beat["id"], beat["query"]
        print(f"\n=== {bid} :: '{query}' ===")
        beat_dir = ROOT / "out" / bid
        beat_dir.mkdir(parents=True, exist_ok=True)

        try:
            results = src.search(query, filters)
        except Exception as e:  # noqa: BLE001
            print(f"  SEARCH FAILED: {e}")
            manifest.append({**beat, "error": str(e), "clips": []})
            continue

        print(f"  Pexels returned {len(results)} candidates; downloading top {PER_BEAT_DOWNLOAD}")
        clips = []
        for rank, cand in enumerate(results[:PER_BEAT_DOWNLOAD]):
            stem = f"{rank:02d}_{cand.source_id}"
            clip_path = beat_dir / f"{stem}.mp4"
            frame_path = beat_dir / f"{stem}.jpg"
            try:
                src.download(cand, clip_path)
                ok = extract_frame(clip_path, frame_path, cand.duration)
            except Exception as e:  # noqa: BLE001
                print(f"    [{rank}] download failed: {e}")
                continue
            size_mb = clip_path.stat().st_size / 1e6 if clip_path.exists() else 0
            print(f"    [{rank}] {cand.width}x{cand.height} {cand.duration:.1f}s "
                  f"{size_mb:.1f}MB  tags='{cand.source_tags[:50]}'  frame={'ok' if ok else 'FAIL'}")
            clips.append({
                "raw_rank": rank,
                "source_id": cand.source_id,
                "source_url": cand.source_url,
                "width": cand.width, "height": cand.height,
                "duration": cand.duration,
                "creator": cand.creator,
                "source_tags": cand.source_tags,
                "clip_file": str(clip_path.relative_to(ROOT)),
                "frame_file": str(frame_path.relative_to(ROOT)) if ok else None,
            })
        manifest.append({**beat, "returned": len(results), "clips": clips})

    (ROOT / "out" / "manifest.json").write_text(json.dumps(manifest, indent=2))
    total = sum(len(m["clips"]) for m in manifest)
    print(f"\nDONE. {total} clips across {len(beats)} beats. manifest -> out/manifest.json")


if __name__ == "__main__":
    main()
