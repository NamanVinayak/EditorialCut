#!/usr/bin/env python3
"""
Verification script for the alpha-compositing benchmark.

Checks:
  - Each output MP4: exactly 600 frames, 1920x1080, 30/1 fps, ~20.0s duration.
  - Both input sources are byte-identical to their pre-run SHA-256 (never modified).
  - Extracts 6 evenly-spaced frames per output as JPEGs, builds one 2x3 contact
    sheet per output.
  - Writes results/manifest.json with checksums, versions, settings, timings,
    and pass/fail per check.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

# Paths are relative to this script. Benchmark media is not shipped with the
# repo -- supply your own cutout + background at these (git-ignored) paths and
# re-record the PRE_* constants below for your own files.
ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(ROOT, "results")
FRAMES_DIR = os.path.join(RESULTS, "frames")

SOURCE_MOV = os.path.join(ROOT, "remotion", "public", "cutout-alpha.mov")
SOURCE_MP4 = os.path.join(ROOT, "remotion", "public", "background-270-290.mp4")

OUTPUTS = [
    ("01-rear-typography.mp4", "RearTypography", "contact-01.jpg"),
    ("02-front-badge.mp4", "FrontBadge", "contact-02.jpg"),
    ("03-both.mp4", "Both", "contact-03.jpg"),
]

EXPECTED_WIDTH = 1920
EXPECTED_HEIGHT = 1080
EXPECTED_FRAMES = 600
EXPECTED_FPS = "30/1"
EXPECTED_DURATION = 20.0
DURATION_TOL = 1.0 / 30.0  # +/- 1 frame tolerance

FRAME_TIMES = [0.0, 4.0, 8.0, 12.0, 16.0, 19.9]

# Pre-run checksums, recorded before any work started in this session.
PRE_SHA_MOV = "5ee2943014e84d8ec8e721ffbdfc0837ec1017e800519d542559dcfa3ce19292"
PRE_SHA_MP4 = "f1b4468ff8ea69fdefa29dd7b035625ffac78bc19942569e2128832ebd3f022c"
PRE_SIZE_MOV = 814619077
PRE_SIZE_MP4 = 440538823
PRE_MTIME_MOV = 1783935191
PRE_MTIME_MP4 = 1783931253


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024 * 8), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe_json(path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_name,codec_type,pix_fmt,width,height,r_frame_rate,nb_frames",
        "-show_entries", "format=duration",
        "-of", "json", path,
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def check_output_probe(path):
    data = ffprobe_json(path)
    vstream = next(s for s in data["streams"] if s["codec_type"] == "video")
    width = vstream.get("width")
    height = vstream.get("height")
    fps = vstream.get("r_frame_rate")
    nb_frames = int(vstream.get("nb_frames", -1))
    duration = float(data["format"]["duration"])
    codec = vstream.get("codec_name")
    pix_fmt = vstream.get("pix_fmt")

    checks = {
        "width_1920": width == EXPECTED_WIDTH,
        "height_1080": height == EXPECTED_HEIGHT,
        "fps_30": fps == EXPECTED_FPS,
        "frames_600": nb_frames == EXPECTED_FRAMES,
        "duration_20s_tol_1frame": abs(duration - EXPECTED_DURATION) <= DURATION_TOL,
    }
    return {
        "codec_name": codec,
        "pix_fmt": pix_fmt,
        "width": width,
        "height": height,
        "r_frame_rate": fps,
        "nb_frames": nb_frames,
        "duration": duration,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def extract_frames_and_contact_sheet(mp4_path, base_name, contact_sheet_name):
    os.makedirs(FRAMES_DIR, exist_ok=True)
    frame_paths = []
    for i, t in enumerate(FRAME_TIMES):
        out_name = f"{base_name}_{i:02d}_{t:05.2f}s.jpg"
        out_path = os.path.join(FRAMES_DIR, out_name)
        cmd = [
            "ffmpeg", "-y", "-ss", str(t), "-i", mp4_path,
            "-frames:v", "1", "-update", "1", "-q:v", "2", out_path,
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        frame_paths.append(out_path)

    contact_sheet_path = os.path.join(RESULTS, contact_sheet_name)
    inputs = []
    for p in frame_paths:
        inputs += ["-i", p]
    filter_inputs = "".join(f"[{i}:v]" for i in range(len(frame_paths)))
    # 2 rows x 3 columns of equal-sized tiles; xstack needs cumulative sums
    # (w0+w1, not "2*w0" -- the latter silently mis-lays the grid).
    filter_complex = (
        f"{filter_inputs}xstack=inputs={len(frame_paths)}:"
        f"layout=0_0|w0_0|w0+w1_0|0_h0|w0_h0|w0+w1_h0[out]"
    )
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", filter_complex,
        "-map", "[out]", "-update", "1", "-q:v", "3", contact_sheet_path,
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)
    return frame_paths, contact_sheet_path


def main():
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "node_version": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(),
        "remotion_version": None,
        "inputs": {},
        "outputs": {},
        "overall_pass": True,
    }

    # remotion version
    pkg_path = os.path.join(ROOT, "remotion", "node_modules", "remotion", "package.json")
    try:
        with open(pkg_path) as f:
            report["remotion_version"] = json.load(f)["version"]
    except Exception as e:
        report["remotion_version"] = f"unknown ({e})"

    # --- Input source verification (post-run, compared to pre-run values) ---
    mov_post_sha = sha256_of(SOURCE_MOV)
    mov_post_size = os.path.getsize(SOURCE_MOV)
    mov_post_mtime = int(os.path.getmtime(SOURCE_MOV))

    mp4_post_sha = sha256_of(SOURCE_MP4)
    mp4_post_size = os.path.getsize(SOURCE_MP4)
    mp4_post_mtime = int(os.path.getmtime(SOURCE_MP4))

    mov_unchanged = (mov_post_sha == PRE_SHA_MOV and mov_post_size == PRE_SIZE_MOV and mov_post_mtime == PRE_MTIME_MOV)
    mp4_unchanged = (mp4_post_sha == PRE_SHA_MP4 and mp4_post_size == PRE_SIZE_MP4 and mp4_post_mtime == PRE_MTIME_MP4)

    report["inputs"]["cutout-alpha.mov"] = {
        "path": SOURCE_MOV,
        "pre_sha256": PRE_SHA_MOV,
        "post_sha256": mov_post_sha,
        "pre_size": PRE_SIZE_MOV,
        "post_size": mov_post_size,
        "pre_mtime": PRE_MTIME_MOV,
        "post_mtime": mov_post_mtime,
        "unchanged": mov_unchanged,
    }
    report["inputs"]["source_long_mp4"] = {
        "path": SOURCE_MP4,
        "pre_sha256": PRE_SHA_MP4,
        "post_sha256": mp4_post_sha,
        "pre_size": PRE_SIZE_MP4,
        "post_size": mp4_post_size,
        "pre_mtime": PRE_MTIME_MP4,
        "post_mtime": mp4_post_mtime,
        "unchanged": mp4_unchanged,
    }

    if not (mov_unchanged and mp4_unchanged):
        report["overall_pass"] = False

    # --- Output verification ---
    for fname, comp_id, contact_name in OUTPUTS:
        path = os.path.join(RESULTS, fname)
        probe = check_output_probe(path)
        base_name = comp_id.lower()
        frame_paths, contact_sheet_path = extract_frames_and_contact_sheet(path, base_name, contact_name)
        out_sha = sha256_of(path)
        out_size = os.path.getsize(path)

        entry = {
            "composition_id": comp_id,
            "path": path,
            "sha256": out_sha,
            "size_bytes": out_size,
            "probe": probe,
            "frames_extracted": frame_paths,
            "contact_sheet": contact_sheet_path,
        }
        report["outputs"][fname] = entry
        if not probe["all_pass"]:
            report["overall_pass"] = False

    manifest_path = os.path.join(RESULTS, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(report, f, indent=2)

    # --- Print summary ---
    print("=== Input verification ===")
    for name, entry in report["inputs"].items():
        status = "PASS" if entry["unchanged"] else "FAIL"
        print(f"[{status}] {name}: unchanged={entry['unchanged']}")

    print("\n=== Output verification ===")
    for fname, entry in report["outputs"].items():
        p = entry["probe"]
        status = "PASS" if p["all_pass"] else "FAIL"
        print(f"[{status}] {fname}: {p['width']}x{p['height']} @ {p['r_frame_rate']}, "
              f"{p['nb_frames']} frames, {p['duration']:.3f}s, codec={p['codec_name']}, pix_fmt={p['pix_fmt']}")
        for check_name, ok in p["checks"].items():
            print(f"    - {check_name}: {'PASS' if ok else 'FAIL'}")

    print(f"\nManifest written to {manifest_path}")
    print(f"\nOVERALL: {'PASS' if report['overall_pass'] else 'FAIL'}")
    sys.exit(0 if report["overall_pass"] else 1)


if __name__ == "__main__":
    main()
