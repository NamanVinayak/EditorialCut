import json
from pathlib import Path

from maskbench.methods import (
    apple_command,
    edgetam_command,
    finalize_run_record,
    rvm_command,
)


def test_apple_command_uses_accurate_quality(tmp_path: Path) -> None:
    command = apple_command(
        binary=Path("build/apple-vision-masker"),
        frames=Path("results/prepared/frames"),
        output=tmp_path / "masks",
        metadata=tmp_path / "metadata.json",
    )

    assert command[-2:] == ["--quality", "accurate"]
    assert "results/prepared/frames" in command


def test_finalize_run_record_preserves_failure(tmp_path: Path) -> None:
    metrics = tmp_path / "metrics.json"
    metrics.write_text(json.dumps({
        "argv": ["backend"],
        "returncode": 9,
        "wall_seconds": 1.25,
        "peak_rss_bytes": 1234,
    }))
    stderr = tmp_path / "stderr.log"
    stderr.write_text("backend exploded")

    record = finalize_run_record(
        method="example",
        metrics_path=metrics,
        stderr_path=stderr,
        input_frames=3,
        output_directory=tmp_path / "masks",
        implementation={"version": "1"},
        device="mps",
        settings={"quality": "test"},
        required_input="one box",
    )

    assert record["status"] == "failed"
    assert record["exact_error"] == "backend exploded"
    assert record["input_frames"] == 3
    assert record["output_frames"] == 0


def test_rvm_command_uses_mps_and_official_checkpoint(tmp_path: Path) -> None:
    command = rvm_command(
        python=Path("backends/rvm/.venv/bin/python"),
        script=Path("backends/rvm/run.py"),
        frames=Path("results/prepared/frames"),
        output=tmp_path / "masks",
        metadata=tmp_path / "metadata.json",
        vendor=Path("backends/rvm/vendor/RobustVideoMatting"),
        checkpoint=Path("backends/rvm/checkpoints/rvm_mobilenetv3.pth"),
        device="mps",
    )

    assert command[command.index("--device") + 1] == "mps"
    assert command[command.index("--variant") + 1] == "mobilenetv3"
    assert command[command.index("--checkpoint") + 1].endswith("rvm_mobilenetv3.pth")


def test_edgetam_command_uses_box_and_mps(tmp_path: Path) -> None:
    command = edgetam_command(
        python=Path("backends/edgetam/.venv/bin/python"),
        script=Path("backends/edgetam/run.py"),
        frames=Path("results/prepared/frames"),
        output=tmp_path / "masks",
        work=tmp_path / "work",
        metadata=tmp_path / "metadata.json",
        checkpoint=Path("backends/edgetam/vendor/EdgeTAM/checkpoints/edgetam.pt"),
        box=(0.30, 0.01, 0.70, 0.99),
    )

    assert command[command.index("--device") + 1] == "mps"
    box_start = command.index("--box") + 1
    assert command[box_start:box_start + 4] == ["0.3", "0.01", "0.7", "0.99"]
