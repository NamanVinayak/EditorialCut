"""Web footage mining — deterministic core (Shelf 3, steps 2-4).

Given a set of YouTube videos (explicit IDs/URLs, or a search query) and a CLIP
query (text and/or a reference image), this:
  1. downloads each video as a low-res PROXY (parallel),
  2. samples frames at a fixed fps,
  3. CLIP-embeds every frame and ranks against the query,
  4. groups high-scoring frames into candidate MOMENTS (video, in, out),
  5. exports candidates.json + a contact sheet of the top moments.

The LLM steps (deciding the query / reference image, and verifying the top
moments) live OUTSIDE this script — this is the mechanical middle. Run inside a
mining sub-agent so the frames/scores never touch the director's context.

Usage:
  .venv/bin/python mine.py --search "white rock bc pier drone" --n 6 \
      --query "a long wooden pier over the ocean, seaside promenade" --out out/run1
  .venv/bin/python mine.py --videos IDorURL1 IDorURL2 --ref-image ref.jpg --out out/run2
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from vendored import clip_embedder  # noqa: E402


# ----------------------------- yt-dlp helpers -----------------------------

def search_ids(query: str, n: int) -> list[str]:
    r = subprocess.run(
        ["yt-dlp", f"ytsearch{n}:{query}", "--flat-playlist", "--print", "%(id)s"],
        capture_output=True, text=True,
    )
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def download_proxy(video: str, proxy_dir: Path, res: int) -> dict | None:
    vid = video.rsplit("/", 1)[-1].split("=")[-1].split("&")[0]
    out = proxy_dir / f"{vid}.mp4"
    if not out.exists():
        cmd = [
            "yt-dlp", video if "://" in video else f"https://youtu.be/{vid}",
            "-S", f"res:{res}", "-f", "bv*+ba/b", "--merge-output-format", "mp4",
            "--no-playlist", "-o", str(proxy_dir / "%(id)s.%(ext)s"),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not out.exists():
            print(f"  [download FAIL] {vid}: {r.stderr.strip().splitlines()[-1:] }")
            return None
    # probe title + duration
    meta = subprocess.run(
        ["yt-dlp", "--skip-download", "--print", "%(title)s\t%(duration)s",
         f"https://youtu.be/{vid}"], capture_output=True, text=True,
    ).stdout.strip().split("\t")
    title = meta[0] if meta else vid
    return {"id": vid, "path": str(out), "title": title, "url": f"https://youtu.be/{vid}"}


def sample_frames(proxy: Path, frames_dir: Path, fps: float) -> list[tuple[float, Path]]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-i", str(proxy),
         "-vf", f"fps={fps},scale=384:-2", str(frames_dir / "f%05d.jpg")],
        capture_output=True,
    )
    out = []
    for f in sorted(frames_dir.glob("f*.jpg")):
        idx = int(f.stem[1:])
        out.append(((idx - 1) / fps, f))   # ~timestamp of this frame
    return out


# ----------------------------- ranking -----------------------------

def query_vector(text: str | None, ref_image: str | None) -> np.ndarray:
    vecs = []
    if text:
        vecs.append(clip_embedder.embed_texts([text])[0])
    if ref_image:
        vecs.append(clip_embedder.embed_images([ref_image])[0])
    if not vecs:
        raise SystemExit("need --query text and/or --ref-image")
    v = np.mean(vecs, axis=0)
    return v / (np.linalg.norm(v) + 1e-8)


def embed_frames(paths: list[Path], batch: int = 64) -> np.ndarray:
    out = []
    for i in range(0, len(paths), batch):
        out.append(clip_embedder.embed_images(paths[i:i + batch]))
    return np.vstack(out) if out else np.zeros((0, 512), np.float32)


def group_moments(scored: list[dict], pad: float, top: int) -> list[dict]:
    """scored: per-frame {video_id, t, score, frame}. Merge top frames into windows."""
    scored.sort(key=lambda s: -s["score"])
    picked: list[dict] = []
    for s in scored:
        win = [s["t"] - pad, s["t"] + pad]
        clash = next((m for m in picked
                      if m["video_id"] == s["video_id"] and not (win[1] < m["in"] or win[0] > m["out"])), None)
        if clash:  # extend existing moment, keep best peak
            clash["in"], clash["out"] = min(clash["in"], win[0]), max(clash["out"], win[1])
            if s["score"] > clash["peak_score"]:
                clash.update(peak_score=s["score"], peak_t=s["t"], peak_frame=s["frame"])
        else:
            picked.append({"video_id": s["video_id"], "in": max(0, win[0]), "out": win[1],
                           "peak_score": s["score"], "peak_t": s["t"], "peak_frame": s["frame"]})
        if len(picked) >= top and s["score"] < picked[-1]["peak_score"]:
            pass
    picked.sort(key=lambda m: -m["peak_score"])
    return picked[:top]


# ----------------------------- contact sheet -----------------------------

def font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc"):
        if Path(p).exists():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def contact_sheet(moments: list[dict], meta: dict, out: Path, cols: int = 4):
    if not moments:
        return
    CW, CH = 384, 216
    rows = (len(moments) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (CW + 6), rows * (CH + 40)), (18, 18, 22))
    d = ImageDraw.Draw(sheet)
    fs = font(13)
    for i, m in enumerate(moments):
        x, y = (i % cols) * (CW + 6), (i // cols) * (CH + 40)
        fp = Path(m["peak_frame"])
        if fp.exists():
            sheet.paste(Image.open(fp).convert("RGB").resize((CW, CH)), (x, y))
        d.rectangle([x, y, x + 46, y + 18], fill=(0, 0, 0))
        d.text((x + 3, y + 2), f"#{i}", font=fs, fill=(80, 230, 140))
        t = meta[m["video_id"]]["title"][:40]
        d.text((x + 2, y + CH + 2), f"{t}", font=fs, fill=(220, 220, 230))
        d.text((x + 2, y + CH + 20),
               f"{m['in']:.0f}-{m['out']:.0f}s peak={m['peak_t']:.0f}s clip={m['peak_score']:.2f}",
               font=fs, fill=(150, 150, 160))
    sheet.save(out, quality=88)


# ----------------------------- main -----------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--search"); ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--videos", nargs="*", default=[])
    ap.add_argument("--query"); ap.add_argument("--ref-image")
    ap.add_argument("--res", type=int, default=480); ap.add_argument("--fps", type=float, default=1.0)
    ap.add_argument("--pad", type=float, default=1.5); ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--out", default="out/run")
    a = ap.parse_args()

    out = ROOT / a.out
    proxy_dir, frames_root = out / "proxies", out / "frames"
    out.mkdir(parents=True, exist_ok=True)

    videos = list(a.videos)
    if a.search:
        print(f"search: '{a.search}' (top {a.n})")
        videos += search_ids(a.search, a.n)
    if not videos:
        raise SystemExit("need --search or --videos")

    print(f"downloading {len(videos)} proxies @ {a.res}p ...")
    with ThreadPoolExecutor(max_workers=4) as ex:
        metas = [m for m in ex.map(lambda v: download_proxy(v, proxy_dir, a.res), videos) if m]
    meta = {m["id"]: m for m in metas}
    print(f"  {len(metas)} downloaded")

    qv = query_vector(a.query, str(ROOT / a.ref_image) if a.ref_image else None)

    scored = []
    for m in metas:
        frames = sample_frames(Path(m["path"]), frames_root / m["id"], a.fps)
        if not frames:
            continue
        embs = embed_frames([f for _, f in frames])
        sims = embs @ qv
        for (t, f), s in zip(frames, sims):
            scored.append({"video_id": m["id"], "t": float(t), "score": float(s), "frame": str(f)})
        print(f"  {m['id']}: {len(frames)} frames, top={float(sims.max()):.3f}  {m['title'][:44]}")

    moments = group_moments(scored, a.pad, a.top)
    for mo in moments:
        mo["url"] = meta[mo["video_id"]]["url"]
        mo["title"] = meta[mo["video_id"]]["title"]
    (out / "candidates.json").write_text(json.dumps(moments, indent=2))
    contact_sheet(moments, meta, out / "candidates.jpg")
    print(f"\n{len(moments)} candidate moments -> {out/'candidates.json'} + candidates.jpg")
    for i, mo in enumerate(moments[:8]):
        print(f"  #{i} {mo['peak_score']:.3f}  {mo['url']}?t={int(mo['peak_t'])}  "
              f"[{mo['in']:.0f}-{mo['out']:.0f}s]  {mo['title'][:44]}")


if __name__ == "__main__":
    main()
