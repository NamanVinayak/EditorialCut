from dataclasses import asdict, dataclass
import json
from pathlib import Path
import time
from typing import Any, Iterable

from scenedetect import SceneManager, StatsManager, open_video
from scenedetect.detectors import AdaptiveDetector, ContentDetector

from .config import BenchmarkVideo, DetectorConfig


@dataclass(frozen=True)
class SceneRange:
    start_frame: int
    end_frame: int
    start_seconds: float
    end_seconds: float


@dataclass(frozen=True)
class NormalizedScenes:
    scenes: tuple[SceneRange, ...]
    cut_frames: tuple[int, ...]


@dataclass(frozen=True)
class DetectionResult:
    schema_version: int
    video_id: str
    source: str
    use_case: str
    detector_name: str
    detector_kind: str
    detector_options: dict[str, int | float]
    fps: float
    duration_seconds: float
    frame_count: int
    width: int
    height: int
    elapsed_seconds: float
    scenes: tuple[SceneRange, ...]
    cut_frames: tuple[int, ...]


def _frame_number(value: Any) -> int:
    if hasattr(value, "frame_num"):
        return int(value.frame_num)
    if hasattr(value, "get_frames"):
        return int(value.get_frames())
    return int(value)


def normalize_scene_pairs(scene_pairs: Iterable[tuple[Any, Any]], fps: float) -> NormalizedScenes:
    if fps <= 0:
        raise ValueError("fps must be positive")
    scenes = tuple(
        SceneRange(
            start_frame=_frame_number(start),
            end_frame=_frame_number(end),
            start_seconds=_frame_number(start) / fps,
            end_seconds=_frame_number(end) / fps,
        )
        for start, end in scene_pairs
    )
    return NormalizedScenes(
        scenes=scenes,
        cut_frames=tuple(scene.start_frame for scene in scenes[1:]),
    )


def _make_detector(config: DetectorConfig):
    if config.kind == "adaptive":
        return AdaptiveDetector(
            adaptive_threshold=float(config.options.get("adaptive_threshold", 3.0)),
            min_content_val=float(config.options.get("min_content_val", 15.0)),
            window_width=int(config.options.get("window_width", 2)),
            min_scene_len=config.min_scene_len_seconds,
        )
    if config.kind == "content":
        return ContentDetector(
            threshold=float(config.options.get("threshold", 27.0)),
            min_scene_len=config.min_scene_len_seconds,
        )
    raise ValueError(f"Unsupported detector kind: {config.kind}")


def detect_video(
    video: BenchmarkVideo,
    detector_config: DetectorConfig,
    output_dir: Path,
    *,
    show_progress: bool = False,
) -> DetectionResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    stream = open_video(str(video.source))
    stats = StatsManager()
    manager = SceneManager(stats_manager=stats)
    manager.add_detector(_make_detector(detector_config))

    started = time.perf_counter()
    manager.detect_scenes(video=stream, show_progress=show_progress)
    elapsed = time.perf_counter() - started
    scene_pairs = manager.get_scene_list(start_in_scene=True)
    normalized = normalize_scene_pairs(scene_pairs, fps=float(stream.frame_rate))
    stats.save_to_csv(output_dir / "frame-stats.csv")

    width, height = stream.frame_size
    duration = stream.duration
    result = DetectionResult(
        schema_version=1,
        video_id=video.id,
        source=str(video.source),
        use_case=video.use_case,
        detector_name=detector_config.name,
        detector_kind=detector_config.kind,
        detector_options={
            "min_scene_len_seconds": detector_config.min_scene_len_seconds,
            **detector_config.options,
        },
        fps=float(stream.frame_rate),
        duration_seconds=float(duration.seconds),
        frame_count=int(duration.frame_num),
        width=int(width),
        height=int(height),
        elapsed_seconds=elapsed,
        scenes=normalized.scenes,
        cut_frames=normalized.cut_frames,
    )
    (output_dir / "detection.json").write_text(
        json.dumps(asdict(result), indent=2) + "\n"
    )
    return result


def load_detection(path: Path) -> DetectionResult:
    data = json.loads(path.read_text())
    scenes = tuple(SceneRange(**scene) for scene in data.pop("scenes"))
    data["cut_frames"] = tuple(data["cut_frames"])
    return DetectionResult(scenes=scenes, **data)
