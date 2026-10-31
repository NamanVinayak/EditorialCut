import json
from pathlib import Path

import pytest

from maskbench.config import load_config


PROJECT = Path(__file__).resolve().parents[1]


def test_loads_locked_excerpt_and_methods() -> None:
    config = load_config(PROJECT / "benchmark.json")

    assert config.start_seconds == 270.0
    assert config.duration_seconds == 20.0
    assert config.width == 1920
    assert config.height == 1080
    assert config.fps == 30
    assert config.expected_frames == 600
    assert [method.id for method in config.methods] == [
        "apple-vision",
        "rvm",
        "edgetam",
    ]
    assert config.source.name.endswith("sample.mp4")


def test_rejects_source_inside_results(tmp_path: Path) -> None:
    source = tmp_path / "results" / "prepared" / "source.mp4"
    source.parent.mkdir(parents=True)
    source.touch()
    data = {
        "schema_version": 1,
        "source": str(source),
        "start_seconds": 270.0,
        "duration_seconds": 20.0,
        "width": 1920,
        "height": 1080,
        "fps": 30,
        "methods": [{"id": "rvm", "label": "RVM", "kind": "alpha"}],
        "prompt_box": [0.3, 0.01, 0.7, 0.99],
        "crops": {"hair": [0.3, 0.0, 0.3, 0.3]},
    }
    path = tmp_path / "benchmark.json"
    path.write_text(json.dumps(data))

    with pytest.raises(ValueError, match="source must be outside results"):
        load_config(path)


def test_rejects_non_normalized_prompt_box(tmp_path: Path) -> None:
    data = json.loads((PROJECT / "benchmark.json").read_text())
    data["source"] = str(
        PROJECT.parents[2]
        / "media"
        / "test-footage"
        / "sample footage"
    )
    data["prompt_box"] = [0.3, 0.1, 1.2, 0.9]
    path = tmp_path / "benchmark.json"
    path.write_text(json.dumps(data))

    with pytest.raises(ValueError, match="prompt_box"):
        load_config(path)
