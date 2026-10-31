from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MethodConfig:
    id: str
    label: str
    kind: str


@dataclass(frozen=True)
class BenchmarkConfig:
    path: Path
    schema_version: int
    source: Path
    start_seconds: float
    duration_seconds: float
    width: int
    height: int
    fps: int
    methods: tuple[MethodConfig, ...]
    prompt_box: tuple[float, float, float, float]
    crops: dict[str, tuple[float, float, float, float]]

    @property
    def expected_frames(self) -> int:
        return round(self.duration_seconds * self.fps)

    @property
    def project_root(self) -> Path:
        return self.path.parent

    @property
    def results_root(self) -> Path:
        return self.project_root / "results"


def _rect(value: Any, name: str) -> tuple[float, float, float, float]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{name} must contain four normalized numbers")
    rect = tuple(float(item) for item in value)
    x0, y0, x1_or_width, y1_or_height = rect
    if any(item < 0.0 or item > 1.0 for item in rect):
        raise ValueError(f"{name} values must be between 0 and 1")
    if name == "prompt_box" and (x0 >= x1_or_width or y0 >= y1_or_height):
        raise ValueError("prompt_box must be ordered x0,y0,x1,y1")
    if name != "prompt_box" and (x1_or_width <= 0 or y1_or_height <= 0):
        raise ValueError(f"{name} crop width and height must be positive")
    return rect


def load_config(path: Path) -> BenchmarkConfig:
    path = path.expanduser().resolve()
    data = json.loads(path.read_text())
    if data.get("schema_version") != 1:
        raise ValueError("unsupported benchmark schema_version")

    source_value = Path(data["source"]).expanduser()
    source = (
        source_value.resolve()
        if source_value.is_absolute()
        else (path.parent / source_value).resolve()
    )
    results_root = (path.parent / "results").resolve()
    if source.is_relative_to(results_root):
        raise ValueError("source must be outside results")
    if not source.is_file():
        raise ValueError(f"source does not exist: {source}")

    methods = tuple(
        MethodConfig(
            id=str(method["id"]),
            label=str(method["label"]),
            kind=str(method["kind"]),
        )
        for method in data["methods"]
    )
    if not methods or len({method.id for method in methods}) != len(methods):
        raise ValueError("methods must be non-empty and have unique ids")

    crops = {
        str(name): _rect(value, f"crop {name}")
        for name, value in data["crops"].items()
    }
    config = BenchmarkConfig(
        path=path,
        schema_version=1,
        source=source,
        start_seconds=float(data["start_seconds"]),
        duration_seconds=float(data["duration_seconds"]),
        width=int(data["width"]),
        height=int(data["height"]),
        fps=int(data["fps"]),
        methods=methods,
        prompt_box=_rect(data["prompt_box"], "prompt_box"),
        crops=crops,
    )
    if config.start_seconds < 0 or config.duration_seconds <= 0:
        raise ValueError("excerpt times must be positive")
    if config.width <= 0 or config.height <= 0 or config.fps <= 0:
        raise ValueError("output dimensions and fps must be positive")
    return config
