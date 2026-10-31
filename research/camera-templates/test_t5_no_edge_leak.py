#!/usr/bin/env python3
"""Render-level regression check for the T5 whip-release boundary."""

from __future__ import annotations

import io
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
RENDER = ROOT / "variants" / "T5-step-punch.mp4"
SAMPLE_TIME_SECONDS = 7.94
EDGE_HEIGHT_PX = 8
MAX_NEAR_BLACK_RATIO = 0.10


def extract_frame(path: Path, seconds: float) -> Image.Image:
    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            str(seconds),
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-f",
            "image2pipe",
            "-vcodec",
            "png",
            "-",
        ],
        check=True,
        capture_output=True,
    )
    return Image.open(io.BytesIO(result.stdout)).convert("RGB")


def near_black_ratio(image: Image.Image) -> float:
    top_edge = image.crop((0, 0, image.width, EDGE_HEIGHT_PX))
    pixels = list(top_edge.get_flattened_data())
    return sum(max(pixel) <= 24 for pixel in pixels) / len(pixels)


def main() -> None:
    if not RENDER.exists():
        raise SystemExit(f"FAIL: missing render: {RENDER}")

    ratio = near_black_ratio(extract_frame(RENDER, SAMPLE_TIME_SECONDS))
    if ratio >= MAX_NEAR_BLACK_RATIO:
        raise SystemExit(
            "FAIL: T5 exposes black canvas at the 7.94s whip undershoot "
            f"(top-edge near-black ratio {ratio:.3f}; expected "
            f"< {MAX_NEAR_BLACK_RATIO:.2f})"
        )

    print(
        "PASS: T5 keeps source imagery on the full top edge at 7.94s "
        f"(near-black ratio {ratio:.3f})"
    )


if __name__ == "__main__":
    main()
