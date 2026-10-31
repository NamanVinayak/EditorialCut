from __future__ import annotations

import json
from pathlib import Path

from maskbench.verify import check_frame_sequence, check_review_links, check_source_integrity


def test_check_frame_sequence_requires_exact_contiguous_names(tmp_path: Path) -> None:
    for number in (1, 2, 4):
        (tmp_path / f"frame_{number:06d}.png").write_bytes(b"mask")

    result = check_frame_sequence(tmp_path, expected_frames=4)

    assert result["passed"] is False
    assert "frame_000003.png" in result["detail"]


def test_check_review_links_reports_missing_media(tmp_path: Path) -> None:
    review = tmp_path / "results/review"
    review.mkdir(parents=True)
    existing = tmp_path / "results/media/rvm/comparison.mp4"
    existing.parent.mkdir(parents=True)
    existing.write_bytes(b"video")
    (review / "review-data.json").write_text(
        json.dumps(
            {
                "source_proxy": "../prepared/missing.mp4",
                "methods": [
                    {
                        "id": "rvm",
                        "media": {
                            "comparison": "../media/rvm/comparison.mp4",
                            "mask": "../media/rvm/missing.mp4",
                        },
                    }
                ],
            }
        )
    )

    result = check_review_links(review / "review-data.json")

    assert result["passed"] is False
    assert "prepared/missing.mp4" in result["detail"]
    assert "media/rvm/missing.mp4" in result["detail"]


def test_check_source_integrity_uses_recorded_sha_size_and_mtime(tmp_path: Path) -> None:
    source = tmp_path / "source.mp4"
    source.write_bytes(b"immutable source")
    stat = source.stat()
    import hashlib

    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "source": str(source),
                "source_fingerprint": {
                    "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                    "size": stat.st_size,
                    "mtime_ns": stat.st_mtime_ns,
                },
            }
        )
    )

    assert check_source_integrity(manifest)["passed"] is True
    source.write_bytes(b"changed")
    assert check_source_integrity(manifest)["passed"] is False
