from __future__ import annotations

import json
import subprocess
from contextlib import ExitStack
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image

from .config import BenchmarkConfig


def normalize_mask(native: np.ndarray, size: tuple[int, int], kind: str) -> np.ndarray:
    if native.ndim == 3:
        native = cv2.cvtColor(native, cv2.COLOR_RGB2GRAY)
    width, height = size
    interpolation = cv2.INTER_NEAREST if kind == "binary" else cv2.INTER_LANCZOS4
    resized = cv2.resize(native, (width, height), interpolation=interpolation)
    if kind == "binary":
        resized = np.where(resized >= 128, 255, 0).astype(np.uint8)
    return resized.astype(np.uint8)


def composite_behind(original: np.ndarray, graphic: np.ndarray, mask: np.ndarray) -> np.ndarray:
    alpha = mask.astype(np.float32)[..., None] / 255.0
    result = original.astype(np.float32) * alpha + graphic.astype(np.float32) * (1.0 - alpha)
    return np.rint(np.clip(result, 0, 255)).astype(np.uint8)


def normalized_crop(
    crop: tuple[float, float, float, float], width: int, height: int
) -> tuple[int, int, int, int]:
    x, y, crop_width, crop_height = crop
    x0 = round(x * width)
    y0 = round(y * height)
    return (
        x0,
        y0,
        round((x + crop_width) * width),
        round((y + crop_height) * height),
    )


class FFmpegRawWriter:
    def __init__(
        self,
        output: Path,
        *,
        width: int,
        height: int,
        fps: int,
        channels: int = 3,
    ) -> None:
        self.output = output
        self.width = width
        self.height = height
        self.channels = channels
        self.process: subprocess.Popen[bytes] | None = None
        self.fps = fps

    def __enter__(self) -> "FFmpegRawWriter":
        self.output.parent.mkdir(parents=True, exist_ok=True)
        input_format = "rgba" if self.channels == 4 else "rgb24"
        if self.channels == 4:
            codec = [
                "-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le"
            ]
        else:
            codec = [
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            ]
        command = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "rawvideo",
            "-pix_fmt", input_format, "-s", f"{self.width}x{self.height}",
            "-r", str(self.fps), "-i", "pipe:0", "-an", *codec, "-y", str(self.output),
        ]
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        return self

    def write(self, frame: np.ndarray) -> None:
        expected = (self.height, self.width, self.channels)
        if frame.shape != expected or frame.dtype != np.uint8:
            raise ValueError(f"raw frame must be uint8 {expected}, got {frame.dtype} {frame.shape}")
        assert self.process is not None and self.process.stdin is not None
        self.process.stdin.write(np.ascontiguousarray(frame).tobytes())

    def __exit__(self, exc_type, exc, traceback) -> None:
        assert self.process is not None and self.process.stdin is not None
        try:
            self.process.stdin.close()
        except BrokenPipeError:
            pass
        stderr = self.process.stderr.read().decode(errors="replace") if self.process.stderr else ""
        returncode = self.process.wait()
        if exc_type is None and returncode != 0:
            raise RuntimeError(f"FFmpeg writer failed for {self.output}: {stderr.strip()}")


def _checkerboard(width: int, height: int, tile: int = 48) -> np.ndarray:
    yy, xx = np.indices((height, width))
    pattern = ((xx // tile + yy // tile) % 2).astype(np.uint8)
    values = np.where(pattern[..., None] == 0, 55, 105).astype(np.uint8)
    return np.repeat(values, 3, axis=2)


def _moving_graphic(original: np.ndarray, index: int, total: int) -> np.ndarray:
    height, width = original.shape[:2]
    background = original.copy()
    cycle = ((index / max(total - 1, 1)) * 2.0) % 1.0
    graphic_width = 850
    x = round(-graphic_width + cycle * (width + graphic_width))
    y0 = round(height * 0.43)
    y1 = y0 + 190
    cv2.rectangle(background, (x, y0), (x + graphic_width, y1), (20, 220, 245), -1)
    cv2.putText(
        background,
        "MASK TRACKING",
        (x + 35, y0 + 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.75,
        (10, 20, 25),
        5,
        cv2.LINE_AA,
    )
    return background


def _fit_panel(image: np.ndarray, width: int, height: int, label: str) -> np.ndarray:
    canvas = np.full((height, width, 3), 12, dtype=np.uint8)
    scale = min(width / image.shape[1], (height - 70) / image.shape[0])
    resized = cv2.resize(
        image,
        (max(1, round(image.shape[1] * scale)), max(1, round(image.shape[0] * scale))),
        interpolation=cv2.INTER_LANCZOS4,
    )
    x = (width - resized.shape[1]) // 2
    y = 60 + (height - 60 - resized.shape[0]) // 2
    canvas[y:y + resized.shape[0], x:x + resized.shape[1]] = resized
    cv2.putText(canvas, label.upper(), (20, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (20, 220, 245), 2, cv2.LINE_AA)
    return canvas


def _edge_diagnostics(
    original: np.ndarray,
    mask: np.ndarray,
    crops: dict[str, tuple[float, float, float, float]],
) -> np.ndarray:
    outline = cv2.Canny(mask, 40, 120)
    outline = cv2.dilate(outline, np.ones((5, 5), dtype=np.uint8))
    annotated = original.copy()
    annotated[outline > 0] = np.array([255, 40, 210], dtype=np.uint8)
    panels = []
    for label in ("hair", "shoulders-mic", "hands"):
        x0, y0, x1, y1 = normalized_crop(crops[label], original.shape[1], original.shape[0])
        crop = annotated[y0:y1, x0:x1]
        panels.append(_fit_panel(crop, 640, 1080, label.replace("-", " / ")))
    return np.concatenate(panels, axis=1)


def _comparison(original: np.ndarray, result: np.ndarray) -> np.ndarray:
    left = cv2.resize(original, (960, 540), interpolation=cv2.INTER_AREA)
    right = cv2.resize(result, (960, 540), interpolation=cv2.INTER_AREA)
    cv2.putText(left, "ORIGINAL", (28, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(right, "GRAPHIC BEHIND MASK", (28, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 220, 245), 2, cv2.LINE_AA)
    return np.concatenate([left, right], axis=1)


def render_method_views(
    project: Path,
    config: BenchmarkConfig,
    method: str,
) -> dict[str, Any]:
    run_path = project / f"results/methods/{method}/run.json"
    record = json.loads(run_path.read_text())
    if record["status"] != "success":
        return {"method": method, "status": "failed", "run_record": str(run_path)}
    input_frames = sorted((project / "results/prepared/frames").glob("frame_*.png"))
    native_root = Path(record["artifacts"]["native_masks"])
    native_frames = sorted(native_root.glob("frame_*.png"))
    if len(input_frames) != config.expected_frames or len(native_frames) != config.expected_frames:
        raise RuntimeError(f"{method} cannot render: input/mask frame count mismatch")
    if [path.name for path in input_frames] != [path.name for path in native_frames]:
        raise RuntimeError(f"{method} cannot render: input/mask names differ")

    kind = "binary" if method == "edgetam" else "alpha"
    normalized_root = project / f"results/methods/{method}/normalized"
    normalized_root.mkdir(parents=True, exist_ok=True)
    for old in normalized_root.glob("frame_*.png"):
        old.unlink()
    media_root = project / f"results/media/{method}"
    media_root.mkdir(parents=True, exist_ok=True)
    outputs = {
        "mask": media_root / "mask.mp4",
        "checkerboard_cutout": media_root / "checkerboard-cutout.mp4",
        "graphic_behind": media_root / "graphic-behind.mp4",
        "edge_diagnostics": media_root / "edge-diagnostics.mp4",
        "comparison": media_root / "comparison.mp4",
    }
    if kind == "alpha":
        outputs["cutout_alpha"] = media_root / "cutout-alpha.mov"

    checkerboard = _checkerboard(config.width, config.height)
    foreground_fractions: list[float] = []
    with ExitStack() as stack:
        writers = {
            name: stack.enter_context(
                FFmpegRawWriter(
                    path,
                    width=config.width,
                    height=540 if name == "comparison" else config.height,
                    fps=config.fps,
                    channels=4 if name == "cutout_alpha" else 3,
                )
            )
            for name, path in outputs.items()
        }
        for index, (frame_path, mask_path) in enumerate(zip(input_frames, native_frames)):
            original = np.asarray(Image.open(frame_path).convert("RGB"), dtype=np.uint8)
            native = np.asarray(Image.open(mask_path).convert("L"), dtype=np.uint8)
            mask = normalize_mask(native, (config.width, config.height), kind)
            Image.fromarray(mask, mode="L").save(normalized_root / frame_path.name)
            foreground_fractions.append(float(mask.mean() / 255.0))

            mask_rgb = np.repeat(mask[..., None], 3, axis=2)
            cutout = composite_behind(original, checkerboard, mask)
            graphic = _moving_graphic(original, index, len(input_frames))
            behind = composite_behind(original, graphic, mask)
            diagnostics = _edge_diagnostics(original, mask, config.crops)
            comparison = _comparison(original, behind)
            writers["mask"].write(mask_rgb)
            writers["checkerboard_cutout"].write(cutout)
            writers["graphic_behind"].write(behind)
            writers["edge_diagnostics"].write(diagnostics)
            writers["comparison"].write(comparison)
            if "cutout_alpha" in writers:
                writers["cutout_alpha"].write(np.dstack([original, mask]))

    manifest = {
        "schema_version": 1,
        "method": method,
        "status": "success",
        "kind": kind,
        "input_frames": len(input_frames),
        "normalized_masks": str(normalized_root),
        "normalization": "nearest-neighbor binary" if kind == "binary" else "Lanczos soft alpha",
        "mean_foreground_fraction": float(np.mean(foreground_fractions)),
        "foreground_fraction_stddev": float(np.std(foreground_fractions)),
        "media": {name: str(path) for name, path in outputs.items()},
        "run_record": str(run_path),
    }
    (media_root / "artifacts.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest
