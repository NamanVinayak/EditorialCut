from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from .media import fingerprint, probe_media


def _check(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "detail": detail}


def check_frame_sequence(directory: Path, expected_frames: int) -> dict[str, Any]:
    paths = sorted(directory.glob("frame_*.png")) if directory.is_dir() else []
    actual = [path.name for path in paths]
    expected = [f"frame_{number:06d}.png" for number in range(1, expected_frames + 1)]
    if actual == expected:
        return _check(str(directory), True, f"exact contiguous sequence of {expected_frames} frames")
    missing = [name for name in expected if name not in set(actual)]
    extra = [name for name in actual if name not in set(expected)]
    parts = [f"expected {expected_frames}, found {len(actual)}"]
    if missing:
        parts.append("missing " + ", ".join(missing[:8]))
    if extra:
        parts.append("unexpected " + ", ".join(extra[:8]))
    return _check(str(directory), False, "; ".join(parts))


def check_review_links(data_path: Path) -> dict[str, Any]:
    if not data_path.is_file():
        return _check("review links", False, f"missing {data_path}")
    data = json.loads(data_path.read_text())
    relative_paths = [str(data.get("source_proxy", ""))]
    for method in data.get("methods", []):
        relative_paths.extend(str(value) for value in method.get("media", {}).values())
    missing = [value for value in relative_paths if not value or not (data_path.parent / value).resolve().is_file()]
    if missing:
        return _check("review links", False, "missing: " + ", ".join(missing))
    return _check("review links", True, f"all {len(relative_paths)} local media links resolve")


def check_source_integrity(manifest_path: Path) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text())
    source = Path(manifest["source"])
    recorded = manifest["source_fingerprint"]
    if not source.is_file():
        return _check("source integrity", False, f"source missing: {source}")
    current = fingerprint(source).as_dict()
    passed = current == recorded
    detail = "SHA-256, byte size, and modification time unchanged" if passed else f"recorded={recorded}, current={current}"
    return _check("source integrity", passed, detail)


def _stream_details(path: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=codec_name,codec_tag_string,pix_fmt,width,height,avg_frame_rate,nb_frames,duration",
            "-of", "json", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    streams = json.loads(completed.stdout).get("streams", [])
    if not streams:
        raise RuntimeError(f"no video stream in {path}")
    return streams[0]


def _check_video(
    path: Path,
    *,
    width: int,
    height: int,
    fps: int,
    frames: int,
    alpha: bool = False,
) -> dict[str, Any]:
    name = f"media {path.relative_to(path.parents[3])}" if len(path.parents) > 3 else f"media {path}"
    try:
        probe = probe_media(path)
        stream = _stream_details(path)
    except Exception as error:
        return _check(name, False, f"probe failed: {error}")
    conditions = {
        "dimensions": (probe.width, probe.height) == (width, height),
        "fps": abs(probe.fps - fps) < 0.001,
        "frames": probe.frame_count == frames,
        "duration": abs(probe.duration - (frames / fps)) < 0.05,
        "silent": not probe.has_audio,
    }
    if alpha:
        conditions["alpha"] = str(stream.get("codec_tag_string")) == "ap4h" and str(stream.get("pix_fmt", "")).startswith("yuva")
    passed = all(conditions.values())
    detail = (
        f"{probe.width}x{probe.height}, {probe.fps:.3f} fps, {probe.frame_count} frames, "
        f"{probe.duration:.3f}s, {stream.get('codec_name')}/{stream.get('pix_fmt')}; "
        + ", ".join(f"{key}={'ok' if value else 'FAIL'}" for key, value in conditions.items())
    )
    return _check(name, passed, detail)


def verify_project(project: Path) -> dict[str, Any]:
    project = project.resolve()
    expected_frames = 600
    width, height, fps = 1920, 1080, 30
    checks: list[dict[str, Any]] = []
    prepared_manifest = project / "results/prepared/manifest.json"
    checks.append(check_source_integrity(prepared_manifest))
    checks.append(check_frame_sequence(project / "results/prepared/frames", expected_frames))
    checks.append(
        _check_video(
            project / "results/prepared/source-proxy.mp4",
            width=width,
            height=height,
            fps=fps,
            frames=expected_frames,
        )
    )

    method_ids = ("apple-vision", "rvm", "edgetam")
    expected_views = ("mask", "checkerboard_cutout", "graphic_behind", "edge_diagnostics", "comparison")
    for method_id in method_ids:
        run_path = project / f"results/methods/{method_id}/run.json"
        try:
            run = json.loads(run_path.read_text())
            run_ok = run.get("status") == "success" and run.get("output_frames") == expected_frames
            checks.append(_check(f"{method_id} run record", run_ok, f"status={run.get('status')}, outputs={run.get('output_frames')}"))
        except Exception as error:
            checks.append(_check(f"{method_id} run record", False, str(error)))
            continue
        checks.append(check_frame_sequence(project / f"results/methods/{method_id}/native", expected_frames))
        checks.append(check_frame_sequence(project / f"results/methods/{method_id}/normalized", expected_frames))
        manifest_path = project / f"results/media/{method_id}/artifacts.json"
        try:
            manifest = json.loads(manifest_path.read_text())
            manifest_ok = manifest.get("status") == "success" and manifest.get("input_frames") == expected_frames
            checks.append(_check(f"{method_id} media manifest", manifest_ok, f"status={manifest.get('status')}, inputs={manifest.get('input_frames')}"))
            media = manifest.get("media", {})
        except Exception as error:
            checks.append(_check(f"{method_id} media manifest", False, str(error)))
            continue
        for view in expected_views:
            value = media.get(view)
            if not value:
                checks.append(_check(f"{method_id} {view}", False, "missing from media manifest"))
                continue
            path = Path(value)
            checks.append(
                _check_video(
                    path,
                    width=width,
                    height=540 if view == "comparison" else height,
                    fps=fps,
                    frames=expected_frames,
                )
            )
        alpha_value = media.get("cutout_alpha")
        if method_id in ("apple-vision", "rvm"):
            if not alpha_value:
                checks.append(_check(f"{method_id} alpha export", False, "missing from media manifest"))
            else:
                checks.append(
                    _check_video(Path(alpha_value), width=width, height=height, fps=fps, frames=expected_frames, alpha=True)
                )
        else:
            checks.append(_check("edgetam alpha export", alpha_value is None, "correctly omitted for hard binary mask"))

    checks.append(check_review_links(project / "results/review/review-data.json"))
    html_path = project / "results/review/index.html"
    html_ok = html_path.is_file() and "Mask Tracking Review" in html_path.read_text()
    checks.append(_check("review HTML", html_ok, str(html_path)))
    result = {
        "schema_version": 1,
        "status": "passed" if all(item["passed"] for item in checks) else "failed",
        "passed": sum(1 for item in checks if item["passed"]),
        "failed": sum(1 for item in checks if not item["passed"]),
        "checks": checks,
    }
    output = project / "results/verification.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    return result
