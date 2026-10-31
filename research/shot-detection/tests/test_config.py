import json
from pathlib import Path

import pytest

from shotbench.config import ManifestError, load_manifest


def test_load_manifest_resolves_sources_relative_to_manifest(tmp_path: Path) -> None:
    source = tmp_path / "source.mp4"
    source.touch()
    manifest_path = tmp_path / "benchmark.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "videos": [
                    {
                        "id": "sample-01",
                        "source": "source.mp4",
                        "use_case": "camera movement without assumed cuts",
                    }
                ],
                "detectors": [
                    {
                        "name": "adaptive-default",
                        "kind": "adaptive",
                        "adaptive_threshold": 3.0,
                        "min_content_val": 15.0,
                        "window_width": 2,
                        "min_scene_len_seconds": 0.25,
                    }
                ],
            }
        )
    )

    manifest = load_manifest(manifest_path)

    assert manifest.schema_version == 1
    assert manifest.videos[0].id == "sample-01"
    assert manifest.videos[0].source == source.resolve()
    assert manifest.detectors[0].name == "adaptive-default"


def test_load_manifest_rejects_missing_source(tmp_path: Path) -> None:
    manifest_path = tmp_path / "benchmark.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "videos": [
                    {
                        "id": "sample-01",
                        "source": "missing.mp4",
                        "use_case": "camera movement without assumed cuts",
                    }
                ],
                "detectors": [],
            }
        )
    )

    with pytest.raises(ManifestError, match="does not exist"):
        load_manifest(manifest_path)

