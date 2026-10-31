from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import subprocess


SCDET_PATTERN = re.compile(
    r"lavfi\.scd\.score:\s*(?P<score>[0-9.]+),\s*"
    r"lavfi\.scd\.time:\s*(?P<time>[0-9.]+)"
)


@dataclass(frozen=True)
class ScdetEvent:
    score: float
    seconds: float
    frame: int


def parse_scdet_log(log: str, fps: float) -> tuple[ScdetEvent, ...]:
    if fps <= 0:
        raise ValueError("fps must be positive")
    events = []
    for match in SCDET_PATTERN.finditer(log):
        seconds = float(match.group("time"))
        events.append(
            ScdetEvent(
                score=float(match.group("score")),
                seconds=seconds,
                frame=round(seconds * fps),
            )
        )
    return tuple(events)


def run_ffmpeg_scdet(
    source: Path,
    fps: float,
    output_dir: Path,
    *,
    threshold: float = 10.0,
) -> tuple[ScdetEvent, ...]:
    output_dir.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(source),
            "-filter:v",
            f"scdet=threshold={threshold}",
            "-an",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    (output_dir / "ffmpeg.log").write_text(completed.stderr)
    if completed.returncode != 0:
        raise RuntimeError(f"FFmpeg scdet failed for {source}: {completed.stderr}")
    events = parse_scdet_log(completed.stderr, fps=fps)
    (output_dir / "detection.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "source": str(source),
                "detector_name": "ffmpeg-scdet",
                "threshold": threshold,
                "fps": fps,
                "events": [asdict(event) for event in events],
            },
            indent=2,
        )
        + "\n"
    )
    return events
