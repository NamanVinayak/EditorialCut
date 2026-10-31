---
name: check-mode-mix
description: Invoke to run the computable mode-mix gate (check #10) on beat-map.json — fails a plan that silently collapses into one visual family (all-overlay or all-presentation) unless single-mode was declared with a reason. Do NOT eyeball the mix; run this before spending a render and again at the final verification gate.
tier: MECHANICAL
---

# check-mode-mix

**Job:** hold every edit to the mode-mix it declared. The recurring failure (the project lead,
2026-07-16) is the editor *defaulting* into one visual family for a whole video — all
graphics-on-footage (`overlay`), or all full-frame `presentation` — when the intent was a
mix. This is a **computable** check, so it must be a script, not a reviewer's discretion
(the N9 lesson). Option A policy: a single-family video is allowed **only** when
`declared_mix.single_mode` is `true` with a non-empty `single_mode_reason`.

## Input

One `beat-map.json` per the schema in
[`docs/rulebook/beat-map-schema.md`](../../docs/rulebook/beat-map-schema.md). The director
emits it at runbook Stage 4.

## Run

```bash
python3 research/mode-mix/check_mode_mix.py <edit-folder>/beat-map.json
```

Pure stdlib — no venv, no install. Exit `0` = pass, `1` = fail (fix the plan), `2` = the
file is missing or not valid JSON.

## When to run

- **Runbook Stage 5 (plan check)** — the primary gate. Runs *before any render*, so a
  collapsed plan is caught while fixing it is free.
- **Runbook Stage 7 (verification gate), check #10** — re-run against the final plan the
  render was built from, so the shipped video provably matches its declared mix.

## What it enforces

- `declared_mix` exists and is complete (`intent`, `modes_used`, `dominant`,
  `single_mode`, `pace`).
- Exactly one non-clean family used **and** `single_mode` not declared → **FAIL**
  (the collapse case).
- `single_mode: true` but the plan actually mixes → **FAIL** (declaration contradicts plan).
- `declared_mix.modes_used` must equal the modes actually present in `beats[]`.
- Every `is_effect_moment` beat has a `reason` (N7); `camera_template_id` is an accepted
  N10 atom (`T1`–`T4`, never the rejected `T5`).

## What it does NOT do

It does not judge whether the mix is *good* — only that the plan matches its own
declaration and did not silently collapse. Taste stays with the director. It reads the
plan, not pixels; pairing it with the Stage-7 pixel checks (occlusion, seams, holds)
gives both "the plan is honest" and "the render obeys the plan."
