from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import BenchmarkConfig


@dataclass(frozen=True)
class FileFingerprint:
    sha256: str
    size: int
    mtime_ns: int

    def as_dict(self) -> dict[str, str | int]:
        return asdict(self)


@dataclass(frozen=True)
class MediaProbe:
    path: Path
    duration: float
    width: int
    height: int
    fps: float
    frame_count: int
    video_codec: str
    has_audio: bool


@dataclass(frozen=True)
class PreparedManifest:
    proxy: Path
    frames: Path
    frame_count: int
    source_fingerprint: FileFingerprint


def expected_frame_count(duration: float, fps: int) -> int:
    return round(duration * fps)


def fingerprint(path: Path) -> FileFingerprint:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    stat = path.stat()
    return FileFingerprint(
        sha256=digest.hexdigest(),
        size=stat.st_size,
        mtime_ns=stat.st_mtime_ns,
    )


def build_proxy_command(config: BenchmarkConfig, output: Path) -> list[str]:
    return [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{config.start_seconds:.6f}",
        "-t",
        f"{config.duration_seconds:.6f}",
        "-i",
        str(config.source),
        "-vf",
        f"scale={config.width}:{config.height}:flags=lanczos,fps={config.fps}",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "16",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-y",
        str(output),
    ]


def probe_media(path: Path) -> MediaProbe:
    completed = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_streams", "-show_format",
            "-of", "json", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)
    video = next(stream for stream in data["streams"] if stream["codec_type"] == "video")
    duration = float(data["format"].get("duration") or video.get("duration") or 0.0)
    rate_text = video.get("avg_frame_rate") or video.get("r_frame_rate") or "0/1"
    fps = float(Fraction(rate_text)) if rate_text != "0/0" else 0.0
    frame_count = int(video.get("nb_frames") or round(duration * fps))
    return MediaProbe(
        path=path.resolve(),
        duration=duration,
        width=int(video["width"]),
        height=int(video["height"]),
        fps=fps,
        frame_count=frame_count,
        video_codec=str(video["codec_name"]),
        has_audio=any(stream["codec_type"] == "audio" for stream in data["streams"]),
    )


def _frame_directory_sha256(frames: list[Path]) -> str:
    digest = hashlib.sha256()
    for frame in frames:
        digest.update(frame.name.encode())
        digest.update(fingerprint(frame).sha256.encode())
    return digest.hexdigest()


def prepare_proxy(config: BenchmarkConfig, results: Path) -> PreparedManifest:
    results = results.resolve()
    prepared = results / "prepared"
    if prepared.exists():
        shutil.rmtree(prepared)
    frames_dir = prepared / "frames"
    frames_dir.mkdir(parents=True)
    proxy = prepared / "source-proxy.mp4"
    source_before = fingerprint(config.source)

    proxy_command = build_proxy_command(config, proxy)
    subprocess.run(proxy_command, check=True)
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(proxy),
            "-start_number", "1", "-vsync", "0", "-y",
            str(frames_dir / "frame_%06d.png"),
        ],
        check=True,
    )
    frames = sorted(frames_dir.glob("frame_*.png"))
    expected = config.expected_frames
    if len(frames) != expected:
        raise RuntimeError(f"prepared frame count {len(frames)} does not equal expected {expected}")
    source_after = fingerprint(config.source)
    if source_after != source_before:
        raise RuntimeError("immutable source changed during preparation")

    probe = probe_media(proxy)
    manifest = {
        "schema_version": 1,
        "source": str(config.source),
        "source_fingerprint": source_before.as_dict(),
        "source_after_fingerprint": source_after.as_dict(),
        "excerpt": {
            "start_seconds": config.start_seconds,
            "duration_seconds": config.duration_seconds,
        },
        "proxy": str(proxy),
        "proxy_probe": {
            "duration": probe.duration,
            "width": probe.width,
            "height": probe.height,
            "fps": probe.fps,
            "frame_count": probe.frame_count,
            "video_codec": probe.video_codec,
            "has_audio": probe.has_audio,
        },
        "proxy_command": proxy_command,
        "frame_count": len(frames),
        "frame_directory_sha256": _frame_directory_sha256(frames),
    }
    (prepared / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return PreparedManifest(
        proxy=proxy,
        frames=frames_dir,
        frame_count=len(frames),
        source_fingerprint=source_before,
    )
