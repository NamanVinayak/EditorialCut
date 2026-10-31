from pathlib import Path

import numpy as np
from PIL import Image

from maskbench.composite import (
    FFmpegRawWriter,
    composite_behind,
    normalize_mask,
    normalized_crop,
)
from maskbench.media import probe_media


def test_soft_matte_remains_soft() -> None:
    native = np.array([[0, 64], [192, 255]], dtype=np.uint8)

    normalized = normalize_mask(native, (2, 2), kind="alpha")

    assert set(np.unique(normalized)) == {0, 64, 192, 255}


def test_hard_mask_uses_only_binary_values() -> None:
    native = np.array([[0, 255], [255, 0]], dtype=np.uint8)

    normalized = normalize_mask(native, (4, 4), kind="binary")

    assert set(np.unique(normalized)) == {0, 255}


def test_composite_keeps_foreground_and_changes_background() -> None:
    original = np.full((2, 2, 3), 20, dtype=np.uint8)
    graphic = np.full((2, 2, 3), 200, dtype=np.uint8)
    mask = np.array([[255, 0], [255, 0]], dtype=np.uint8)

    result = composite_behind(original, graphic, mask)

    assert result[0, 0].tolist() == [20, 20, 20]
    assert result[0, 1].tolist() == [200, 200, 200]


def test_normalized_crop_converts_to_pixel_bounds() -> None:
    assert normalized_crop((0.25, 0.10, 0.50, 0.40), 1920, 1080) == (
        480,
        108,
        1440,
        540,
    )


def test_raw_writer_encodes_exact_frame_count(tmp_path: Path) -> None:
    output = tmp_path / "five-frames.mp4"
    with FFmpegRawWriter(output, width=64, height=48, fps=5, channels=3) as writer:
        for value in range(5):
            writer.write(np.full((48, 64, 3), value * 30, dtype=np.uint8))

    probe = probe_media(output)
    assert probe.frame_count == 5
    assert probe.width == 64
    assert probe.height == 48
