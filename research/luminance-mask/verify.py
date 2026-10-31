#!/usr/bin/env python3
"""
Verification for the luminance-mask benchmark outputs.

Checks:
  1. Input fingerprint unchanged (sha256 + size vs recorded values).
  2. Each output mp4: 600 frames, 1920x1080, 30fps, 20.000s duration, yuv420p.
  3. Inner-mask containment: sample 20 frames evenly spaced across the clip,
     decode alpha from the (untouched) source and the encoded
     matte-reference.mp4 grayscale value at the same frames, and confirm no
     pixel has inner-mask value > 2/255 wherever source alpha < 2/255.

Prints a JSON report and exits non-zero on any failure.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

BASE = Path("<REDACTED-PATH>")
RESULTS = BASE / "results"
INPUT = Path("<REDACTED-PATH>")

EXPECTED_SHA256 = "5ee2943014e84d8ec8e721ffbdfc0837ec1017e800519d542559dcfa3ce19292"
EXPECTED_SIZE = 814619077

W, H = 1920, 1080
NFRAMES = 600
OUTPUTS = ["01-conservative.mp4", "02-reference.mp4", "03-aggressive.mp4", "matte-reference.mp4"]

SAMPLE_IDXS = list(range(0, 600, 30))  # 20 evenly spaced frames: 0,30,...,570
ALPHA_THRESH = 2.0 / 255.0
MASK_THRESH = 2.0 / 255.0


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def ffprobe_json(path):
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,pix_fmt,nb_frames,duration",
        "-of", "json", str(path),
    ]
    out = subprocess.check_output(cmd)
    return json.loads(out)["streams"][0]


def decode_select_frames(path, pix_fmt, channels, bytes_per_channel, idxs):
    """Decode only the given frame indices via ffmpeg select filter, returns
    a list of numpy arrays shaped (H, W, channels)."""
    select_expr = "+".join(f"eq(n\\,{i})" for i in idxs)
    cmd = [
        "ffmpeg", "-v", "error", "-i", str(path),
        "-vf", f"select='{select_expr}'", "-vsync", "0",
        "-f", "rawvideo", "-pix_fmt", pix_fmt, "pipe:1",
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg decode failed for {path}: {proc.stderr.decode()}")
    dtype = np.uint16 if bytes_per_channel == 2 else np.uint8
    frame_bytes = W * H * channels * bytes_per_channel
    data = proc.stdout
    n_frames = len(data) // frame_bytes
    if n_frames != len(idxs):
        raise RuntimeError(
            f"Expected {len(idxs)} frames decoded from {path}, got {n_frames} "
            f"(bytes={len(data)}, frame_bytes={frame_bytes})"
        )
    frames = []
    for k in range(n_frames):
        chunk = data[k * frame_bytes:(k + 1) * frame_bytes]
        arr = np.frombuffer(chunk, dtype=dtype).reshape(H, W, channels)
        frames.append(arr)
    return frames


def main():
    report = {"checks": {}, "pass": True}

    # 1. Input fingerprint
    actual_size = INPUT.stat().st_size
    actual_sha = sha256_of(INPUT)
    fp_ok = (actual_size == EXPECTED_SIZE) and (actual_sha == EXPECTED_SHA256)
    report["checks"]["input_fingerprint"] = {
        "pass": fp_ok,
        "expected_sha256": EXPECTED_SHA256,
        "actual_sha256": actual_sha,
        "expected_size": EXPECTED_SIZE,
        "actual_size": actual_size,
    }
    if not fp_ok:
        report["pass"] = False

    # 2. Per-output spec checks
    spec_checks = {}
    for name in OUTPUTS:
        path = RESULTS / name
        if not path.exists():
            spec_checks[name] = {"pass": False, "error": "file missing"}
            report["pass"] = False
            continue
        info = ffprobe_json(path)
        width = int(info["width"])
        height = int(info["height"])
        pix_fmt = info["pix_fmt"]
        r_frame_rate = info["r_frame_rate"]
        nb_frames = int(info["nb_frames"])
        duration = float(info["duration"])

        ok = (
            width == W
            and height == H
            and pix_fmt == "yuv420p"
            and r_frame_rate == "30/1"
            and nb_frames == NFRAMES
            and abs(duration - 20.000000) < 0.01
        )
        spec_checks[name] = {
            "pass": ok,
            "width": width, "height": height, "pix_fmt": pix_fmt,
            "r_frame_rate": r_frame_rate, "nb_frames": nb_frames, "duration": duration,
        }
        if not ok:
            report["pass"] = False
    report["checks"]["output_specs"] = spec_checks

    # 3. Inner-mask containment (matte-reference vs source alpha)
    alpha_frames = decode_select_frames(INPUT, "rgba64le", 4, 2, SAMPLE_IDXS)
    matte_frames = decode_select_frames(RESULTS / "matte-reference.mp4", "rgb24", 3, 1, SAMPLE_IDXS)

    violations = []
    max_violation_value = 0.0
    total_alpha0_pixels = 0
    for idx, a_arr, m_arr in zip(SAMPLE_IDXS, alpha_frames, matte_frames):
        alpha_norm = a_arr[..., 3].astype(np.float64) / 65535.0
        matte_norm = m_arr[..., 0].astype(np.float64) / 255.0  # R channel (grayscale, R=G=B)

        low_alpha = alpha_norm < ALPHA_THRESH
        total_alpha0_pixels += int(low_alpha.sum())
        bad = low_alpha & (matte_norm > MASK_THRESH)
        n_bad = int(bad.sum())
        if n_bad > 0:
            local_max = float(matte_norm[bad].max())
            max_violation_value = max(max_violation_value, local_max)
            violations.append({"frame": idx, "violating_pixels": n_bad, "max_mask_value": local_max})

    containment_ok = len(violations) == 0
    report["checks"]["inner_mask_containment"] = {
        "pass": containment_ok,
        "sampled_frames": SAMPLE_IDXS,
        "alpha_threshold": ALPHA_THRESH,
        "mask_threshold": MASK_THRESH,
        "total_low_alpha_pixels_sampled": total_alpha0_pixels,
        "violations": violations,
        "max_violation_value": max_violation_value,
    }
    if not containment_ok:
        report["pass"] = False

    print(json.dumps(report, indent=2))
    with open(BASE / "verify_report.json", "w") as f:
        json.dump(report, f, indent=2)

    if not report["pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
