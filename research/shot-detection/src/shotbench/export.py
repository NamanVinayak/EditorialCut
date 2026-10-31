from dataclasses import asdict, dataclass
import json
from pathlib import Path
import subprocess
from typing import Iterable

from .detect import DetectionResult


@dataclass(frozen=True)
class TimeWindow:
    start: float
    end: float


@dataclass(frozen=True)
class ExportedArtifacts:
    scene_clips: tuple[Path, ...]
    boundary_clips: tuple[Path, ...]
    before_images: tuple[Path, ...]
    after_images: tuple[Path, ...]
    manifest: Path

    def all_paths(self) -> tuple[Path, ...]:
        return (
            *self.scene_clips,
            *self.boundary_clips,
            *self.before_images,
            *self.after_images,
            self.manifest,
        )


def boundary_window(
    boundary_seconds: float,
    duration_seconds: float,
    radius_seconds: float = 1.0,
) -> TimeWindow:
    if duration_seconds <= 0 or radius_seconds <= 0:
        raise ValueError("Duration and radius must be positive")
    start = max(0.0, boundary_seconds - radius_seconds)
    end = min(duration_seconds, boundary_seconds + radius_seconds)
    return TimeWindow(start=start, end=end)


def _run_ffmpeg(arguments: Iterable[str]) -> None:
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *arguments]
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(
            f"FFmpeg failed ({completed.returncode}): {' '.join(command)}\n{completed.stderr}"
        )


def _export_clip(source: Path, start: float, end: float, output: Path) -> None:
    duration = end - start
    if duration <= 0:
        raise ValueError(f"Clip duration must be positive: {start} to {end}")
    _run_ffmpeg(
        [
            "-ss",
            f"{start:.6f}",
            "-i",
            str(source),
            "-t",
            f"{duration:.6f}",
            "-map",
            "0:v:0",
            "-map",
            "0:a?",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "veryfast",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )


def _export_frame(source: Path, frame: int, output: Path) -> None:
    frame = max(0, frame)
    _run_ffmpeg(
        [
            "-i",
            str(source),
            "-vf",
            f"select=eq(n\\,{frame})",
            "-frames:v",
            "1",
            "-fps_mode",
            "vfr",
            "-q:v",
            "2",
            str(output),
        ]
    )


def export_detection(
    result: DetectionResult,
    output_dir: Path,
    *,
    boundary_radius_seconds: float = 1.0,
    include_scenes: bool = True,
    include_boundaries: bool = True,
) -> ExportedArtifacts:
    source = Path(result.source)
    if not source.is_file():
        raise FileNotFoundError(source)
    scene_dir = output_dir / "scenes"
    boundary_dir = output_dir / "boundaries"
    still_dir = output_dir / "boundary-stills"
    for directory in (scene_dir, boundary_dir, still_dir):
        directory.mkdir(parents=True, exist_ok=True)

    scene_clips: list[Path] = []
    if include_scenes:
        for index, scene in enumerate(result.scenes, start=1):
            output = scene_dir / (
                f"scene-{index:03d}_f{scene.start_frame:06d}-f{scene.end_frame:06d}.mp4"
            )
            _export_clip(source, scene.start_seconds, scene.end_seconds, output)
            scene_clips.append(output)

    boundary_clips: list[Path] = []
    before_images: list[Path] = []
    after_images: list[Path] = []
    boundary_records: list[dict[str, object]] = []
    boundary_frames = result.cut_frames if include_boundaries else ()
    for index, frame in enumerate(boundary_frames, start=1):
        seconds = frame / result.fps
        window = boundary_window(
            seconds,
            result.duration_seconds,
            radius_seconds=boundary_radius_seconds,
        )
        clip = boundary_dir / f"boundary-{index:03d}_f{frame:06d}_{seconds:010.3f}s.mp4"
        before = still_dir / f"boundary-{index:03d}_before_f{max(0, frame - 1):06d}.jpg"
        after = still_dir / f"boundary-{index:03d}_after_f{frame:06d}.jpg"
        _export_clip(source, window.start, window.end, clip)
        _export_frame(source, frame - 1, before)
        _export_frame(source, frame, after)
        boundary_clips.append(clip)
        before_images.append(before)
        after_images.append(after)
        boundary_records.append(
            {
                "index": index,
                "frame": frame,
                "seconds": seconds,
                "clip": str(clip.relative_to(output_dir)),
                "before_image": str(before.relative_to(output_dir)),
                "after_image": str(after.relative_to(output_dir)),
            }
        )

    manifest_path = output_dir / "artifacts.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "video_id": result.video_id,
                "detector_name": result.detector_name,
                "source": result.source,
                "scenes": (
                    [
                        {
                            **asdict(scene),
                            "clip": str(path.relative_to(output_dir)),
                        }
                        for scene, path in zip(result.scenes, scene_clips, strict=True)
                    ]
                    if include_scenes
                    else []
                ),
                "boundaries": boundary_records,
            },
            indent=2,
        )
        + "\n"
    )
    return ExportedArtifacts(
        scene_clips=tuple(scene_clips),
        boundary_clips=tuple(boundary_clips),
        before_images=tuple(before_images),
        after_images=tuple(after_images),
        manifest=manifest_path,
    )
