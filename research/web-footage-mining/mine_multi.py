"""Multi-opportunity mining — the real-world test.

Download ONE corpus of source videos, sample+embed frames ONCE, then hunt many
b-roll opportunities against the shared embeddings (efficient: download+embed
once, locate many moments). Mirrors real use: pull the relevant videos for a
topic, then find every moment the edit needs inside them.

Reuses mine.py's building blocks. Opportunities are defined inline (the director
step). Run:
  .venv/bin/python mine_multi.py --out out/run1
"""
from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import mine  # reuse download_proxy, sample_frames, embed_frames, query_vector, group_moments

ROOT = Path(__file__).resolve().parent

# Corpus: multi-scene compilations of the benchmark series (rich, multi-scene =
# buried-moment test). Supply your own YouTube video IDs before running.
CORPUS = ["<video-id-1>", "<video-id-2>", "<video-id-3>", "<video-id-4>", "<video-id-5>"]

# B-roll opportunities from the talking-head's structure (his-video timecode → scene → CLIP query).
OPPS = [
    {"id": "o1_hero",        "tc": "~15-30s S1/S2", "scene": "protagonist as the hero agent",
     "query": "a confident middle-aged Indian man, serious spy thriller hero, close up"},
    {"id": "o2_hospital",    "tc": "~58-68s S2 b09", "scene": "hospital / artificial stakes",
     "query": "a person in a hospital bed in a hospital ward, patient, medical scene"},
    {"id": "o3_action",      "tc": "~103s S3",       "scene": "action / fight (protagonist vs attacker)",
     "query": "an intense action fight scene, two men fighting, thriller violence"},
    {"id": "o4_family",      "tc": "~116-131s S3",   "scene": "family in danger / kids escape",
     "query": "a worried family with children in danger, tense domestic scene indoors"},
    {"id": "o5_onrun",       "tc": "~131s cascade",  "scene": "on the run / chase",
     "query": "a man running and fleeing through streets at night, chase"},
    {"id": "o6_marriage",    "tc": "~120s cascade",  "scene": "marriage / emotional tension",
     "query": "a tense emotional confrontation between a husband and wife at home"},
    {"id": "o7_villain",     "tc": "~S2/S5",         "scene": "antagonist close-up",
     "query": "a menacing intense villain man staring, dramatic dark thriller antagonist"},
    {"id": "o8_standoff",    "tc": "~194-230s S5",   "scene": "protagonist vs rival confrontation",
     "query": "two men in a tense face to face standoff confrontation"},
]

FPS, PAD, TOPK = 0.5, 1.5, 4


def font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc"):
        if Path(p).exists():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def combined_sheet(results, meta, out):
    CW, CH, HDR = 300, 169, 250
    rows, cols = len(results), TOPK
    sheet = Image.new("RGB", (HDR + cols * (CW + 4), rows * (CH + 34)), (16, 16, 20))
    d = ImageDraw.Draw(sheet)
    fh, fs = font(15), font(12)
    for r, res in enumerate(results):
        y = r * (CH + 34)
        for i, ln in enumerate(mine_wrap(d, res["scene"], fh, HDR - 12)):
            d.text((6, y + 8 + i * 20), ln, font=fh, fill=(240, 210, 120))
        d.text((6, y + CH - 26), res["tc"], font=fs, fill=(140, 140, 150))
        d.text((6, y + CH - 10), res["id"], font=fs, fill=(110, 110, 120))
        for c, m in enumerate(res["moments"][:cols]):
            x = HDR + c * (CW + 4)
            fp = Path(m["peak_frame"])
            if fp.exists():
                sheet.paste(Image.open(fp).convert("RGB").resize((CW, CH)), (x, y))
            d.rectangle([x, y, x + 40, y + 17], fill=(0, 0, 0))
            d.text((x + 3, y + 2), f"{m['peak_score']:.2f}", font=fs, fill=(80, 230, 140))
            d.text((x + 2, y + CH + 2), meta[m["video_id"]]["title"][:34], font=fs, fill=(200, 200, 210))
            d.text((x + 2, y + CH + 18), f"{m['peak_t']:.0f}s", font=fs, fill=(150, 150, 160))
    sheet.save(out, quality=88)


def mine_wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out/run1")
    ap.add_argument("--res", type=int, default=480)
    a = ap.parse_args()
    out = ROOT / a.out
    (out / "proxies").mkdir(parents=True, exist_ok=True)

    print(f"downloading {len(CORPUS)} proxies @ {a.res}p ...")
    with ThreadPoolExecutor(max_workers=4) as ex:
        metas = [m for m in ex.map(lambda v: mine.download_proxy(v, out / "proxies", a.res), CORPUS) if m]
    meta = {m["id"]: m for m in metas}
    print(f"  {len(metas)} downloaded")

    # sample + embed ONCE
    all_frames = []  # (video_id, t, path)
    embs = []
    for m in metas:
        frames = mine.sample_frames(Path(m["path"]), out / "frames" / m["id"], FPS)
        if not frames:
            continue
        e = mine.embed_frames([f for _, f in frames])
        for (t, f), row in zip(frames, e):
            all_frames.append((m["id"], float(t), str(f)))
        embs.append(e)
        print(f"  {m['id']}: {len(frames)} frames  {m['title'][:44]}")
    E = np.vstack(embs)

    results = []
    for o in OPPS:
        qv = mine.query_vector(o["query"], None)
        sims = E @ qv
        scored = [{"video_id": vid, "t": t, "score": float(s), "frame": fr}
                  for (vid, t, fr), s in zip(all_frames, sims)]
        moments = mine.group_moments(scored, PAD, TOPK)
        for mo in moments:
            mo["url"], mo["title"] = meta[mo["video_id"]]["url"], meta[mo["video_id"]]["title"]
        results.append({**o, "moments": moments})
        top = moments[0] if moments else {}
        print(f"  {o['id']:12} top={top.get('peak_score',0):.3f}  {top.get('url','')}?t={int(top.get('peak_t',0))}  {o['scene']}")

    (out / "opportunities.json").write_text(json.dumps(results, indent=2))
    combined_sheet(results, meta, out / "opportunities.jpg")
    print(f"\n{len(results)} opportunities -> {out/'opportunities.json'} + opportunities.jpg")


if __name__ == "__main__":
    main()
