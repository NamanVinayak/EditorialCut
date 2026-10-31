from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


class ManifestError(ValueError):
    """Raised when a benchmark manifest is unsafe or incomplete."""


@dataclass(frozen=True)
class BenchmarkVideo:
    id: str
    source: Path
    use_case: str


@dataclass(frozen=True)
class DetectorConfig:
    name: str
    kind: str
    min_scene_len_seconds: float
    options: dict[str, int | float]


@dataclass(frozen=True)
class BenchmarkManifest:
    schema_version: int
    videos: tuple[BenchmarkVideo, ...]
    detectors: tuple[DetectorConfig, ...]


def _required(item: dict[str, Any], key: str, context: str) -> Any:
    if key not in item:
        raise ManifestError(f"{context} is missing required field {key!r}")
    return item[key]


def load_manifest(path: Path) -> BenchmarkManifest:
    path = path.resolve()
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"Could not read benchmark manifest {path}: {exc}") from exc

    if data.get("schema_version") != 1:
        raise ManifestError("Only benchmark schema_version 1 is supported")

    videos: list[BenchmarkVideo] = []
    seen_video_ids: set[str] = set()
    for index, item in enumerate(data.get("videos", []), start=1):
        context = f"video entry {index}"
        video_id = str(_required(item, "id", context))
        if video_id in seen_video_ids:
            raise ManifestError(f"Duplicate video id: {video_id}")
        seen_video_ids.add(video_id)
        source = (path.parent / str(_required(item, "source", context))).resolve()
        if not source.is_file():
            raise ManifestError(f"Source for {video_id} does not exist: {source}")
        videos.append(
            BenchmarkVideo(
                id=video_id,
                source=source,
                use_case=str(_required(item, "use_case", context)),
            )
        )

    detectors: list[DetectorConfig] = []
    seen_detector_names: set[str] = set()
    for index, item in enumerate(data.get("detectors", []), start=1):
        context = f"detector entry {index}"
        name = str(_required(item, "name", context))
        kind = str(_required(item, "kind", context))
        if name in seen_detector_names:
            raise ManifestError(f"Duplicate detector name: {name}")
        if kind not in {"adaptive", "content"}:
            raise ManifestError(f"Unsupported detector kind {kind!r} for {name}")
        seen_detector_names.add(name)
        ignored = {"name", "kind", "min_scene_len_seconds"}
        options = {key: value for key, value in item.items() if key not in ignored}
        detectors.append(
            DetectorConfig(
                name=name,
                kind=kind,
                min_scene_len_seconds=float(item.get("min_scene_len_seconds", 0.25)),
                options=options,
            )
        )

    if not videos:
        raise ManifestError("Benchmark manifest contains no videos")
    return BenchmarkManifest(
        schema_version=1,
        videos=tuple(videos),
        detectors=tuple(detectors),
    )
