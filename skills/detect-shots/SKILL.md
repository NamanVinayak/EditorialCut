---
name: detect-shots
description: Invoke to detect shot/cut boundaries over footage or a rough cut and emit shot-boundary indexing, isolated shot clips, or representative frames for later B-roll and editing analysis. Do NOT eyeball cut points or hand-roll a scene-change ffmpeg command; run this detector.
---

# Detect Shots

## Overview

Create an assistant-editor's shot map: divide ordinary footage into useful sections while preserving uncertainty.

## Workflow

1. **Confirm scope.** List the source files and what each tests. Get the project lead's confirmation before choosing videos or changing the use case.
2. **Protect sources.** Treat originals, canonical transcripts, and reference documents as read-only. Write every derived artifact to a separate run directory.
3. **Reuse the local runner.** In EditorialCut, use `research/shot-detection/`; never install into system Python. Copy `benchmark.json` to the run directory and replace only confirmed video entries with absolute paths and plain-language `use_case` values.
4. **Run and verify.** From `research/shot-detection/`:

   ```bash
   uv run shotbench --manifest /absolute/run/benchmark.json --results-dir /absolute/run/results benchmark
   uv run shotbench --manifest /absolute/run/benchmark.json --results-dir /absolute/run/results prepare-review
   uv run shotbench --manifest /absolute/run/benchmark.json --results-dir /absolute/run/results verify
   ```

5. **Present evidence.** Give the user `review/index.html`, isolated clips, and a short results note. Humans judge ambiguity; detector agreement is not accuracy.
6. **Choose frames when requested.** This is downstream, not automated by `shotbench`. Select about two stable frames inside each accepted shot, away from transitions. Add samples for long, montage, split-screen, picture-in-picture, or active sections. Retain shot IDs and timestamps.
7. **Persist the map.** Downstream skills reuse it. Rerun only when the source or timeline changes.

## Interpretation

| Footage condition | Treat the output as |
| --- | --- |
| Ordinary vlog, talking head, basic edit, rough cut | A dependable first-pass shot index |
| Flash, wipe, dissolve, or blended transition | An approximate transition location requiring interval-aware review |
| Stable canvas with changing internal panels | One possible top-level shot with internal visual activity—not automatically many shots |
| Story/location grouping across several shots | A separate semantic-scene task |

## Current Output Contract

- Source identity and intended use case
- Detector versions/settings and raw candidates
- Contiguous provisional shot clips
- Review clips plus exact before/after frames
- Human review state and unresolved cases
- Verification result and honest known limitations

`shotbench` does **not** currently estimate transition start/end ranges, automatically classify internal panel activity, export representative-frame sets, or produce a final human-approved semantic shot map. Describe these as manual/downstream steps when requested; never present them as implemented detector outputs.

## Guardrails

- Do not claim a numeric success rate without complete human labels, including missed boundaries.
- Do not keep tuning after the project lead accepts the capability for its intended use. Record limitations and move forward; reopen it only when a real edit exposes a blocking failure.
- Do not make this skill responsible for understanding story scenes, motion-graphics semantics, or every internal panel event.
- In this project, read `docs/capabilities/shot-detection.md` for the accepted v1 decision and `research/shot-detection/results/BENCHMARK-RESULTS.md` for experiment evidence.
