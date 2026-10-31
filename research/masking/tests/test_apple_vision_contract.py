import json
import subprocess
from pathlib import Path

from PIL import Image


PROJECT = Path(__file__).resolve().parents[1]
BINARY = PROJECT / "build/apple-vision-masker"


def test_apple_vision_preserves_names_and_count(tmp_path: Path) -> None:
    assert BINARY.is_file(), "compile build/apple-vision-masker first"
    inputs = tmp_path / "frames"
    outputs = tmp_path / "masks"
    metadata = tmp_path / "metadata.json"
    inputs.mkdir()
    for number in range(1, 4):
        Image.new("RGB", (64, 48), (20 * number, 40, 80)).save(
            inputs / f"frame_{number:06d}.png"
        )

    completed = subprocess.run(
        [
            str(BINARY),
            "--input-dir", str(inputs),
            "--output-dir", str(outputs),
            "--metadata", str(metadata),
            "--quality", "accurate",
        ],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert [path.name for path in sorted(outputs.glob("*.png"))] == [
        "frame_000001.png",
        "frame_000002.png",
        "frame_000003.png",
    ]
    stored = json.loads(metadata.read_text())
    assert stored["processed_frames"] == 3
    assert stored["quality"] == "accurate"
    assert len(stored["frame_results"]) == 3


def test_apple_vision_rejects_unknown_quality(tmp_path: Path) -> None:
    assert BINARY.is_file(), "compile build/apple-vision-masker first"
    completed = subprocess.run(
        [
            str(BINARY),
            "--input-dir", str(tmp_path),
            "--output-dir", str(tmp_path / "out"),
            "--metadata", str(tmp_path / "meta.json"),
            "--quality", "imaginary",
        ],
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "quality" in completed.stderr.lower()
