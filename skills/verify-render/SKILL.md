---
name: verify-render
description: Invoke before declaring ANY render, cut, or edit done — verify the actual rendered pixels and audio, never a worker's prose report. Wraps the editorial verification gate and the mode-mix check; a failed automatic-fail check means fix and re-render, not a footnote. Do NOT claim success from a description of the output.
tier: MECHANICAL
---

# verify-render

**Job:** be the last gate before you tell the user a render is done. It exists so
"looks done" never substitutes for "verified against pixels and audio." This is a thin
governance wrapper so the gate pages in by description-match even when the working
contract is trimmed; the runbook and director instructions hold the full checklist.

## Read these

- [`docs/rulebook/orchestration-runbook.md`](../../docs/rulebook/orchestration-runbook.md)
  — Stage 7, the editorial verification gate.
- [`docs/rulebook/creative-director-instructions.md`](../../docs/rulebook/creative-director-instructions.md)
  — the full check list the gate runs.
- [`check-mode-mix`](../check-mode-mix/SKILL.md) — check #10, re-run on the final plan.

## What the gate verifies (pixels and audio, not prose)

- word-sync, holds within the N1/N2 budget, active-frame alignment;
- presenter integrity — no seams, no doubling during camera motion;
- **no text crosses the presenter's face** (rule N5);
- **check #9:** zero Devanagari codepoints in rendered text;
- **check #10:** mode-mix — re-run against the final `beat-map.json`:

  ```bash
  python3 research/mode-mix/check_mode_mix.py <edit-folder>/beat-map.json
  ```

- **check #11:** color authority — with `color_authority: unchanged`, inspect the engine
  graph/filters for any footage color transform and compare representative
  full-resolution source/output frames.

## Computable vs human checks

The computable checks (#9, #10, word-sync, holds, and the render-plan portion of #11)
run automatically and **cannot be skipped**. Only the un-computable ones — seams,
doubling, active-frame *feel* — are human/pixel work. Write `verify/gate-report.md` with
every check, pass/fail, and its evidence (full-resolution crops, scan output, timing
measurements).

## The rule

Verify rendered pixels and audio, not a worker's prose report. A failed automatic-fail
check means fix and re-render, not a footnote. Do not claim success without a gate report
that exists and passes.
