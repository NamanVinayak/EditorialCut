#!/usr/bin/env python3
"""
Selective luminance subject poster treatment.
Decodes cutout-alpha.mov (ProRes 4444, straight alpha) once, computes three
duotone luminance-selection variants + reference inner-mask matte, and streams
all four outputs to concurrent ffmpeg H.264 encoders.

Deterministic, numpy-only (no ML models).
"""
import subprocess
import sys
import time
import json
import os
from pathlib import Path

import numpy as np

W, H = 1920, 1080
NFRAMES = 600
FPS = 30
FRAME_BYTES_IN = W * H * 4 * 2  # rgba64le: 4 channels x 2 bytes
FRAME_BYTES_OUT = W * H * 3     # rgb24 out

BASE = Path(__file__).resolve().parent
INPUT = os.environ.get("EDITORIALCUT_ALPHA_INPUT", str(BASE / "input-alpha.mov"))
OUTDIR = BASE / "results"
LOGDIR = BASE / "logs"
OUTDIR.mkdir(parents=True, exist_ok=True)
LOGDIR.mkdir(parents=True, exist_ok=True)

ACCENT = np.array([0xB3, 0x27, 0x1E], dtype=np.float64) / 255.0  # deep red
WHITE = np.array([0xF7, 0xF4, 0xEE], dtype=np.float64) / 255.0   # near paper-white
CANVAS = np.array([0xF5, 0xF2, 0xEC], dtype=np.float64) / 255.0  # warm paper canvas

VARIANTS = {
    "01-conservative": (0.10, 0.35),
    "02-reference": (0.20, 0.55),
    "03-aggressive": (0.35, 0.75),
}
GRAIN_AMPLITUDE = 6.0 / 255.0


def smoothstep(lo, hi, x):
    t = np.clip((x - lo) / (hi - lo), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def start_decoder():
    cmd = [
        "ffmpeg", "-v", "error", "-i", INPUT,
        "-f", "rawvideo", "-pix_fmt", "rgba64le", "pipe:1",
    ]
    logf = open(LOGDIR / "decoder.stderr.log", "wb")
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=logf), logf


def start_encoder(path, framerate=FPS, crf=16):
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pixel_format", "rgb24",
        "-video_size", f"{W}x{H}", "-framerate", str(framerate),
        "-i", "pipe:0",
        "-frames:v", str(NFRAMES),
        "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        "-color_range", "tv", "-colorspace", "bt709",
        "-color_primaries", "bt709", "-color_trc", "bt709",
        str(path),
    ]
    logf = open(LOGDIR / f"{Path(path).stem}.stderr.log", "wb")
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=logf), logf


def main():
    t_start = time.time()
    timings = {}

    decoder, decoder_log = start_decoder()

    encoders = {}
    encoder_logs = {}
    for name in VARIANTS:
        proc, logf = start_encoder(OUTDIR / f"{name}.mp4")
        encoders[name] = proc
        encoder_logs[name] = logf

    # Matte is a verification artifact: encode lossless (crf=0) so the
    # inner-mask containment check isn't confounded by H.264 quantization
    # bleed at the silhouette edge.
    matte_proc, matte_log = start_encoder(OUTDIR / "matte-reference.mp4", crf=0)

    t_decode_setup = time.time()

    for idx in range(NFRAMES):
        buf = decoder.stdout.read(FRAME_BYTES_IN)
        if len(buf) != FRAME_BYTES_IN:
            raise RuntimeError(
                f"Short read from decoder at frame {idx}: got {len(buf)} bytes, "
                f"expected {FRAME_BYTES_IN}"
            )
        arr = np.frombuffer(buf, dtype="<u2").reshape(H, W, 4).astype(np.float64)
        R = arr[..., 0] / 65535.0
        G = arr[..., 1] / 65535.0
        B = arr[..., 2] / 65535.0
        A = arr[..., 3] / 65535.0

        Y = 0.2126 * R + 0.7152 * G + 0.0722 * B

        # One canonical grain field per frame (seed depends only on frame index,
        # per spec), reused across variants, each gated by that variant's own
        # inner mask so the visible grain differs per variant even though the
        # underlying noise field is identical.
        rng = np.random.default_rng(seed=idx)
        noise = rng.normal(0.0, 1.0, size=(H, W)) * GRAIN_AMPLITUDE

        for name, (lo, hi) in VARIANTS.items():
            t = smoothstep(lo, hi, Y)          # bright-side mix fraction
            sel = 1.0 - t                       # dark-side selection
            inner_mask = sel * A                # exactly zero where A == 0

            accent_factor = np.clip(Y / hi, 0.0, 1.0)
            shade = 0.55 + 0.45 * accent_factor
            accent_shaded = ACCENT[None, None, :] * shade[..., None]

            duotone = accent_shaded * sel[..., None] + WHITE[None, None, :] * t[..., None]
            duotone_grain = duotone + noise[..., None] * inner_mask[..., None]

            composite = duotone_grain * A[..., None] + CANVAS[None, None, :] * (1.0 - A[..., None])
            composite = np.clip(composite, 0.0, 1.0)

            out_u8 = np.clip(composite * 255.0 + 0.5, 0, 255).astype(np.uint8)
            encoders[name].stdin.write(out_u8.tobytes())

            if name == "02-reference":
                matte_u8 = np.clip(inner_mask * 255.0 + 0.5, 0, 255).astype(np.uint8)
                matte_rgb = np.repeat(matte_u8[..., None], 3, axis=2)
                matte_proc.stdin.write(matte_rgb.tobytes())

        if (idx + 1) % 100 == 0 or idx == 0:
            print(f"  frame {idx+1}/{NFRAMES} ({time.time()-t_start:.1f}s elapsed)", file=sys.stderr)

    t_compute_done = time.time()

    # Close stdin on all encoders to signal EOF, then wait.
    for name, proc in encoders.items():
        proc.stdin.close()
    matte_proc.stdin.close()

    rc = {}
    for name, proc in encoders.items():
        rc[name] = proc.wait()
    rc["matte-reference"] = matte_proc.wait()

    decoder.stdout.close()
    dec_rc = decoder.wait()

    for logf in list(encoder_logs.values()) + [matte_log, decoder_log]:
        logf.close()

    t_end = time.time()

    timings = {
        "decoder_setup_s": round(t_decode_setup - t_start, 3),
        "decode_and_compute_and_encode_stream_s": round(t_compute_done - t_decode_setup, 3),
        "encoder_flush_wait_s": round(t_end - t_compute_done, 3),
        "total_s": round(t_end - t_start, 3),
    }

    result = {
        "decoder_returncode": dec_rc,
        "encoder_returncodes": rc,
        "timings": timings,
    }
    print(json.dumps(result, indent=2))

    if dec_rc != 0 or any(v != 0 for v in rc.values()):
        print("ERROR: non-zero return code detected, check logs/ directory", file=sys.stderr)
        sys.exit(1)

    with open(LOGDIR / "process_run.json", "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
