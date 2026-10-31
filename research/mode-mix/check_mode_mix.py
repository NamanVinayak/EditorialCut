#!/usr/bin/env python3
"""check_mode_mix.py — computable mode-mix gate (Option A, the project lead 2026-07-16).

Reads a beat-map.json (schema: docs/rulebook/beat-map-schema.md) and enforces that the
plan did not silently collapse into a single visual family. A single-mode video is
allowed ONLY when the director declared it on purpose with a reason.

Pure stdlib — no venv. Exit 0 = pass, 1 = fail, 2 = usage/parse error.

    python3 check_mode_mix.py path/to/beat-map.json

Run at runbook Stage 5 (plan check, before any render) and Stage 7 (gate, against the
final plan). This is check #10 of the editorial verification gate.
"""
import argparse
import json
import sys

VALID_MODES = {"clean", "overlay", "presentation"}
NON_CLEAN = {"overlay", "presentation"}
ACCEPTED_CAMERA_ATOMS = {"T1", "T2", "T3", "T4"}  # T5 (step-punch) is rejected — N10
VALID_PACE = {"fast", "medium", "slow"}


def fail(msgs):
    return (1, msgs)


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: beat-map not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"ERROR: beat-map is not valid JSON: {e}", file=sys.stderr)
        sys.exit(2)


def check(bm):
    """Return (exit_code, failures, warnings, summary_lines)."""
    failures, warnings, summary = [], [], []

    dm = bm.get("declared_mix")
    if not isinstance(dm, dict):
        failures.append("declared_mix is missing — the director must declare the intended "
                        "overlay/presentation balance up front (Option A).")
        return 1, failures, warnings, summary

    for field in ("intent", "modes_used", "dominant", "single_mode", "pace"):
        if field not in dm:
            failures.append(f"declared_mix.{field} is missing (required).")
    if not str(dm.get("intent", "")).strip():
        failures.append("declared_mix.intent must be a non-empty human sentence.")
    if dm.get("pace") not in VALID_PACE:
        failures.append(f"declared_mix.pace must be one of {sorted(VALID_PACE)}.")

    single_mode = dm.get("single_mode")
    reason = dm.get("single_mode_reason")
    if single_mode is True and not str(reason or "").strip():
        failures.append("declared_mix.single_mode is true but single_mode_reason is empty — "
                        "a deliberately single-mode video must state the story reason.")
    if single_mode is False and str(reason or "").strip():
        warnings.append("single_mode is false but single_mode_reason is set; it will be ignored.")

    beats = bm.get("beats")
    if not isinstance(beats, list) or not beats:
        failures.append("beats[] is missing or empty.")
        return 1, failures, warnings, summary

    # Per-beat validity + tally.
    mode_counts = {"clean": 0, "overlay": 0, "presentation": 0}
    effect_moments = 0
    for b in beats:
        bid = b.get("id", "<no-id>")
        mode = b.get("spatial_mode")
        if mode not in VALID_MODES:
            failures.append(f"beat {bid}: spatial_mode '{mode}' invalid; must be one of {sorted(VALID_MODES)}.")
            continue
        mode_counts[mode] += 1
        cam = b.get("camera_template_id")
        if cam == "T5" or (cam is not None and cam not in ACCEPTED_CAMERA_ATOMS):
            failures.append(f"beat {bid}: camera_template_id '{cam}' is not an accepted N10 atom "
                            f"({sorted(ACCEPTED_CAMERA_ATOMS)}); T5 is rejected.")
        if b.get("is_effect_moment"):
            effect_moments += 1
            if not str(b.get("reason", "")).strip():
                failures.append(f"beat {bid}: is_effect_moment but has no reason (N7 requires "
                                "semantic or rhythmic motivation).")

    actual_non_clean = {m for m in NON_CLEAN if mode_counts[m] > 0}
    summary.append(f"beats: {len(beats)}  |  clean={mode_counts['clean']} "
                   f"overlay={mode_counts['overlay']} presentation={mode_counts['presentation']}  "
                   f"|  effect moments: {effect_moments}")
    summary.append(f"declared: single_mode={single_mode} dominant={dm.get('dominant')} "
                   f"modes_used={dm.get('modes_used')} pace={dm.get('pace')}")

    # --- The core Option-A policy -----------------------------------------
    if len(actual_non_clean) == 0:
        if single_mode is True:
            warnings.append("plan is entirely clean footage/captions — allowed because "
                            "single_mode is declared, but confirm this is intended.")
        else:
            failures.append("plan has zero treated beats (all clean) — nothing is mixed and "
                            "no single_mode was declared. Either treat some beats or declare "
                            "single_mode with a reason.")
    elif len(actual_non_clean) == 1:
        only = next(iter(actual_non_clean))
        missing = next(iter(NON_CLEAN - actual_non_clean))
        if single_mode is True:
            summary.append(f"single family '{only}' — allowed (declared): {reason}")
        else:
            failures.append(
                f"COLLAPSED TO ONE FAMILY: the whole video uses only '{only}' and never "
                f"'{missing}', but single_mode was not declared. This is exactly the "
                "default-into-one-mode failure this gate exists to stop. Either interleave "
                f"'{missing}' beats, or set single_mode=true with a story reason.")
    else:  # both overlay and presentation present -> it mixed
        if single_mode is True:
            failures.append("declared_mix.single_mode is true but the plan actually uses "
                            f"{sorted(actual_non_clean)} — declaration contradicts the plan.")
        else:
            summary.append(f"mixed families: {sorted(actual_non_clean)} — good.")

    # Declared modes_used should match what's actually used (clean included).
    declared_used = dm.get("modes_used")
    if isinstance(declared_used, list):
        actual_all = {m for m, c in mode_counts.items() if c > 0}
        if set(declared_used) != actual_all:
            failures.append(f"declared_mix.modes_used {sorted(set(declared_used))} != modes "
                            f"actually in the plan {sorted(actual_all)}.")

    # dominant should be the real most-used non-clean mode (soft check).
    if actual_non_clean:
        real_dominant = max(actual_non_clean, key=lambda m: mode_counts[m])
        if dm.get("dominant") not in (real_dominant, "clean"):
            warnings.append(f"declared dominant '{dm.get('dominant')}' but most-used treated "
                            f"family is '{real_dominant}'.")

    return (1 if failures else 0), failures, warnings, summary


def main():
    ap = argparse.ArgumentParser(description="Computable mode-mix gate (check #10).")
    ap.add_argument("beat_map", help="path to beat-map.json")
    args = ap.parse_args()

    bm = load(args.beat_map)
    code, failures, warnings, summary = check(bm)

    print("=== mode-mix check (#10) ===")
    for line in summary:
        print("  " + line)
    for w in warnings:
        print("  WARN: " + w)
    if failures:
        print("\nFAIL:")
        for m in failures:
            print("  - " + m)
        print("\nRESULT: FAIL — fix the plan (Stage 4/4a) and re-check before rendering.")
    else:
        print("\nRESULT: PASS")
    sys.exit(code)


if __name__ == "__main__":
    main()
