import json
import subprocess
from pathlib import Path

from maskbench.config import load_config
from maskbench.media import (
    build_proxy_command,
    expected_frame_count,
    fingerprint,
    prepare_proxy,
    probe_media,
)


PROJECT = Path(__file__).resolve().parents[1]


def test_expected_frame_count_is_exact() -> None:
    assert expected_frame_count(duration=20.0, fps=30) == 600


def test_prepare_command_uses_approved_excerpt() -> None:
    config = load_config(PROJECT / "benchmark.json")
    command = build_proxy_command(config, Path("proxy.mp4"))

    assert command[command.index("-ss") + 1] == "270.000000"
    assert command[command.index("-t") + 1] == "20.000000"
    joined = " ".join(command)
    assert "scale=1920:1080:flags=lanczos,fps=30" in joined
    assert "libx264" in joined
    assert "-an" in command


def test_fingerprint_changes_when_content_changes(tmp_path: Path) -> None:
    path = tmp_path / "source.bin"
    path.write_bytes(b"first")
    before = fingerprint(path)
    path.write_bytes(b"second")
    after = fingerprint(path)

    assert before.sha256 != after.sha256
    assert before.size != after.size


def test_prepare_proxy_preserves_source_and_extracts_exact_frames(tmp_path: Path) -> None:
    source = tmp_path / "source.mp4"
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "testsrc2=size=64x64:rate=5",
            "-t", "1", "-pix_fmt", "yuv420p", "-y", str(source),
        ],
        check=True,
    )
    before = fingerprint(source)
    config_data = {
        "schema_version": 1,
        "source": str(source),
        "start_seconds": 0,
        "duration_seconds": 1,
        "width": 64,
        "height": 64,
        "fps": 5,
        "methods": [{"id": "rvm", "label": "RVM", "kind": "alpha"}],
        "prompt_box": [0.1, 0.1, 0.9, 0.9],
        "crops": {"hair": [0.1, 0.1, 0.5, 0.5]},
    }
    config_path = tmp_path / "benchmark.json"
    config_path.write_text(json.dumps(config_data))
    config = load_config(config_path)

    manifest = prepare_proxy(config, tmp_path / "results")

    assert manifest.frame_count == 5
    assert len(list((tmp_path / "results/prepared/frames").glob("*.png"))) == 5
    assert probe_media(manifest.proxy).width == 64
    assert fingerprint(source) == before
