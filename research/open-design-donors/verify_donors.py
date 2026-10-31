#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Sequence


ALLOWED_STATUSES = {
    "reference-only",
    "candidate",
    "benchmarked",
    "accepted",
    "rejected",
}
ALLOWED_DONOR_TYPES = {
    "reasoning-method",
    "visual-grammar",
    "code-pattern",
    "font",
    "raw-asset",
}
ALLOWED_LICENSE_STATES = {"verified", "incomplete", "not-applicable"}
ALLOWED_OVERLAP_STATES = {"none", "partial", "duplicate"}
USABLE_STATUSES = {"candidate", "benchmarked", "accepted"}
REQUIRED_DONOR_KEYS = {
    "id",
    "name",
    "upstream_path",
    "preview_path",
    "donor_type",
    "license",
    "local_overlap",
    "portable_qualities",
    "do_not_copy",
    "required_adaptation",
    "status",
    "review_evidence",
    "known_limitations",
}
REQUIRED_LIST_KEYS = {
    "portable_qualities",
    "do_not_copy",
    "required_adaptation",
    "review_evidence",
    "known_limitations",
}


def load_registry(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("registry root must be a JSON object")
    return value


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_string_list(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(_nonempty_string(item) for item in value)
    )


def validate_registry(registry: dict, workspace_root: Path) -> list[str]:
    errors: list[str] = []
    if registry.get("schema_version") != 1:
        errors.append("schema_version must equal 1")

    audit = registry.get("audit")
    if not isinstance(audit, dict):
        errors.append("audit must be an object")
    else:
        for key in ("repository", "commit", "audited_on", "root_license"):
            if not _nonempty_string(audit.get(key)):
                errors.append(f"audit.{key} must be a non-empty string")
        commit = audit.get("commit")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            errors.append("audit.commit must be a lowercase 40-character Git hash")

    donors = registry.get("donors")
    if not isinstance(donors, list) or not donors:
        errors.append("donors must be a non-empty list")
        return errors

    seen_ids: set[str] = set()
    root = workspace_root.resolve()
    for index, donor in enumerate(donors):
        prefix = f"donors[{index}]"
        if not isinstance(donor, dict):
            errors.append(f"{prefix} must be an object")
            continue

        missing = sorted(REQUIRED_DONOR_KEYS - donor.keys())
        if missing:
            errors.append(f"{prefix} missing required keys: {', '.join(missing)}")
            continue

        donor_id = donor["id"]
        if not _nonempty_string(donor_id):
            errors.append(f"{prefix}.id must be a non-empty string")
        elif donor_id in seen_ids:
            errors.append(f"{prefix} has duplicate donor id '{donor_id}'")
        else:
            seen_ids.add(donor_id)

        for key in ("name", "upstream_path", "preview_path"):
            if not _nonempty_string(donor[key]):
                errors.append(f"{prefix}.{key} must be a non-empty string")

        if donor["donor_type"] not in ALLOWED_DONOR_TYPES:
            errors.append(
                f"{prefix}.donor_type has invalid value '{donor['donor_type']}'"
            )
        if donor["status"] not in ALLOWED_STATUSES:
            errors.append(f"{prefix}.status has invalid value '{donor['status']}'")

        for key in REQUIRED_LIST_KEYS:
            if not _nonempty_string_list(donor[key]):
                errors.append(
                    f"{prefix}.{key} must be a non-empty list of non-empty strings"
                )

        license_info = donor["license"]
        if not isinstance(license_info, dict):
            errors.append(f"{prefix}.license must be an object")
        else:
            for key in ("state", "upstream", "nested", "notes"):
                if not _nonempty_string(license_info.get(key)):
                    errors.append(
                        f"{prefix}.license.{key} must be a non-empty string"
                    )
            state = license_info.get("state")
            if state not in ALLOWED_LICENSE_STATES:
                errors.append(
                    f"{prefix}.license.state has invalid value '{state}'"
                )

        overlap = donor["local_overlap"]
        if not isinstance(overlap, dict):
            errors.append(f"{prefix}.local_overlap must be an object")
            continue
        state = overlap.get("state")
        paths = overlap.get("local_paths")
        notes = overlap.get("notes")
        if state not in ALLOWED_OVERLAP_STATES:
            errors.append(
                f"{prefix}.local_overlap.state has invalid value '{state}'"
            )
        if not isinstance(paths, list) or not all(
            _nonempty_string(path) for path in paths
        ):
            errors.append(
                f"{prefix}.local_overlap.local_paths must be a list of non-empty strings"
            )
            continue
        if not _nonempty_string(notes):
            errors.append(f"{prefix}.local_overlap.notes must be a non-empty string")
        if state == "none" and paths:
            errors.append(
                f"{prefix}.local_overlap state 'none' cannot declare local_paths"
            )
        if state in {"partial", "duplicate"} and not paths:
            errors.append(
                f"{prefix}.local_overlap state '{state}' requires local_paths"
            )
        for relative in paths:
            candidate = (root / relative).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                errors.append(f"{prefix} local path escapes workspace: {relative}")
                continue
            if not candidate.exists():
                errors.append(
                    f"{prefix} local overlap path does not exist: {relative}"
                )

    return errors


def validate_selected_donor(
    registry: dict, donor_id: str | None, require_usable: bool
) -> list[str]:
    if donor_id is None:
        if require_usable:
            return ["--require-usable requires --donor-id"]
        return []

    donors = registry.get("donors")
    if not isinstance(donors, list):
        return [f"selected donor '{donor_id}' cannot be resolved: donors is invalid"]

    selected = next(
        (
            donor
            for donor in donors
            if isinstance(donor, dict) and donor.get("id") == donor_id
        ),
        None,
    )
    if selected is None:
        return [f"selected donor '{donor_id}' does not exist"]

    status = selected.get("status")
    if require_usable and status not in USABLE_STATUSES:
        return [
            f"selected donor '{donor_id}' is not usable: status is '{status}', "
            f"expected one of {sorted(USABLE_STATUSES)}"
        ]
    return []


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify external design donor records"
    )
    parser.add_argument("registry", type=Path)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--donor-id")
    parser.add_argument("--require-usable", action="store_true")
    args = parser.parse_args(argv)

    try:
        registry = load_registry(args.registry)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    errors = validate_registry(registry, args.workspace)
    errors.extend(
        validate_selected_donor(registry, args.donor_id, args.require_usable)
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    selected = f"; selected donor={args.donor_id}" if args.donor_id else ""
    print(f"PASS: {len(registry['donors'])} donor records verified{selected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
