from pathlib import Path

from shotbench.report import CandidateVote, cluster_votes, render_review_page


def test_cluster_votes_groups_nearby_detectors_without_merging_same_detector() -> None:
    groups = cluster_votes(
        [
            CandidateVote(detector="adaptive", frame=100),
            CandidateVote(detector="content", frame=101),
            CandidateVote(detector="adaptive", frame=102),
        ],
        tolerance_frames=2,
    )

    assert len(groups) == 2
    assert groups[0].frame == 100
    assert {vote.detector for vote in groups[0].votes} == {"adaptive", "content"}
    assert groups[1].votes[0].frame == 102


def test_render_review_page_contains_editorial_context_and_media() -> None:
    html = render_review_page(
        [
            {
                "video_id": "sample-15",
                "use_case": "cut hidden inside fast movement",
                "source": "sources/sample-15.mp4",
                "scenes": ["selected/sample-15/scenes/scene-001.mp4"],
                "candidates": [
                    {
                        "index": 1,
                        "frame": 24,
                        "seconds": 1.0,
                        "votes": ["adaptive-default", "content-baseline"],
                        "clip": "media/sample-15/boundary-001.mp4",
                        "before": "media/sample-15/before.jpg",
                        "after": "media/sample-15/after.jpg",
                    }
                ],
            }
        ],
        output_path=Path("index.html"),
    )

    assert "cut hidden inside fast movement" in html
    assert "media/sample-15/boundary-001.mp4" in html
    assert "Download review JSON" in html
    assert "Real cut" in html

