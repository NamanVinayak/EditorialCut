from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Boundary:
    kind: str
    start_frame: int
    end_frame: int

    @classmethod
    def hard_cut(cls, frame: int) -> "Boundary":
        if frame < 0:
            raise ValueError("Boundary frames cannot be negative")
        return cls(kind="hard_cut", start_frame=frame, end_frame=frame)

    @classmethod
    def transition(cls, start_frame: int, end_frame: int) -> "Boundary":
        if start_frame < 0 or end_frame < start_frame:
            raise ValueError("Transition frame range is invalid")
        return cls(kind="transition", start_frame=start_frame, end_frame=end_frame)


@dataclass(frozen=True)
class BoundaryMatch:
    predicted_frame: int
    label: Boundary
    distance_frames: int


@dataclass(frozen=True)
class Score:
    matched: int
    false_positive: int
    missed: int
    precision: float
    recall: float
    f1: float
    matches: tuple[BoundaryMatch, ...]
    unmatched_predictions: tuple[int, ...]
    unmatched_labels: tuple[Boundary, ...]


def _distance_to_boundary(frame: int, boundary: Boundary) -> int:
    if boundary.start_frame <= frame <= boundary.end_frame:
        return 0
    return min(abs(frame - boundary.start_frame), abs(frame - boundary.end_frame))


def score_boundaries(
    predicted_frames: Sequence[int] | Iterable[int],
    labels: Sequence[Boundary] | Iterable[Boundary],
    tolerance_frames: int,
) -> Score:
    if tolerance_frames < 0:
        raise ValueError("tolerance_frames cannot be negative")

    predictions = tuple(sorted(int(frame) for frame in predicted_frames))
    ordered_labels = tuple(sorted(labels, key=lambda item: (item.start_frame, item.end_frame)))
    unmatched_label_indexes = set(range(len(ordered_labels)))
    matches: list[BoundaryMatch] = []
    unmatched_predictions: list[int] = []

    for prediction in predictions:
        candidates = []
        for index in unmatched_label_indexes:
            distance = _distance_to_boundary(prediction, ordered_labels[index])
            if distance <= tolerance_frames:
                candidates.append((distance, ordered_labels[index].start_frame, index))
        if not candidates:
            unmatched_predictions.append(prediction)
            continue
        distance, _, selected_index = min(candidates)
        selected_label = ordered_labels[selected_index]
        unmatched_label_indexes.remove(selected_index)
        matches.append(
            BoundaryMatch(
                predicted_frame=prediction,
                label=selected_label,
                distance_frames=distance,
            )
        )

    unmatched_labels = tuple(ordered_labels[index] for index in sorted(unmatched_label_indexes))
    matched = len(matches)
    precision = matched / len(predictions) if predictions else (1.0 if not ordered_labels else 0.0)
    recall = matched / len(ordered_labels) if ordered_labels else (1.0 if not predictions else 0.0)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return Score(
        matched=matched,
        false_positive=len(unmatched_predictions),
        missed=len(unmatched_labels),
        precision=precision,
        recall=recall,
        f1=f1,
        matches=tuple(matches),
        unmatched_predictions=tuple(unmatched_predictions),
        unmatched_labels=unmatched_labels,
    )
