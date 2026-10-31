"""Shelf 1 sharpening pass — one round only.

The two weak beats failed partly on lazy queries. The query-construction guide
guidance says: lead with the subject, 2-4 keywords, add a POV/quality keyword,
try synonyms. Re-run ONLY the two weak beats with better queries and compare
against the original, so we can tell what's fixable at the query layer vs a
true stock gap (→ generate).

Run from sandbox root:
    .venv/bin/python sharpen.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from vendored import clip_embedder  # noqa: E402
from vendored.base import SearchFilters  # noqa: E402
from vendored.pexels import PexelsSource  # noqa: E402

from source_clips import load_env, extract_frame  # noqa: E402

PER_VARIANT = 4

# beat_id -> clip_description (for CLIP scoring) + query variants (first = original baseline)
TRIALS = {
    "b1_on_the_run": {
        "desc": "a person running anxiously through a crowded city street, chased, on the run, urgent handheld",
        "queries": [
            "man running crowded city street",          # original (baseline)
            "man running away scared",                  # subject + emotion
            "person running night alley handheld",      # + POV keyword
        ],
    },
    "b4_artificial_stakes": {
        "desc": "an urgent hospital emergency corridor with medical staff and monitors, high stakes, life or death",
        "queries": [
            "hospital emergency corridor",              # original (baseline)
            "doctors rushing patient stretcher",        # subject + action
            "emergency room hospital urgent",           # register words
        ],
    },
}


def main() -> None:
    load_env()
    src = PexelsSource()
    filters = SearchFilters(kind="video", orientation="landscape", min_width=1280,
                            min_duration=3.0, max_duration=30.0, per_page=12)
    sharpen_dir = ROOT / "out" / "sharpen"
    sharpen_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for beat_id, spec in TRIALS.items():
        desc = spec["desc"]
        txt = clip_embedder.embed_texts([desc])[0]
        for qi, query in enumerate(spec["queries"]):
            tag = f"{beat_id}__q{qi}"
            qdir = sharpen_dir / tag
            qdir.mkdir(parents=True, exist_ok=True)
            print(f"\n=== {tag} :: '{query}' ===")
            try:
                cands = src.search(query, filters)[:PER_VARIANT]
            except Exception as e:  # noqa: BLE001
                print(f"  search failed: {e}")
                continue
            clips, frames = [], []
            for rank, c in enumerate(cands):
                cp = qdir / f"{rank:02d}_{c.source_id}.mp4"
                fp = qdir / f"{rank:02d}_{c.source_id}.jpg"
                try:
                    src.download(c, cp)
                    if not extract_frame(cp, fp, c.duration):
                        continue
                except Exception:  # noqa: BLE001
                    continue
                clips.append({"raw_rank": rank, "source_id": c.source_id,
                              "tags": c.source_tags, "frame_file": str(fp.relative_to(ROOT))})
                frames.append(fp)
            if not frames:
                continue
            scores = clip_embedder.embed_images(frames) @ txt
            for c, s in zip(clips, scores):
                c["clip_score"] = round(float(s), 4)
            top = float(np.max(scores))
            print(f"  {len(clips)} clips, CLIP top={top:.3f}  tags={[c['tags'][:28] for c in clips]}")
            results.append({"beat_id": beat_id, "query_index": qi, "query": query,
                            "is_baseline": qi == 0, "clip_top": round(top, 4),
                            "clips": clips})

    (sharpen_dir / "sharpen_results.json").write_text(json.dumps(results, indent=2))
    print("\n-> out/sharpen/sharpen_results.json")


if __name__ == "__main__":
    main()
