from pathlib import Path
import subprocess

from shotbench.detect import DetectionResult, SceneRange
from shotbench.export import boundary_window, export_detection


def test_boundary_window_clamps_to_video_start() -> None:
    window = boundary_window(
        boundary_seconds=0.4,
        duration_seconds=10.0,
        radius_seconds=1.0,
    )

    assert window.start == 0.0
    assert window.end == 1.4


def test_boundary_window_clamps_to_video_end() -> None:
    window = boundary_window(
        boundary_seconds=9.7,
        duration_seconds=10.0,
        radius_seconds=1.0,
    )

    assert window.start == 8.7
    assert window.end == 10.0


def test_export_detection_creates_scene_and_boundary_clips(tmp_path: Path) -> None:
    source = tmp_path / "source.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:s=320x180:r=24:d=2",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(source),
        ],
        check=True,
        capture_output=True,
    )
    result = DetectionResult(
        schema_version=1,
        video_id="synthetic",
        source=str(source),
        use_case="export test",
        detector_name="manual",
        detector_kind="content",
        detector_options={},
        fps=24.0,
        duration_seconds=2.0,
        frame_count=48,
        width=320,
        height=180,
        elapsed_seconds=0.01,
        scenes=(
            SceneRange(0, 24, 0.0, 1.0),
            SceneRange(24, 48, 1.0, 2.0),
        ),
        cut_frames=(24,),
    )

    artifacts = export_detection(result, tmp_path / "exports")

    assert len(artifacts.scene_clips) == 2
    assert len(artifacts.boundary_clips) == 1
    assert len(artifacts.before_images) == 1
    assert len(artifacts.after_images) == 1
    assert all(path.is_file() and path.stat().st_size > 0 for path in artifacts.all_paths())

