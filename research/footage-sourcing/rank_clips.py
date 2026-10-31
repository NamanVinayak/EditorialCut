"""Step B — semantic re-ranking with CLIP.

For each beat, embed the rich clip_description (text) and each downloaded
clip's representative frame (image), then score by cosine similarity. This
tests whether CLIP can (a) push the best-matching clip to the top even when
Pexels' keyword order didn't, and (b) SIGNAL when nothing fits (low top score),
which is itself a decision input: real footage may be the wrong source for
that beat.

Run from sandbox root:
    .venv/bin/python rank_clips.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from vendored import clip_embedder  # noqa: E402


def main() -> None:
    beats_meta = {b["id"]: b for b in json.loads((ROOT / "beats.json").read_text())["beats"]}
    manifest = json.loads((ROOT / "out" / "manifest.json").read_text())
    print("model:", clip_embedder.model_info())

    out = []
    summary_rows = []
    for beat in manifest:
        clips = [c for c in beat["clips"] if c.get("frame_file")]
        if not clips:
            continue
        desc = beats_meta[beat["id"]]["clip_description"]
        frame_paths = [ROOT / c["frame_file"] for c in clips]

        txt = clip_embedder.embed_texts([desc])[0]          # (512,)
        imgs = clip_embedder.embed_images(frame_paths)       # (N, 512)
        scores = imgs @ txt                                  # cosine (normalized)

        order = np.argsort(-scores)                          # best first
        ranked = []
        for clip_rank, idx in enumerate(order):
            c = clips[idx]
            ranked.append({
                "clip_rank": clip_rank,
                "raw_rank": c["raw_rank"],
                "source_id": c["source_id"],
                "score": round(float(scores[idx]), 4),
                "source_tags": c["source_tags"],
                "frame_file": c["frame_file"],
            })
        out.append({"id": beat["id"], "query": beat["query"],
                    "clip_description": desc, "clips": ranked})

        top = ranked[0]
        moved = "YES" if top["raw_rank"] != 0 else "no"
        summary_rows.append((beat["id"], top["score"], float(np.mean(scores)),
                             top["raw_rank"], moved, top["source_tags"][:42]))

    (ROOT / "out" / "ranking.json").write_text(json.dumps(out, indent=2))

    print(f"\n{'beat':22} {'top':>6} {'mean':>6} {'rawRk':>5} {'moved?':>6}  top-clip tag")
    print("-" * 92)
    for bid, top, mean, rawrk, moved, tag in summary_rows:
        print(f"{bid:22} {top:6.3f} {mean:6.3f} {rawrk:5d} {moved:>6}  {tag}")
    print("\nHigher 'top' = CLIP found a strong visual match. Low 'top' across a beat"
          "\n= nothing fits well → consider AI-generated footage for that beat.")


if __name__ == "__main__":
    main()
