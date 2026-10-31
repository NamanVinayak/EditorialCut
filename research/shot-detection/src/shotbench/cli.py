import argparse
from pathlib import Path
from typing import Iterable, TypeVar

from .config import BenchmarkManifest, load_manifest
from .detect import detect_video
from .diagnostics import run_ffmpeg_scdet
from .pipeline import prepare_review
from .verify import verify_results


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = PROJECT_ROOT / "benchmark.json"
DEFAULT_RESULTS = PROJECT_ROOT / "results"


class SelectionError(ValueError):
    pass


T = TypeVar("T")


def select_by_name(items: Iterable[T], requested: str, label: str) -> T:
    choices = tuple(items)
    for item in choices:
        if getattr(item, "name") == requested:
            return item
    valid = ", ".join(str(getattr(item, "name")) for item in choices)
    raise SelectionError(f"Unknown {label} {requested!r}. Valid choices: {valid}")


def _select_video(manifest: BenchmarkManifest, requested: str):
    for video in manifest.videos:
        if video.id == requested:
            return video
    valid = ", ".join(video.id for video in manifest.videos)
    raise SelectionError(f"Unknown video {requested!r}. Valid choices: {valid}")


def _detect_one(
    manifest: BenchmarkManifest,
    video_id: str,
    detector_name: str,
    results_dir: Path,
    show_progress: bool,
) -> None:
    video = _select_video(manifest, video_id)
    detector = select_by_name(manifest.detectors, detector_name, "detector")
    output = results_dir / "candidates" / video.id / detector.name
    result = detect_video(video, detector, output, show_progress=show_progress)
    print(
        f"{video.id} / {detector.name}: "
        f"{len(result.scenes)} scenes, {len(result.cut_frames)} boundaries, "
        f"{result.elapsed_seconds:.2f}s analysis"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shotbench",
        description="Human-reviewable shot detection benchmark",
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    subparsers = parser.add_subparsers(dest="command", required=True)

    detect_parser = subparsers.add_parser("detect", help="Run one detector on one video")
    detect_parser.add_argument("--video", required=True)
    detect_parser.add_argument("--detector", required=True)
    detect_parser.add_argument("--show-progress", action="store_true")

    benchmark_parser = subparsers.add_parser(
        "benchmark", help="Run every configured detector on every confirmed video"
    )
    benchmark_parser.add_argument("--show-progress", action="store_true")
    subparsers.add_parser(
        "prepare-review",
        help="Export primary scenes and every union candidate into an offline review page",
    )
    subparsers.add_parser("verify", help="Decode-check every generated review artifact")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        manifest = load_manifest(args.manifest)
        if args.command == "detect":
            _detect_one(
                manifest,
                args.video,
                args.detector,
                args.results_dir,
                args.show_progress,
            )
        elif args.command == "benchmark":
            for video in manifest.videos:
                first_result = None
                for detector in manifest.detectors:
                    output = args.results_dir / "candidates" / video.id / detector.name
                    result = detect_video(
                        video,
                        detector,
                        output,
                        show_progress=args.show_progress,
                    )
                    first_result = first_result or result
                    print(
                        f"{video.id} / {detector.name}: "
                        f"{len(result.scenes)} scenes, {len(result.cut_frames)} boundaries, "
                        f"{result.elapsed_seconds:.2f}s analysis"
                    )
                assert first_result is not None
                diagnostic_events = run_ffmpeg_scdet(
                    video.source,
                    first_result.fps,
                    args.results_dir / "candidates" / video.id / "ffmpeg-scdet",
                )
                print(
                    f"{video.id} / ffmpeg-scdet: "
                    f"{len(diagnostic_events)} diagnostic boundary votes"
                )
        elif args.command == "prepare-review":
            page = prepare_review(manifest, args.results_dir)
            print(f"Review page: {page}")
        elif args.command == "verify":
            report = verify_results(args.results_dir)
            print(f"Checked {report.checked} generated artifacts")
            if report.failures:
                for failure in report.failures:
                    print(f"ERROR: {failure}")
                return 1
    except SelectionError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
