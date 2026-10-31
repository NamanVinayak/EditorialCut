import pytest

from shotbench.metrics import Boundary, score_boundaries


def test_hard_cut_within_two_frames_matches() -> None:
    score = score_boundaries(
        predicted_frames=[102],
        labels=[Boundary.hard_cut(100)],
        tolerance_frames=2,
    )

    assert score.matched == 1
    assert score.false_positive == 0
    assert score.missed == 0
    assert score.f1 == 1.0


def test_prediction_inside_transition_interval_matches() -> None:
    score = score_boundaries(
        predicted_frames=[205],
        labels=[Boundary.transition(200, 210)],
        tolerance_frames=0,
    )

    assert score.matched == 1
    assert score.matches[0].label.kind == "transition"


def test_false_positive_and_missed_boundary_are_counted() -> None:
    score = score_boundaries(
        predicted_frames=[100, 300],
        labels=[Boundary.hard_cut(100), Boundary.hard_cut(500)],
        tolerance_frames=2,
    )

    assert score.matched == 1
    assert score.false_positive == 1
    assert score.missed == 1
    assert score.precision == pytest.approx(0.5)
    assert score.recall == pytest.approx(0.5)
    assert score.f1 == pytest.approx(0.5)


def test_empty_predictions_and_labels_are_perfectly_consistent() -> None:
    score = score_boundaries([], [], tolerance_frames=2)

    assert score.precision == 1.0
    assert score.recall == 1.0
    assert score.f1 == 1.0

