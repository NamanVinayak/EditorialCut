---
title: Shot Detection
aliases:
  - Shot Boundary Detection
  - Detect Shots
type: capability
status: accepted-v1
updated: 2026-07-13
---

# Shot Detection

## Decision

**Accepted for v1. Move on.** The current local detector is good enough for its intended job: making an initial visual index of ordinary footage and rough edits. Do not continue tuning it merely to cover every possible motion-graphics edge case. Reopen it only if a real editing project exposes a blocking failure.

No formal 95% accuracy claim was established because the project lead did not label every candidate and every missed boundary. He visually reviewed the four-video package, found most major changes correct, identified the limitations below, and explicitly accepted the capability for its intended use.

## Editorial purpose

This is an assistant-editor logging step. It divides a long source into manageable camera/edit sections so later analysis can inspect a few useful frames from each section instead of scanning every frame.

It is **shot-boundary detection**, not complete story-scene understanding. Several shots may belong to one narrative scene. A stable designed canvas may also contain several changing panels without becoming several top-level shots.

### Use it for

- Initial ingest of vlogs, talking-head footage, basic edits, and rough cuts
- Isolating provisional shot clips
- Reducing the number of frames needed for B-roll and visual analysis
- Reusing shot timing for transcript, audio, and later editing skills

### Do not use it as

- A semantic story-scene grouper
- A perfect interpreter of motion-graphics layouts
- Proof that every internal panel/image change is a new shot
- A reason to rerun analysis after the accepted shot map is saved, unless the source or timeline changes

## Proven implementation

- Workspace: `research/shot-detection/`
- Local isolated environment: `.venv` with CPython 3.12.13
- Primary baseline: PySceneDetect 0.7 `AdaptiveDetector`
- Comparison passes: sensitive Adaptive, Content baseline, and FFmpeg `scdet`
- Review surface: static local HTML with isolated scenes, boundary clips, exact before/after frames, detector votes, notes, and human labels
- Verification: 23 tests passed; 517 generated artifacts decoded/parsed/resolved
- Sources remained read-only

The reusable agent procedure is [`skills/detect-shots/SKILL.md`](../../skills/detect-shots/SKILL.md). Private benchmark evidence is not distributed; reproduce it with the shipped runner and your own footage.

## Confirmed benchmark

| Source | Editorial challenge | Provisional scenes | Review candidates |
| --- | --- | ---: | ---: |
| Video 01 | Virtual-camera motion and graphic reveals | 14 | 19 |
| Video 04 | Dense editing and frame-within-frame montage | 61 | 70 |
| Video 15 | Image/design replacements | 26 | 26 |
| Video 19 | Repeated studio layouts and red/blue state changes | 12 | 11 |
| **Total** |  | **113** | **126** |

## Human-observed limits

1. **Flashy transitions have width.** The proposed cut point can land inside a flash, wipe, or blend. When exact transition timing matters, interpret it as a start-to-end range during review rather than trusting one edge frame.
2. **Nested visual events are different from top-level shots.** Video 04 shows multiple image panels changing inside a related graphic canvas. A whole-frame detector sees major pixel change; an editor may see one designed sequence evolving internally.
3. **Polished motion graphics need richer inspection.** Use the current result as a coarse index and inspect extra frames. Do not increase sensitivity until every panel pop becomes a false "shot."

These are accepted limitations, not blockers for ordinary ingest.

## What exists now versus later

| Available now | Manual/downstream extension |
| --- | --- |
| Boundary candidates from four detector opinions | Exact start/end ranges for gradual transitions |
| Provisional isolated scene clips | Internal panel/montage event labels |
| Boundary clips and before/after stills | About two safe representative frames per accepted shot |
| Browser review and downloaded labels | Extra samples for long or visually active shots |
| Raw detector settings/results and artifact verification | Semantic grouping of shots into story scenes |

Do not describe the right-hand column as automated by the current runner.

## Operating rule

Confirm the exact video files and their intended use with the project lead before running a new benchmark. Keep originals immutable, store all outputs separately, show the result for editorial review, state uncertainty honestly, and stop improving once the capability is accepted for its purpose.

## Capability sequence update

the project lead moved subject masking ahead of audio. That capability is now accepted and documented in [`subject-masking.md`](subject-masking.md). He subsequently chose to finish the other masking/tracking/occlusion jobs before audio. Current order belongs to the root the project review log; shot detection remains closed unless real edit work exposes a blocking failure.
