from shotbench.detect import DetectionResult
from shotbench.diagnostics import ScdetEvent
from shotbench.pipeline import build_vote_groups, select_review_groups
from shotbench.report import CandidateGroup, CandidateVote


def _result(detector_name: str, cut_frames: tuple[int, ...]) -> DetectionResult:
    return DetectionResult(
        schema_version=1,
        video_id="video-test",
        source="source.mp4",
        use_case="test",
        detector_name=detector_name,
        detector_kind="adaptive",
        detector_options={},
        fps=24.0,
        duration_seconds=10.0,
        frame_count=240,
        width=320,
        height=180,
        elapsed_seconds=0.1,
        scenes=(),
        cut_frames=cut_frames,
    )


def test_build_vote_groups_combines_detector_agreement() -> None:
    groups = build_vote_groups(
        [_result("adaptive", (100, 200)), _result("content", (101,))],
        [ScdetEvent(score=20.0, seconds=100 / 24, frame=100)],
        tolerance_frames=1,
    )

    assert len(groups) == 2
    assert groups[0].frame == 100
    assert {vote.detector for vote in groups[0].votes} == {
        "adaptive",
        "content",
        "ffmpeg-scdet",
    }
    assert groups[1].frame == 200


def test_select_review_groups_keeps_primary_or_multi_detector_candidates() -> None:
    groups = (
        CandidateGroup(100, (CandidateVote("adaptive-default", 100),)),
        CandidateGroup(
            200,
            (CandidateVote("content", 200), CandidateVote("ffmpeg-scdet", 200)),
        ),
        CandidateGroup(300, (CandidateVote("adaptive-sensitive", 300),)),
    )

    selected = select_review_groups(groups, primary_detector="adaptive-default")

    assert [group.frame for group in selected] == [100, 200]
