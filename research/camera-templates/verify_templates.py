#!/usr/bin/env python3
"""Verify the N10 atomic camera registry, active renders, and media contract."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
EXPECTED_LEG_COUNTS = {
    "reveal-out": 1,
    "emphasis-push": 2,
    "right-reveal": 2,
    "lr-phrase": 3,
}
EXPECTED_COMPOSITIONS = {
    "reveal-out": "N10RevealOut",
    "emphasis-push": "N10EmphasisPush",
    "right-reveal": "N10RightReveal",
    "lr-phrase": "N10LeftRightPhrase",
}
EXPECTED_OUTPUTS = {
    "reveal-out": "T1-reveal-out-atomic.mp4",
    "emphasis-push": "T2-emphasis-push-atomic.mp4",
    "right-reveal": "T3-right-reveal-atomic.mp4",
    "lr-phrase": "T4-lr-phrase-atomic.mp4",
}
EXPECTED_COMPONENT_BINDINGS = {
    "T1.tsx": "reveal-out",
    "T2.tsx": "emphasis-push",
    "T3.tsx": "right-reveal",
    "T4.tsx": "lr-phrase",
}
ALLOWED_EASES = {"standard", "easeOut", "linear", "snap"}


def is_number_pair(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 2
        and all(isinstance(item, (int, float)) for item in value)
    )


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if registry.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    floor = registry.get("perceptibility_floor", {})
    scale_floor = floor.get("scale_delta")
    cx_floor = floor.get("cx_delta_px")
    if not isinstance(scale_floor, (int, float)) or not isinstance(
        cx_floor, (int, float)
    ):
        errors.append("perceptibility_floor must define numeric scale_delta and cx_delta_px")
        scale_floor, cx_floor = 0.10, 96

    records = registry.get("templates")
    if not isinstance(records, list):
        return errors + ["templates must be a list"]

    ids = [record.get("id") for record in records if isinstance(record, dict)]
    if len(ids) != len(set(ids)):
        errors.append("template IDs must be unique")

    by_id = {
        record.get("id"): record
        for record in records
        if isinstance(record, dict) and isinstance(record.get("id"), str)
    }
    active_ids = {
        template_id
        for template_id, record in by_id.items()
        if record.get("status") == "candidate"
    }
    expected_ids = set(EXPECTED_LEG_COUNTS)
    if active_ids != expected_ids:
        errors.append(
            f"active candidate set must be {sorted(expected_ids)}, got {sorted(active_ids)}"
        )

    step_punch = by_id.get("step-punch")
    if not step_punch:
        errors.append("step-punch must remain recorded as rejected evidence")
    else:
        if step_punch.get("status") != "rejected":
            errors.append("step-punch must be rejected and non-selectable")
        if step_punch.get("composition_id") is not None:
            errors.append("step-punch must not have an active composition_id")
        if step_punch.get("legs") != []:
            errors.append("step-punch must not expose active camera legs")
        if not str(step_punch.get("rejection_reason", "")).strip():
            errors.append("step-punch must record its rejection reason")

    for template_id, expected_count in EXPECTED_LEG_COUNTS.items():
        record = by_id.get(template_id)
        if not record:
            errors.append(f"missing required template: {template_id}")
            continue
        if record.get("status") != "candidate":
            errors.append(f"{template_id}: status must be candidate")
        if record.get("composition_id") != EXPECTED_COMPOSITIONS[template_id]:
            errors.append(
                f"{template_id}: composition_id must be {EXPECTED_COMPOSITIONS[template_id]}"
            )
        legs = record.get("legs")
        if not isinstance(legs, list):
            errors.append(f"{template_id}: legs must be a list")
            continue
        if len(legs) != expected_count:
            errors.append(
                f"{template_id}: expected {expected_count} legs, got {len(legs)}"
            )

        previous: dict[str, Any] | None = None
        for index, current in enumerate(legs, start=1):
            prefix = f"{template_id} leg {index}"
            if not isinstance(current, dict):
                errors.append(f"{prefix}: leg must be an object")
                continue
            t0, t1 = current.get("t0"), current.get("t1")
            if not isinstance(t0, (int, float)) or not isinstance(t1, (int, float)):
                errors.append(f"{prefix}: t0 and t1 must be numeric")
            elif t1 <= t0:
                errors.append(f"{prefix}: t1 must be greater than t0")
            if not str(current.get("reason", "")).strip():
                errors.append(f"{prefix}: editorial reason is required")
            if current.get("ease") not in ALLOWED_EASES:
                errors.append(f"{prefix}: unknown ease {current.get('ease')!r}")

            for field in ("scale", "cx", "cy"):
                if not is_number_pair(current.get(field)):
                    errors.append(f"{prefix}: {field} must be a numeric pair")

            scale = current.get("scale")
            cx = current.get("cx")
            if is_number_pair(scale):
                if min(scale) < 1.0:
                    errors.append(f"{prefix}: scale below 1.0 exposes canvas")
                scale_delta = abs(scale[1] - scale[0])
            else:
                scale_delta = 0.0
            cx_delta = abs(cx[1] - cx[0]) if is_number_pair(cx) else 0.0
            if scale_delta + 1e-9 < scale_floor and cx_delta + 1e-9 < cx_floor:
                errors.append(
                    f"{prefix}: movement is below the perceptibility floor"
                )

            if previous is not None:
                if isinstance(t0, (int, float)) and t0 < previous.get("t1", t0):
                    errors.append(f"{prefix}: legs overlap or are out of order")
                for field in ("scale", "cx", "cy"):
                    prior_pair = previous.get(field)
                    current_pair = current.get(field)
                    if is_number_pair(prior_pair) and is_number_pair(current_pair):
                        if prior_pair[1] != current_pair[0]:
                            errors.append(
                                f"{prefix}: {field} does not continue from the prior leg"
                            )
            previous = current

    return errors


def validate_root(workspace: Path, registry: dict[str, Any]) -> list[str]:
    root_path = workspace / "composition" / "remotion" / "src" / "Root.tsx"
    if not root_path.exists():
        return [f"missing Remotion root: {root_path}"]
    source = root_path.read_text(encoding="utf-8")
    registered = set(re.findall(r'\bid="([^"]+)"', source))
    expected = {
        record["composition_id"]
        for record in registry.get("templates", [])
        if isinstance(record, dict)
        and record.get("status") == "candidate"
        and isinstance(record.get("composition_id"), str)
    }
    errors: list[str] = []
    if registered != expected:
        errors.append(
            f"Root.tsx must register exactly {sorted(expected)}, got {sorted(registered)}"
        )
    if re.search(r'import\s+\{?\s*T5\b', source):
        errors.append("Root.tsx must not import rejected T5")
    if "N10StepPunch" in source:
        errors.append("Root.tsx must not register rejected step-punch")
    return errors


def validate_component_bindings(workspace: Path) -> list[str]:
    source_dir = workspace / "composition" / "remotion" / "src"
    errors: list[str] = []
    for filename, template_id in EXPECTED_COMPONENT_BINDINGS.items():
        path = source_dir / filename
        if not path.exists():
            errors.append(f"missing active component: {path}")
            continue
        source = path.read_text(encoding="utf-8")
        binding = re.compile(
            rf'const\s+LEGS\s*=\s*getCameraLegs\(\s*"{re.escape(template_id)}"\s*\)\s*;'
        )
        if not binding.search(source):
            errors.append(
                f"{filename}: LEGS must come directly from registry template {template_id}"
            )
        if source.count("getCameraLegs(") != 1:
            errors.append(f"{filename}: exactly one registry schedule lookup is allowed")
        if source.count("<CameraViewport") != 1 or "legs={LEGS}" not in source:
            errors.append(f"{filename}: the single CameraViewport must use registry LEGS")
    return errors


def validate_media(workspace: Path) -> list[str]:
    errors: list[str] = []
    output_dir = workspace / "variants" / "v2"
    for template_id, filename in EXPECTED_OUTPUTS.items():
        path = output_dir / filename
        if not path.exists():
            errors.append(f"{template_id}: missing Version 2 render: {path}")
            continue
        probe = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-count_frames",
                "-show_entries",
                "stream=codec_type,width,height,avg_frame_rate,nb_read_frames,duration,sample_rate,channels",
                "-of",
                "json",
                str(path),
            ],
            capture_output=True,
            text=True,
        )
        if probe.returncode != 0:
            errors.append(f"{template_id}: ffprobe failed: {probe.stderr.strip()}")
            continue
        streams = json.loads(probe.stdout).get("streams", [])
        video = next((item for item in streams if item.get("codec_type") == "video"), None)
        audio = next((item for item in streams if item.get("codec_type") == "audio"), None)
        if video is None:
            errors.append(f"{template_id}: missing video stream")
            continue
        if (video.get("width"), video.get("height")) != (1920, 1080):
            errors.append(f"{template_id}: video must be 1920x1080")
        if video.get("avg_frame_rate") != "30/1":
            errors.append(f"{template_id}: video must be 30fps")
        if video.get("nb_read_frames") != "336":
            errors.append(f"{template_id}: video must contain 336 frames")
        if video.get("duration") != "11.200000":
            errors.append(f"{template_id}: video duration must be 11.200000s")
        if audio is None:
            errors.append(f"{template_id}: missing audio stream")
        elif audio.get("sample_rate") != "48000" or audio.get("channels") != 2:
            errors.append(f"{template_id}: audio must be 48kHz stereo")
    return errors


def validate_workspace(workspace: Path, require_media: bool = True) -> list[str]:
    registry_path = workspace / "templates.json"
    if not registry_path.exists():
        return [f"missing registry: {registry_path}"]
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"cannot read registry: {error}"]
    if not isinstance(registry, dict):
        return ["registry root must be an object"]
    errors = validate_registry(registry)
    errors.extend(validate_root(workspace, registry))
    errors.extend(validate_component_bindings(workspace))
    if require_media:
        errors.extend(validate_media(workspace))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=ROOT)
    parser.add_argument("--skip-media", action="store_true")
    args = parser.parse_args(argv)
    errors = validate_workspace(args.workspace.resolve(), not args.skip_media)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    scope = "registry and active compositions" if args.skip_media else "registry, compositions, and Version 2 media"
    print(f"PASS: N10 atomic camera {scope} verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
