import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from verify_donors import load_registry, main, validate_registry


def valid_registry(local_path: str) -> dict:
    return {
        "schema_version": 1,
        "audit": {
            "repository": "https://github.com/nexu-io/open-design",
            "commit": "3a6221a54b84bdc29d7f1bfe9b9da71c0935a229",
            "audited_on": "2026-07-16",
            "root_license": "Apache-2.0",
        },
        "donors": [
            {
                "id": "sample-donor",
                "name": "Sample donor",
                "upstream_path": "skills/sample/SKILL.md",
                "preview_path": "skills/sample/example.md",
                "donor_type": "reasoning-method",
                "license": {
                    "state": "verified",
                    "upstream": "Apache-2.0",
                    "nested": "not-applicable",
                    "notes": "Repository-authored method.",
                },
                "local_overlap": {
                    "state": "partial",
                    "local_paths": [local_path],
                    "notes": "The local path covers part of the method.",
                },
                "portable_qualities": ["Keep/change/do-not-copy separation."],
                "do_not_copy": ["Source-specific examples."],
                "required_adaptation": ["Use EditorialCut evidence lanes."],
                "status": "candidate",
                "review_evidence": ["Source inspected at the audited commit."],
                "known_limitations": ["No rendered EditorialCut benchmark yet."],
            }
        ],
    }


class DonorRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "existing.md").write_text("evidence\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_registry(self, registry: dict) -> Path:
        path = self.root / "selected-donors.json"
        path.write_text(json.dumps(registry), encoding="utf-8")
        return path

    def run_main(self, argv: list[str]) -> int:
        with redirect_stdout(io.StringIO()):
            return main(argv)

    def test_valid_registry_has_no_errors(self) -> None:
        registry = valid_registry("existing.md")
        self.assertEqual(validate_registry(registry, self.root), [])

    def test_missing_required_key_is_reported(self) -> None:
        registry = valid_registry("existing.md")
        del registry["donors"][0]["do_not_copy"]
        errors = validate_registry(registry, self.root)
        self.assertTrue(any("do_not_copy" in error for error in errors))

    def test_invalid_commit_status_and_license_are_reported(self) -> None:
        registry = valid_registry("existing.md")
        registry["audit"]["commit"] = "main"
        registry["donors"][0]["status"] = "looks-good"
        registry["donors"][0]["license"]["state"] = "probably"
        errors = validate_registry(registry, self.root)
        self.assertTrue(any("40-character" in error for error in errors))
        self.assertTrue(any("looks-good" in error for error in errors))
        self.assertTrue(any("probably" in error for error in errors))

    def test_duplicate_id_and_missing_overlap_path_are_reported(self) -> None:
        registry = valid_registry("missing.md")
        registry["donors"].append(dict(registry["donors"][0]))
        errors = validate_registry(registry, self.root)
        self.assertTrue(any("duplicate donor id" in error for error in errors))
        self.assertTrue(any("does not exist" in error for error in errors))

    def test_none_overlap_rejects_local_paths(self) -> None:
        registry = valid_registry("existing.md")
        registry["donors"][0]["local_overlap"]["state"] = "none"
        errors = validate_registry(registry, self.root)
        self.assertTrue(any("state 'none'" in error for error in errors))

    def test_load_and_cli(self) -> None:
        path = self.root / "donors.json"
        path.write_text(json.dumps(valid_registry("existing.md")), encoding="utf-8")
        self.assertEqual(load_registry(path)["schema_version"], 1)
        self.assertEqual(
            self.run_main([str(path), "--workspace", str(self.root)]), 0
        )

    def test_cli_accepts_selected_candidate_donor(self) -> None:
        path = self.write_registry(valid_registry("existing.md"))
        result = self.run_main(
            [
                str(path),
                "--workspace",
                str(self.root),
                "--donor-id",
                "sample-donor",
                "--require-usable",
            ]
        )
        self.assertEqual(result, 0)

    def test_cli_rejects_selected_rejected_donor(self) -> None:
        registry = valid_registry("existing.md")
        registry["donors"][0]["status"] = "rejected"
        path = self.write_registry(registry)
        result = self.run_main(
            [
                str(path),
                "--workspace",
                str(self.root),
                "--donor-id",
                "sample-donor",
                "--require-usable",
            ]
        )
        self.assertEqual(result, 1)

    def test_cli_rejects_selected_reference_only_donor(self) -> None:
        registry = valid_registry("existing.md")
        registry["donors"][0]["status"] = "reference-only"
        path = self.write_registry(registry)
        result = self.run_main(
            [
                str(path),
                "--workspace",
                str(self.root),
                "--donor-id",
                "sample-donor",
                "--require-usable",
            ]
        )
        self.assertEqual(result, 1)

    def test_cli_rejects_unknown_selected_donor(self) -> None:
        path = self.write_registry(valid_registry("existing.md"))
        result = self.run_main(
            [
                str(path),
                "--workspace",
                str(self.root),
                "--donor-id",
                "missing-donor",
                "--require-usable",
            ]
        )
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
