#!/usr/bin/env python3
"""Render-level regression check for T3's right-side reveal elements."""

from __future__ import annotations

import io
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
RENDER = ROOT / "variants" / "T3-right-reveal.mp4"
SAMPLE_TIME_SECONDS = 7.0
EDGE_WIDTH_PX = 8
MAX_NEAR_WHITE_RATIO = 0.02


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


def right_edge_white_ratio(image: Image.Image) -> float:
    right_edge = image.crop((image.width - EDGE_WIDTH_PX, 0, image.width, image.height))
    pixels = list(right_edge.get_flattened_data())
    return sum(min(pixel) >= 235 for pixel in pixels) / len(pixels)


def main() -> None:
    if not RENDER.exists():
        raise SystemExit(f"FAIL: missing render: {RENDER}")

    ratio = right_edge_white_ratio(extract_frame(RENDER, SAMPLE_TIME_SECONDS))
    if ratio >= MAX_NEAR_WHITE_RATIO:
        raise SystemExit(
            "FAIL: T3's white pills touch the right frame edge at 7.0s "
            f"(near-white ratio {ratio:.3f}; expected "
            f"< {MAX_NEAR_WHITE_RATIO:.2f})"
        )

    print(
        "PASS: T3's pills remain fully inside the right frame edge at 7.0s "
        f"(near-white ratio {ratio:.3f})"
    )


if __name__ == "__main__":
    main()
