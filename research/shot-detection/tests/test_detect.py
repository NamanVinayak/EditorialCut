from pathlib import Path
import subprocess

from shotbench.config import BenchmarkVideo, DetectorConfig
from shotbench.detect import detect_video, normalize_scene_pairs


def test_normalize_scene_pairs_uses_end_exclusive_frames() -> None:
    result = normalize_scene_pairs([(0, 24), (24, 48)], fps=24.0)

    assert result.scenes[0].start_frame == 0
    assert result.scenes[0].end_frame == 24
    assert result.scenes[0].start_seconds == 0.0
    assert result.scenes[0].end_seconds == 1.0
    assert result.cut_frames == (24,)


def test_normalize_scene_pairs_keeps_single_scene_without_cuts() -> None:
    result = normalize_scene_pairs([(0, 90)], fps=30.0)

    assert len(result.scenes) == 1
    assert result.cut_frames == ()
    assert result.scenes[0].end_seconds == 3.0


def test_detect_video_finds_synthetic_hard_cut(tmp_path: Path) -> None:
    source = tmp_path / "two-colors.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=red:s=320x180:r=24:d=1",
            "-f",
            "lavfi",
            "-i",
            "color=c=blue:s=320x180:r=24:d=1",
            "-filter_complex",
            "[0:v][1:v]concat=n=2:v=1:a=0",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(source),
        ],
        check=True,
        capture_output=True,
    )
    video = BenchmarkVideo(id="synthetic", source=source, use_case="test hard cut")
    detector = DetectorConfig(
        name="content-test",
        kind="content",
        min_scene_len_seconds=0.1,
        options={"threshold": 10.0},
    )

    result = detect_video(video, detector, tmp_path / "result")

    assert result.video_id == "synthetic"
    assert result.fps == 24.0
    assert any(abs(frame - 24) <= 1 for frame in result.cut_frames)
    assert (tmp_path / "result" / "detection.json").is_file()
