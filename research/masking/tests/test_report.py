from __future__ import annotations

import json
from pathlib import Path

from maskbench.report import build_review


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def test_build_review_contains_methods_views_and_editor_rubric(tmp_path: Path) -> None:
    project = tmp_path
    (project / "results/prepared").mkdir(parents=True)
    (project / "results/prepared/source-proxy.mp4").write_bytes(b"video")
    methods = (
        ("apple-vision", "Apple Vision", "automatic person matte"),
        ("rvm", "Robust Video Matting", "recurrent temporal matte"),
        ("edgetam", "EdgeTAM", "prompted tracked selection"),
    )
    for method_id, label, required_input in methods:
        media = project / f"results/media/{method_id}"
        media.mkdir(parents=True)
        paths = {}
        for view in ("mask", "checkerboard_cutout", "graphic_behind", "edge_diagnostics", "comparison"):
            filename = view.replace("_", "-") + ".mp4"
            (media / filename).write_bytes(b"video")
            paths[view] = str(media / filename)
        _write_json(
            media / "artifacts.json",
            {
                "method": method_id,
                "status": "success",
                "kind": "binary" if method_id == "edgetam" else "alpha",
                "media": paths,
            },
        )
        _write_json(
            project / f"results/methods/{method_id}/run.json",
            {
                "method": method_id,
                "status": "success",
                "wall_seconds": 12.5,
                "peak_rss_bytes": 1024,
                "required_input": required_input,
                "warnings": [],
            },
        )

    result = build_review(project)

    html = result["html"].read_text()
    data = json.loads(result["data"].read_text())
    assert "Mask Tracking Review" in html
    assert "Apple Vision" in html
    assert "Robust Video Matting" in html
    assert "EdgeTAM" in html
    assert "Graphic behind subject" in html
    assert "Edge diagnostics" in html
    assert "Download review JSON" in html
    assert "localStorage" in html
    for criterion in ("overall", "hair", "hands", "shoulders_mic", "flicker", "tracking"):
        assert criterion in html
    assert len(data["methods"]) == 3
    assert data["methods"][2]["job"] == "prompted tracked selection"
    assert data["methods"][0]["media"]["comparison"] == "../media/apple-vision/comparison.mp4"


def test_build_review_keeps_failed_method_visible(tmp_path: Path) -> None:
    project = tmp_path
    (project / "results/prepared").mkdir(parents=True)
    (project / "results/prepared/source-proxy.mp4").write_bytes(b"video")
    _write_json(
        project / "results/methods/rvm/run.json",
        {
            "method": "rvm",
            "status": "failed",
            "exact_error": "model failed clearly",
            "wall_seconds": 3.0,
            "peak_rss_bytes": 0,
            "required_input": "automatic",
            "warnings": [],
        },
    )

    result = build_review(project)
    data = json.loads(result["data"].read_text())

    assert data["methods"][0]["status"] == "failed"
    assert data["methods"][0]["error"] == "model failed clearly"
    assert "model failed clearly" in result["html"].read_text()
