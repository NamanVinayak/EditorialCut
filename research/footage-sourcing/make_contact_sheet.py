"""Build a labeled contact sheet from the Step A manifest so a human (and the
director) can eyeball what Pexels actually returned. One row per beat, one
thumbnail per downloaded clip, labeled with raw rank + tag slug.

Optionally overlays CLIP scores/ordering if out/ranking.json exists (Step B).
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
CELL_W, CELL_H = 480, 270
PAD, LABEL_H, HEADER_W = 8, 46, 210


def font(size: int):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main() -> None:
    manifest = json.loads((ROOT / "out" / "manifest.json").read_text())
    ranking = {}
    rank_path = ROOT / "out" / "ranking.json"
    if rank_path.exists():
        ranking = {b["id"]: b for b in json.loads(rank_path.read_text())}

    max_clips = max(len(b["clips"]) for b in manifest)
    cols = max_clips
    rows = len(manifest)
    W = HEADER_W + cols * (CELL_W + PAD) + PAD
    H = PAD + rows * (CELL_H + LABEL_H + PAD)
    sheet = Image.new("RGB", (W, H), (18, 18, 22))
    draw = ImageDraw.Draw(sheet)
    f_head, f_lab, f_small = font(20), font(15), font(13)

    for r, beat in enumerate(manifest):
        y0 = PAD + r * (CELL_H + LABEL_H + PAD)
        # row header
        for i, ln in enumerate(wrap(draw, beat["query"], f_head, HEADER_W - 12)):
            draw.text((6, y0 + 8 + i * 24), ln, font=f_head, fill=(240, 220, 120))
        draw.text((6, y0 + CELL_H - 20), beat["id"], font=f_small, fill=(140, 140, 150))

        rank_info = ranking.get(beat["id"], {})
        clip_scores = {c["source_id"]: c for c in rank_info.get("clips", [])}

        for c, clip in enumerate(beat["clips"]):
            x0 = HEADER_W + c * (CELL_W + PAD) + PAD
            frame = clip.get("frame_file")
            if frame and (ROOT / frame).exists():
                thumb = Image.open(ROOT / frame).convert("RGB").resize((CELL_W, CELL_H))
                sheet.paste(thumb, (x0, y0))
            else:
                draw.rectangle([x0, y0, x0 + CELL_W, y0 + CELL_H], fill=(40, 40, 40))

            # raw rank badge (top-left)
            draw.rectangle([x0, y0, x0 + 34, y0 + 22], fill=(0, 0, 0))
            draw.text((x0 + 5, y0 + 3), f"#{clip['raw_rank']}", font=f_lab, fill=(255, 255, 255))

            # CLIP score badge (top-right) if available
            sc = clip_scores.get(clip["source_id"])
            if sc:
                txt = f"CLIP {sc['clip_rank']}  {sc['score']:.2f}"
                w = draw.textlength(txt, font=f_lab) + 10
                color = (60, 200, 120) if sc["clip_rank"] == 0 else (0, 0, 0)
                draw.rectangle([x0 + CELL_W - w, y0, x0 + CELL_W, y0 + 22], fill=color)
                draw.text((x0 + CELL_W - w + 5, y0 + 3), txt, font=f_lab, fill=(255, 255, 255))

            # tag label under the cell
            ly = y0 + CELL_H + 2
            for i, ln in enumerate(wrap(draw, clip["source_tags"], f_small, CELL_W)[:2]):
                draw.text((x0 + 2, ly + i * 16), ln, font=f_small, fill=(200, 200, 210))

    out = ROOT / "out" / "contact_sheet.jpg"
    sheet.save(out, quality=88)
    print(f"contact sheet -> {out}  ({W}x{H})")


if __name__ == "__main__":
    main()
