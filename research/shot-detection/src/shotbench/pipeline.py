from dataclasses import asdict, replace
import json
import os
from pathlib import Path
from typing import Iterable

from .config import BenchmarkManifest
from .detect import DetectionResult, load_detection
from .diagnostics import ScdetEvent
from .export import export_detection
from .report import CandidateGroup, CandidateVote, cluster_votes, write_review_page


def build_vote_groups(
    results: Iterable[DetectionResult],
    diagnostic_events: Iterable[ScdetEvent],
    tolerance_frames: int = 1,
) -> tuple[CandidateGroup, ...]:
    votes = [
        CandidateVote(detector=result.detector_name, frame=frame)
        for result in results
        for frame in result.cut_frames
    ]
    votes.extend(
        CandidateVote(detector="ffmpeg-scdet", frame=event.frame, score=event.score)
        for event in diagnostic_events
    )
    return cluster_votes(votes, tolerance_frames=tolerance_frames)


def select_review_groups(
    groups: Iterable[CandidateGroup],
    primary_detector: str,
) -> tuple[CandidateGroup, ...]:
    selected = []
    for group in groups:
        detectors = {vote.detector for vote in group.votes}
        if primary_detector in detectors or len(detectors) >= 2:
            selected.append(group)
    return tuple(selected)


def _relative(path: Path, start: Path) -> str:
    return os.path.relpath(path, start=start)


def _load_scdet_events(path: Path) -> tuple[ScdetEvent, ...]:
    data = json.loads(path.read_text())
    return tuple(ScdetEvent(**item) for item in data["events"])


def prepare_review(
    manifest: BenchmarkManifest,
    results_dir: Path,
    *,
    primary_detector: str = "adaptive-default",
    cluster_tolerance_frames: int = 1,
) -> Path:
    review_dir = results_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    page_videos: list[dict[str, object]] = []
    review_records: list[dict[str, object]] = []

    for video in manifest.videos:
        detections = tuple(
            load_detection(
                results_dir
                / "candidates"
                / video.id
                / detector.name
                / "detection.json"
            )
            for detector in manifest.detectors
        )
        primary = next(
            (item for item in detections if item.detector_name == primary_detector),
            None,
        )
        if primary is None:
            raise FileNotFoundError(
                f"Primary detector {primary_detector!r} has no result for {video.id}"
            )

        selected_output = results_dir / "selected" / video.id
        selected_artifacts = export_detection(
            primary,
            selected_output,
            include_boundaries=False,
        )
        diagnostic_events = _load_scdet_events(
            results_dir
            / "candidates"
            / video.id
            / "ffmpeg-scdet"
            / "detection.json"
        )
        groups = select_review_groups(
            build_vote_groups(
                detections,
                diagnostic_events,
                tolerance_frames=cluster_tolerance_frames,
            ),
            primary_detector=primary_detector,
        )
        union_result = replace(
            primary,
            detector_name="candidate-union",
            detector_kind="ensemble-review",
            detector_options={"cluster_tolerance_frames": cluster_tolerance_frames},
            scenes=(),
            cut_frames=tuple(group.frame for group in groups),
        )
        review_media_output = results_dir / "review-media" / video.id
        review_artifacts = export_detection(union_result, review_media_output)

        candidates = []
        for index, (group, clip, before, after) in enumerate(
            zip(
                groups,
                review_artifacts.boundary_clips,
                review_artifacts.before_images,
                review_artifacts.after_images,
                strict=True,
            ),
            start=1,
        ):
            candidates.append(
                {
                    "index": index,
                    "frame": group.frame,
                    "seconds": group.frame / primary.fps,
                    "votes": [vote.detector for vote in group.votes],
                    "vote_details": [asdict(vote) for vote in group.votes],
                    "clip": _relative(clip, review_dir),
                    "before": _relative(before, review_dir),
                    "after": _relative(after, review_dir),
                }
            )

        video_record = {
            "video_id": video.id,
            "use_case": video.use_case,
            "source": _relative(video.source, review_dir),
            "primary_detector": primary_detector,
            "scenes": [
                _relative(path, review_dir) for path in selected_artifacts.scene_clips
            ],
            "candidates": candidates,
        }
        page_videos.append(video_record)
        review_records.append(video_record)

    (review_dir / "review-candidates.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "status": "awaiting-human-review",
                "primary_detector": primary_detector,
                "cluster_tolerance_frames": cluster_tolerance_frames,
                "videos": review_records,
            },
            indent=2,
        )
        + "\n"
    )
    return write_review_page(page_videos, review_dir / "index.html")
