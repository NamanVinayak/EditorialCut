#!/usr/bin/env python3
"""Tests for the N10 atomic camera-template contract."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VERIFIER = ROOT / "verify_templates.py"
COMPONENT_BINDINGS = {
    "T1.tsx": "reveal-out",
    "T2.tsx": "emphasis-push",
    "T3.tsx": "right-reveal",
    "T4.tsx": "lr-phrase",
}


def leg(
    t0: float,
    t1: float,
    scale: list[float],
    cx: list[float],
    cy: list[float],
    ease: str,
    reason: str,
) -> dict:
    return {
        "t0": t0,
        "t1": t1,
        "scale": scale,
        "cx": cx,
        "cy": cy,
        "ease": ease,
        "reason": reason,
    }


def valid_registry() -> dict:
    return {
        "schema_version": 1,
        "perceptibility_floor": {"scale_delta": 0.10, "cx_delta_px": 96},
        "templates": [
            {
                "id": "reveal-out",
                "status": "candidate",
                "composition_id": "N10RevealOut",
                "legs": [
                    leg(
                        0.0,
                        2.6,
                        [1.25, 1.0],
                        [985, 960],
                        [400, 540],
                        "easeOut",
                        "Open tight, reveal to the full frame once.",
                    )
                ],
            },
            {
                "id": "emphasis-push",
                "status": "candidate",
                "composition_id": "N10EmphasisPush",
                "legs": [
                    leg(
                        2.64,
                        3.88,
                        [1.0, 1.18],
                        [960, 985],
                        [540, 420],
                        "standard",
                        "Push in on the selected emphasis phrase.",
                    ),
                    leg(
                        7.74,
                        8.14,
                        [1.18, 1.0],
                        [985, 960],
                        [420, 540],
                        "easeOut",
                        "Return when the emphasized thought closes.",
                    ),
                ],
            },
            {
                "id": "right-reveal",
                "status": "candidate",
                "composition_id": "N10RightReveal",
                "legs": [
                    leg(
                        2.4,
                        3.6,
                        [1.0, 1.14],
                        [960, 1075],
                        [540, 480],
                        "standard",
                        "Seat the presenter left and open the right third.",
                    ),
                    leg(
                        7.74,
                        8.6,
                        [1.14, 1.0],
                        [1075, 960],
                        [480, 540],
                        "easeOut",
                        "Return after the right-side visual moment closes.",
                    ),
                ],
            },
            {
                "id": "lr-phrase",
                "status": "candidate",
                "composition_id": "N10LeftRightPhrase",
                "legs": [
                    leg(
                        4.36,
                        4.9,
                        [1.0, 1.15],
                        [960, 860],
                        [540, 470],
                        "standard",
                        "Favor one side for the first parallel clause.",
                    ),
                    leg(
                        5.94,
                        6.5,
                        [1.15, 1.15],
                        [860, 1060],
                        [470, 470],
                        "standard",
                        "Cross to the opposite side for the second parallel clause.",
                    ),
                    leg(
                        7.74,
                        8.5,
                        [1.15, 1.0],
                        [1060, 960],
                        [470, 540],
                        "easeOut",
                        "Return to neutral when the paired phrase closes.",
                    ),
                ],
            },
            {
                "id": "step-punch",
                "status": "rejected",
                "composition_id": None,
                "rejection_reason": "Rejected by the project lead after the first moving-video review.",
                "legs": [],
            },
        ],
    }


def root_source(composition_ids: list[str], include_t5_import: bool = False) -> str:
    import_line = 'import { T5 } from "./T5";\n' if include_t5_import else ""
    registrations = "\n".join(
        f'<Composition id="{composition_id}" component={{T1}} durationInFrames={{336}} fps={{30}} width={{1920}} height={{1080}} />'
        for composition_id in composition_ids
    )
    return f'{import_line}export const Root = () => (<>{{{registrations}}}</>);\n'


class TemplateVerifierTests(unittest.TestCase):
    maxDiff = None

    def run_fixture(
        self,
        registry: dict,
        *,
        composition_ids: list[str] | None = None,
        include_t5_import: bool = False,
        component_overrides: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            source_dir = workspace / "composition" / "remotion" / "src"
            source_dir.mkdir(parents=True)
            (workspace / "templates.json").write_text(
                json.dumps(registry), encoding="utf-8"
            )
            ids = composition_ids or [
                "N10RevealOut",
                "N10EmphasisPush",
                "N10RightReveal",
                "N10LeftRightPhrase",
            ]
            (source_dir / "Root.tsx").write_text(
                root_source(ids, include_t5_import), encoding="utf-8"
            )
            overrides = component_overrides or {}
            for filename, template_id in COMPONENT_BINDINGS.items():
                source = overrides.get(
                    filename,
                    'import { getCameraLegs } from "./templateRegistry";\n'
                    f'const LEGS = getCameraLegs("{template_id}");\n'
                    'export const Demo = () => <CameraViewport legs={LEGS} />;\n',
                )
                (source_dir / filename).write_text(source, encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(VERIFIER),
                    "--workspace",
                    str(workspace),
                    "--skip-media",
                ],
                capture_output=True,
                text=True,
            )

    def test_real_workspace_satisfies_atomic_contract(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VERIFIER),
                "--workspace",
                str(ROOT),
                "--skip-media",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_valid_fixture_passes(self) -> None:
        result = self.run_fixture(valid_registry())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_active_step_punch_fails(self) -> None:
        registry = valid_registry()
        rejected = registry["templates"][-1]
        rejected.update(
            {
                "status": "candidate",
                "composition_id": "N10StepPunch",
                "legs": [
                    leg(
                        2.64,
                        2.8,
                        [1.0, 1.12],
                        [960, 970],
                        [540, 500],
                        "snap",
                        "Punch in.",
                    )
                ],
            }
        )
        result = self.run_fixture(
            registry,
            composition_ids=[
                "N10RevealOut",
                "N10EmphasisPush",
                "N10RightReveal",
                "N10LeftRightPhrase",
                "N10StepPunch",
            ],
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("step-punch", result.stdout + result.stderr)

    def test_extra_camera_leg_fails(self) -> None:
        registry = valid_registry()
        registry["templates"][0]["legs"].append(
            leg(
                8.98,
                9.6,
                [1.0, 1.12],
                [960, 985],
                [540, 430],
                "standard",
                "Unrelated later push.",
            )
        )
        result = self.run_fixture(registry)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected 1 legs", result.stdout + result.stderr)

    def test_missing_reason_fails(self) -> None:
        registry = valid_registry()
        registry["templates"][0]["legs"][0]["reason"] = ""
        result = self.run_fixture(registry)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("reason", result.stdout + result.stderr)

    def test_micro_movement_fails(self) -> None:
        registry = valid_registry()
        first_leg = registry["templates"][0]["legs"][0]
        first_leg["scale"] = [1.0, 1.05]
        first_leg["cx"] = [960, 960]
        result = self.run_fixture(registry)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("perceptibility floor", result.stdout + result.stderr)

    def test_scale_below_one_fails(self) -> None:
        registry = valid_registry()
        registry["templates"][0]["legs"][0]["scale"] = [1.25, 0.99]
        result = self.run_fixture(registry)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("below 1.0", result.stdout + result.stderr)

    def test_t5_import_or_registration_fails(self) -> None:
        registry = copy.deepcopy(valid_registry())
        result = self.run_fixture(registry, include_t5_import=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("T5", result.stdout + result.stderr)

    def test_handwritten_schedule_instead_of_registry_binding_fails(self) -> None:
        result = self.run_fixture(
            valid_registry(),
            component_overrides={
                "T1.tsx": (
                    "const LEGS = [{t0: 0, t1: 1}];\n"
                    "export const Demo = () => <CameraViewport legs={LEGS} />;\n"
                )
            },
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("T1.tsx", result.stdout + result.stderr)
        self.assertIn("registry", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
