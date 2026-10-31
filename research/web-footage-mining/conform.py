"""HD conform (Shelf 3, step 7) — pull ONLY the chosen seconds in max quality.

After the director picks moments from candidates.json, download just those
sections in high resolution via yt-dlp --download-sections, so we never store
the full HD videos. Proxies are discarded separately.

Usage:
  .venv/bin/python conform.py --url https://youtu.be/ID --in 324 --out 334 --dest out/hd
  .venv/bin/python conform.py --from-candidates out/run/candidates.json --pick 0 2 --dest out/hd
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def hms(t: float) -> str:
    h, r = divmod(int(t), 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def pull(url: str, t_in: float, t_out: float, dest: Path, tag: str) -> Path | None:
    dest.mkdir(parents=True, exist_ok=True)
    out_tmpl = str(dest / f"{tag}.%(ext)s")
    cmd = [
        "yt-dlp", url,
        "--download-sections", f"*{hms(t_in)}-{hms(t_out)}",
        "--force-keyframes-at-cuts",
        "-f", "bv*+ba/b", "--merge-output-format", "mp4",
        "--no-playlist", "-o", out_tmpl,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    hit = list(dest.glob(f"{tag}.mp4"))
    if r.returncode != 0 or not hit:
        print(f"  [conform FAIL] {tag}: {r.stderr.strip().splitlines()[-1:]}")
        return None
    return hit[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url"); ap.add_argument("--in", dest="t_in", type=float)
    ap.add_argument("--out", dest="t_out", type=float)
    ap.add_argument("--from-candidates"); ap.add_argument("--pick", nargs="*", type=int, default=[])
    ap.add_argument("--dest", default="out/hd")
    a = ap.parse_args()
    dest = ROOT / a.dest

    jobs = []
    if a.from_candidates:
        cands = json.loads((ROOT / a.from_candidates).read_text())
        for i in (a.pick or range(len(cands))):
            c = cands[i]
            jobs.append((c["url"], c["in"], c["out"], f"cand{i}_{c['video_id']}"))
    elif a.url:
        jobs.append((a.url, a.t_in, a.t_out, f"clip_{int(a.t_in)}-{int(a.t_out)}"))
    else:
        raise SystemExit("need --url or --from-candidates")

    for url, ti, to, tag in jobs:
        out = pull(url, ti, to, dest, tag)
        if out:
            info = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height", "-show_entries", "format=duration",
                 "-of", "default=nw=1:nk=1", str(out)], capture_output=True, text=True).stdout.split()
            sz = out.stat().st_size / 1e6
            print(f"  {tag}: {'x'.join(info[:2])} {info[-1:]}s {sz:.1f}MB -> {out.name}")


if __name__ == "__main__":
    main()
