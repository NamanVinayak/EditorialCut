from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

from .execute import run_measured
from .media import fingerprint


def apple_command(
    *,
    binary: Path,
    frames: Path,
    output: Path,
    metadata: Path,
) -> list[str]:
    return [
        str(binary),
        "--input-dir", str(frames),
        "--output-dir", str(output),
        "--metadata", str(metadata),
        "--quality", "accurate",
    ]


def rvm_command(
    *,
    python: Path,
    script: Path,
    frames: Path,
    output: Path,
    metadata: Path,
    vendor: Path,
    checkpoint: Path,
    device: str,
) -> list[str]:
    return [
        str(python), str(script),
        "--input-dir", str(frames),
        "--output-dir", str(output),
        "--metadata", str(metadata),
        "--vendor", str(vendor),
        "--checkpoint", str(checkpoint),
        "--variant", "mobilenetv3",
        "--device", device,
    ]


def edgetam_command(
    *,
    python: Path,
    script: Path,
    frames: Path,
    output: Path,
    work: Path,
    metadata: Path,
    checkpoint: Path,
    box: tuple[float, float, float, float],
) -> list[str]:
    return [
        str(python), str(script),
        "--input-dir", str(frames),
        "--output-dir", str(output),
        "--work-dir", str(work),
        "--metadata", str(metadata),
        "--checkpoint", str(checkpoint),
        "--box", *(str(value) for value in box),
        "--device", "mps",
    ]


def _mask_size(paths: list[Path]) -> list[int] | None:
    if not paths:
        return None
    with Image.open(paths[0]) as image:
        return [image.width, image.height]


def finalize_run_record(
    *,
    method: str,
    metrics_path: Path,
    stderr_path: Path,
    input_frames: int,
    output_directory: Path,
    implementation: dict[str, Any],
    device: str,
    settings: dict[str, Any],
    required_input: str,
    warnings: list[str] | None = None,
    extra_artifacts: dict[str, str] | None = None,
) -> dict[str, Any]:
    metrics = json.loads(metrics_path.read_text())
    masks = sorted(output_directory.glob("frame_*.png"))
    complete = len(masks) == input_frames
    success = metrics["returncode"] == 0 and complete
    exact_error = None
    if not success:
        exact_error = stderr_path.read_text(errors="replace").strip()
        if metrics["returncode"] == 0 and not complete:
            exact_error = (
                f"backend returned success but wrote {len(masks)} of "
                f"{input_frames} expected masks"
            )
    merged_warnings = list(warnings or [])
    if masks and _mask_size(masks) != [1920, 1080]:
        merged_warnings.append("native mask size differs from the 1920x1080 input")
    return {
        "schema_version": 1,
        "method": method,
        "status": "success" if success else "failed",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "implementation": implementation,
        "device": device,
        "settings": settings,
        "required_input": required_input,
        "returncode": metrics["returncode"],
        "wall_seconds": metrics["wall_seconds"],
        "peak_rss_bytes": metrics.get("peak_rss_bytes"),
        "input_frames": input_frames,
        "output_frames": len(masks),
        "native_mask_size": _mask_size(masks),
        "warnings": merged_warnings,
        "exact_error": exact_error,
        "artifacts": {
            "native_masks": str(output_directory),
            "stdout": str(metrics_path.with_name("stdout.log")),
            "stderr": str(stderr_path),
            "metrics": str(metrics_path),
            **(extra_artifacts or {}),
        },
    }


def run_apple_vision(project: Path, frames: Path, expected_frames: int) -> dict[str, Any]:
    method_root = project / "results/methods/apple-vision"
    native = method_root / "native"
    logs = method_root / "logs"
    native.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    for old in native.glob("frame_*.png"):
        old.unlink()
    metadata = method_root / "backend-metadata.json"
    command = apple_command(
        binary=project / "build/apple-vision-masker",
        frames=frames,
        output=native,
        metadata=metadata,
    )
    metrics = logs / "metrics.json"
    stderr = logs / "stderr.log"
    run_measured(
        command,
        cwd=project,
        stdout_path=logs / "stdout.log",
        stderr_path=stderr,
        metrics_path=metrics,
    )
    record = finalize_run_record(
        method="apple-vision",
        metrics_path=metrics,
        stderr_path=stderr,
        input_frames=expected_frames,
        output_directory=native,
        implementation={
            "framework": "Apple Vision",
            "request": "VNGeneratePersonSegmentationRequest",
            "revision": 1,
        },
        device="Apple Vision system-managed local execution",
        settings={"quality": "accurate", "pixel_format": "OneComponent8"},
        required_input="automatic person detection; no prompt",
        extra_artifacts={"backend_metadata": str(metadata)},
    )
    (method_root / "run.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


def _git_head(repository: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _run_rvm_device(
    *,
    project: Path,
    frames: Path,
    expected_frames: int,
    device: str,
    output: Path,
    logs: Path,
) -> dict[str, Any]:
    backend = project / "backends/rvm"
    vendor = backend / "vendor/RobustVideoMatting"
    checkpoint = backend / "checkpoints/rvm_mobilenetv3.pth"
    output.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    for old in output.glob("frame_*.png"):
        old.unlink()
    metadata = logs / "backend-metadata.json"
    command = rvm_command(
        python=backend / ".venv/bin/python",
        script=backend / "run.py",
        frames=frames,
        output=output,
        metadata=metadata,
        vendor=vendor,
        checkpoint=checkpoint,
        device=device,
    )
    metrics = logs / "metrics.json"
    stderr = logs / "stderr.log"
    run_measured(
        command,
        cwd=project,
        stdout_path=logs / "stdout.log",
        stderr_path=stderr,
        metrics_path=metrics,
    )
    return finalize_run_record(
        method="rvm",
        metrics_path=metrics,
        stderr_path=stderr,
        input_frames=expected_frames,
        output_directory=output,
        implementation={
            "repository": "https://github.com/PeterL1n/RobustVideoMatting",
            "commit": _git_head(vendor),
            "variant": "mobilenetv3",
            "checkpoint_sha256": fingerprint(checkpoint).sha256,
        },
        device=device,
        settings={"downsample_ratio": "auto (512 / longest side)", "temporal_state": True},
        required_input="automatic human matte; no prompt",
        extra_artifacts={"backend_metadata": str(metadata)},
    )


def run_rvm(project: Path, frames: Path, expected_frames: int) -> dict[str, Any]:
    method_root = project / "results/methods/rvm"
    mps_record = _run_rvm_device(
        project=project,
        frames=frames,
        expected_frames=expected_frames,
        device="mps",
        output=method_root / "native",
        logs=method_root / "logs-mps",
    )
    (method_root / "run-mps.json").write_text(json.dumps(mps_record, indent=2) + "\n")
    if mps_record["status"] == "success":
        final = mps_record
    else:
        cpu_record = _run_rvm_device(
            project=project,
            frames=frames,
            expected_frames=expected_frames,
            device="cpu",
            output=method_root / "native-cpu",
            logs=method_root / "logs-cpu",
        )
        cpu_record["warnings"].append("MPS attempt failed; exact failure preserved in run-mps.json")
        cpu_record["artifacts"]["failed_mps_record"] = str(method_root / "run-mps.json")
        final = cpu_record
    (method_root / "run.json").write_text(json.dumps(final, indent=2) + "\n")
    return final


def run_edgetam(
    project: Path,
    frames: Path,
    expected_frames: int,
    box: tuple[float, float, float, float],
) -> dict[str, Any]:
    method_root = project / "results/methods/edgetam"
    native = method_root / "native"
    work = method_root / "work"
    logs = method_root / "logs"
    native.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    for old in native.glob("frame_*.png"):
        old.unlink()

    backend = project / "backends/edgetam"
    vendor = backend / "vendor/EdgeTAM"
    checkpoint = vendor / "checkpoints/edgetam.pt"
    metadata = method_root / "backend-metadata.json"
    command = edgetam_command(
        python=backend / ".venv/bin/python",
        script=backend / "run.py",
        frames=frames,
        output=native,
        work=work,
        metadata=metadata,
        checkpoint=checkpoint,
        box=box,
    )
    metrics = logs / "metrics.json"
    stderr = logs / "stderr.log"
    run_measured(
        command,
        cwd=project,
        stdout_path=logs / "stdout.log",
        stderr_path=stderr,
        metrics_path=metrics,
    )
    record = finalize_run_record(
        method="edgetam",
        metrics_path=metrics,
        stderr_path=stderr,
        input_frames=expected_frames,
        output_directory=native,
        implementation={
            "repository": "https://github.com/facebookresearch/EdgeTAM",
            "commit": _git_head(vendor),
            "checkpoint_sha256": fingerprint(checkpoint).sha256,
        },
        device="mps with CPU-offloaded video/state",
        settings={
            "prompt_box_normalized": list(box),
            "temporal_propagation": True,
            "async_loader": False,
        },
        required_input="one first-frame presenter box",
        warnings=[
            "hard binary segmentation, not a soft fine-alpha matte",
            "CUDA-only connected-components hole filling is unavailable on the Mac and was skipped",
            "official async loader produced float64 frames incompatible with MPS; official synchronous float32 loading was used",
        ],
        extra_artifacts={"backend_metadata": str(metadata)},
    )
    (method_root / "run.json").write_text(json.dumps(record, indent=2) + "\n")
    return record
