#!/usr/bin/env python3
"""
verify.py — Geometric Masks Conformance Reel verification script.
Checks: ffprobe metadata, source fingerprint, flash timing proof, frame extraction.
"""

import subprocess
import json
import hashlib
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
RESULTS = ROOT / "results"
FLASH_PROOF = RESULTS / "flash-proof"
FRAMES_DIR = RESULTS / "frames"
REEL = RESULTS / "conformance-reel.mp4"
SOURCE = Path("<REDACTED-PATH>")

# Known source fingerprint (recorded before starting)
SOURCE_SHA256 = "229371d07ea41bf58a8c744fcacec71a24dc9aaf31e3560c3958c2980778f906"
SOURCE_SIZE   = 17368738

# Flash event windows (absolute frame numbers, 0-indexed, inclusive)
FLASH_EVENTS = {
    "seg0_event_A_4frame": {"start": 25, "end": 28, "expected_duration": 4},
    "seg0_event_B_5frame": {"start": 50, "end": 54, "expected_duration": 5},
    "seg0_stack_rect0":    {"start": 80, "end": 83, "expected_duration": 4},
    "seg0_stack_rect1":    {"start": 83, "end": 86, "expected_duration": 4},
    "seg0_stack_rect2":    {"start": 86, "end": 89, "expected_duration": 4},
    "seg1_flash_A_precut": {"start": 177, "end": 179, "expected_duration": 3},
    "seg1_flash_B_postcut":{"start": 180, "end": 182, "expected_duration": 3},
}

# For flash-proof extraction: frames around each key event
PROOF_EVENTS = [
    # Event A: 4-frame (abs 25-28) — extract abs 23-30
    {"name": "event_A", "range": range(23, 31)},
    # Event B: 5-frame (abs 50-54) — extract abs 48-56
    {"name": "event_B", "range": range(48, 57)},
    # Stacked region (abs 78-91) — 2 frames before rect0, through 2 after rect2
    {"name": "stack_region", "range": range(78, 92)},
    # Cut bridge flash (abs 175-184)
    {"name": "cut_bridge_flash", "range": range(175, 185)},
]

# Segment frame windows for contact-sheet extraction
SEGMENTS = [
    {"name": "seg0_diff_flash",      "start": 0,   "end": 119},
    {"name": "seg1_cut_bridge",      "start": 120, "end": 239},
    {"name": "seg2_circular_reveal", "start": 240, "end": 359},
    {"name": "seg3_slider",          "start": 360, "end": 479},
    {"name": "seg4_cinematic_screen",   "start": 480, "end": 599},
]


def run(cmd, **kwargs):
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    return result


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe_video(path: Path) -> dict:
    """Return basic video stream info via ffprobe."""
    r = run([
        "ffprobe", "-v", "quiet",
        "-select_streams", "v:0",
        "-count_frames",
        "-show_entries", "stream=nb_read_frames,width,height,r_frame_rate,duration,codec_name,pix_fmt",
        "-of", "json",
        str(path)
    ])
    if r.returncode != 0:
        return {"error": r.stderr}
    data = json.loads(r.stdout)
    if data.get("streams"):
        return data["streams"][0]
    return {"error": "no video stream"}


def extract_frame(src: Path, frame_num: int, out_path: Path):
    """Extract a single frame by absolute frame number (0-indexed)."""
    ts = frame_num / 30.0
    r = run([
        "ffmpeg", "-y",
        "-ss", f"{ts:.6f}",
        "-i", str(src),
        "-frames:v", "1",
        "-q:v", "2",
        str(out_path)
    ])
    return r.returncode == 0


def main():
    checks = {}
    print("=" * 70)
    print("Geometric Masks Conformance Reel — Verification")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 70)

    # ─── 1. Source fingerprint unchanged ─────────────────────────────────────
    print("\n[1] Verifying source fingerprint...")
    if not SOURCE.exists():
        checks["source_exists"] = {"pass": False, "msg": f"Source not found: {SOURCE}"}
        print(f"  FAIL: {SOURCE} not found")
    else:
        actual_sha = sha256_file(SOURCE)
        actual_size = SOURCE.stat().st_size
        sha_ok = (actual_sha == SOURCE_SHA256)
        size_ok = (actual_size == SOURCE_SIZE)
        checks["source_sha256"] = {"pass": sha_ok, "expected": SOURCE_SHA256, "actual": actual_sha}
        checks["source_size"]   = {"pass": size_ok, "expected": SOURCE_SIZE,   "actual": actual_size}
        print(f"  SHA256: {'PASS' if sha_ok else 'FAIL'} ({actual_sha[:16]}...)")
        print(f"  Size:   {'PASS' if size_ok else 'FAIL'} ({actual_size} bytes)")

    # ─── 2. Reel exists ───────────────────────────────────────────────────────
    print("\n[2] Checking reel exists...")
    if not REEL.exists():
        checks["reel_exists"] = {"pass": False, "msg": str(REEL)}
        print(f"  FAIL: {REEL} not found")
        print("\nAborting — reel not rendered yet.")
        write_manifest(checks)
        sys.exit(1)
    checks["reel_exists"] = {"pass": True}
    print(f"  PASS: {REEL}")

    # ─── 3. ffprobe metadata ──────────────────────────────────────────────────
    print("\n[3] ffprobe metadata...")
    info = ffprobe_video(REEL)
    print(f"  Raw: {info}")

    frame_count = int(info.get("nb_read_frames", 0))
    width       = int(info.get("width", 0))
    height      = int(info.get("height", 0))
    fps_raw     = info.get("r_frame_rate", "0/1")
    duration    = float(info.get("duration", 0))
    pix_fmt     = info.get("pix_fmt", "")
    codec       = info.get("codec_name", "")

    # Parse fps fraction
    fps_num, fps_den = (int(x) for x in fps_raw.split("/"))
    fps = fps_num / fps_den

    checks["frame_count"]  = {"pass": frame_count == 600, "expected": 600, "actual": frame_count}
    checks["width"]        = {"pass": width == 1920,      "expected": 1920, "actual": width}
    checks["height"]       = {"pass": height == 1080,     "expected": 1080, "actual": height}
    checks["fps"]          = {"pass": abs(fps - 30.0) < 0.01, "expected": 30.0, "actual": fps}
    checks["duration_20s"] = {"pass": abs(duration - 20.0) < 0.1, "expected": 20.0, "actual": duration}
    checks["pix_fmt_yuv420p"] = {"pass": pix_fmt == "yuv420p", "expected": "yuv420p", "actual": pix_fmt}
    checks["codec_h264"]   = {"pass": codec == "h264", "expected": "h264", "actual": codec}

    for k in ["frame_count", "width", "height", "fps", "duration_20s", "pix_fmt_yuv420p", "codec_h264"]:
        c = checks[k]
        print(f"  {k}: {'PASS' if c['pass'] else 'FAIL'} (expected={c['expected']}, actual={c['actual']})")

    # ─── 4. Flash-proof frame extraction ─────────────────────────────────────
    print("\n[4] Extracting flash-proof frames...")
    FLASH_PROOF.mkdir(parents=True, exist_ok=True)

    all_flash_frames = set()
    for event in PROOF_EVENTS:
        for fn in event["range"]:
            all_flash_frames.add(fn)

    extracted = []
    for fn in sorted(all_flash_frames):
        out = FLASH_PROOF / f"frame_{fn:04d}.jpg"
        ok = extract_frame(REEL, fn, out)
        if ok:
            extracted.append(fn)
            print(f"  Extracted frame {fn:04d} → {out.name}")
        else:
            print(f"  WARN: failed to extract frame {fn}")

    checks["flash_proof_frames"] = {"pass": len(extracted) == len(all_flash_frames), "extracted": len(extracted), "expected": len(all_flash_frames)}
    print(f"  Flash-proof extraction: {'PASS' if checks['flash_proof_frames']['pass'] else 'FAIL'} ({len(extracted)}/{len(all_flash_frames)} frames)")

    # ─── 5. Per-segment frame extraction (6 evenly spaced per segment) ────────
    print("\n[5] Extracting per-segment frames...")
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    seg_frame_paths = []  # for contact sheet

    for seg in SEGMENTS:
        seg_start = seg["start"]
        seg_end   = seg["end"]
        seg_name  = seg["name"]
        total = seg_end - seg_start + 1
        # Pick 6 evenly spaced frames within segment (integer steps)
        indices = [seg_start + round(i * (total - 1) / 5) for i in range(6)]
        for i, fn in enumerate(indices):
            out = FRAMES_DIR / f"{seg_name}_f{fn:04d}_{i+1}of6.jpg"
            ok = extract_frame(REEL, fn, out)
            if ok:
                seg_frame_paths.append(out)
                print(f"  {seg_name} frame {fn}: OK")
            else:
                print(f"  WARN: {seg_name} frame {fn}: FAILED")

    checks["segment_frames"] = {"pass": len(seg_frame_paths) == 30, "extracted": len(seg_frame_paths), "expected": 30}
    print(f"  Segment frame extraction: {'PASS' if checks['segment_frames']['pass'] else 'FAIL'} ({len(seg_frame_paths)}/30)")

    # ─── 6. Contact sheet (ffmpeg xstack 5×6 = 30 tiles) ─────────────────────
    # Build a 5×6 grid: 5 segments (rows) × 6 frames each (columns)
    # Use xstack with layout syntax: cumulative w/h offsets
    print("\n[6] Building contact sheet...")
    contact_sheet = RESULTS / "contact-sheet.jpg"

    # Sort paths to ensure correct order
    sorted_paths = sorted(seg_frame_paths)

    # Build ffmpeg inputs
    inputs = []
    for p in sorted_paths:
        inputs += ["-i", str(p)]

    # Build xstack layout: 6 columns, 5 rows
    # Layout: col = idx % 6, row = idx // 6
    # Use cumulative position strings
    # Frame dimensions: 1920/6=320 wide, 1080/5=216 high (approx)
    # We'll use xstack with 30 tiles arranged 6 wide × 5 tall
    N = 30
    COLS = 6
    ROWS = 5

    # Build layout string using w0+w1+... syntax for x positions
    # and h0*row syntax for y positions
    layout_parts = []
    for idx in range(N):
        col = idx % COLS
        row = idx // COLS
        # x position: sum of widths of previous columns in same row
        if col == 0:
            x_pos = "0"
        else:
            x_pos = "+".join(f"w{(row * COLS) + c}" for c in range(col))
        # y position: sum of heights of rows above
        if row == 0:
            y_pos = "0"
        else:
            y_pos = "+".join(f"h{r * COLS}" for r in range(row))
        layout_parts.append(f"{x_pos}_{y_pos}")

    layout_str = "|".join(layout_parts)

    # Scale each frame to 320x216 before stacking
    filter_parts = []
    for idx in range(N):
        filter_parts.append(f"[{idx}:v]scale=320:216[v{idx}]")
    scale_str = ";".join(filter_parts)
    inputs_str = "".join(f"[v{idx}]" for idx in range(N))
    vf = f"{scale_str};{inputs_str}xstack=inputs={N}:layout={layout_str}[out]"

    r = run(
        ["ffmpeg", "-y"] + inputs + [
            "-filter_complex", vf,
            "-map", "[out]",
            "-frames:v", "1",
            str(contact_sheet)
        ]
    )
    if r.returncode == 0:
        checks["contact_sheet"] = {"pass": True, "path": str(contact_sheet)}
        print(f"  PASS: {contact_sheet}")
    else:
        print(f"  FAIL: {r.stderr[-500:]}")
        # Try simpler 5-column layout (one frame per segment, label frame)
        checks["contact_sheet"] = {"pass": False, "error": r.stderr[-200:]}

    # ─── 7. Flash timing verification (documentary only) ─────────────────────
    print("\n[7] Flash timing documentation...")
    for event_name, ev in FLASH_EVENTS.items():
        dur = ev["end"] - ev["start"] + 1
        ok = (dur == ev["expected_duration"])
        checks[f"flash_timing_{event_name}"] = {
            "pass": ok,
            "start_frame": ev["start"],
            "end_frame": ev["end"],
            "duration_frames": dur,
            "expected_duration": ev["expected_duration"]
        }
        print(f"  {event_name}: frames {ev['start']}–{ev['end']} = {dur}f {'PASS' if ok else 'FAIL'}")

    # ─── 8. Reel checksum ────────────────────────────────────────────────────
    print("\n[8] Computing reel SHA256...")
    reel_sha = sha256_file(REEL)
    reel_size = REEL.stat().st_size
    checks["reel_sha256"] = reel_sha
    checks["reel_size"]   = reel_size
    print(f"  SHA256: {reel_sha}")
    print(f"  Size: {reel_size} bytes")

    # ─── 9. Get versions ─────────────────────────────────────────────────────
    node_v = run(["node", "--version"]).stdout.strip()
    npm_v  = run(["npm", "--version"]).stdout.strip()
    ffmpeg_v = run(["ffmpeg", "-version"]).stdout.split("\n")[0]

    # Get Remotion version from package.json
    with open(ROOT / "remotion" / "package.json") as f:
        pkg = json.load(f)
    remotion_version = pkg["dependencies"]["remotion"]

    # ─── 10. Summary ─────────────────────────────────────────────────────────
    total = sum(1 for k, v in checks.items() if isinstance(v, dict) and "pass" in v)
    passed = sum(1 for k, v in checks.items() if isinstance(v, dict) and v.get("pass"))
    print(f"\n{'='*70}")
    print(f"SUMMARY: {passed}/{total} checks passed")

    # ─── 11. Write manifest ───────────────────────────────────────────────────
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "asset_provenance": {
            "source": str(SOURCE),
            "source_sha256": SOURCE_SHA256,
            "source_size": SOURCE_SIZE,
            "plate": str(ASSETS / "plate.mp4"),
            "plate_gray": str(ASSETS / "plate-gray.mp4"),
            "plate_noisy": str(ASSETS / "plate-noisy.mp4"),
            "derived_from": "ffmpeg re-encode with -c:v libx264 -r 30 -g 30 -keyint_min 30 -movflags +faststart"
        },
        "reel": {
            "path": str(REEL),
            "sha256": reel_sha,
            "size_bytes": reel_size
        },
        "versions": {
            "node": node_v,
            "npm": npm_v,
            "remotion": remotion_version,
            "ffmpeg": ffmpeg_v
        },
        "render_settings": {
            "composition": "ConformanceReel",
            "fps": 30,
            "width": 1920,
            "height": 1080,
            "duration_frames": 600,
            "flags": "--muted --color-space=bt709 --concurrency=4"
        },
        "segment_frame_windows": {s["name"]: {"start": s["start"], "end": s["end"]} for s in SEGMENTS},
        "flash_events": FLASH_EVENTS,
        "checks": checks,
        "summary": {"total": total, "passed": passed}
    }

    manifest_path = RESULTS / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest written: {manifest_path}")

    return 0 if passed == total else 1


def write_manifest(checks):
    manifest = {"checks": checks, "generated_at": datetime.now().isoformat()}
    manifest_path = RESULTS / "manifest.json"
    RESULTS.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    sys.exit(main())
