# Editorial Treatment Selection — Design Specification

**Date:** 2026-07-18
**Status:** approved by the project lead
**Benchmark:** `screenwriting-masterclass-20260718`
**Scope:** reusable editorial judgment, presenter-world typography, camera-safe layout,
caption timing, and verification. The current full film is evidence, not a requested
re-edit.

## Problem

The screenwriting film showed that the system can produce a coherent visual direction,
masked presenter depth, camera movement, and designed typography, but the director and
generic renderer collapsed several different storytelling jobs into the same
`overlay_accent` answer.

The representative failures were:

- an identity introduction (`SAMPLE PRESENTER`) whose necessary text was obscured;
- a transformation (`HERO → ZERO`) treated as ordinary side text rather than a large
  environmental statement whose phrase survives controlled presenter occlusion;
- a thesis (`CONFLICT → DRAMA`) whose text left the visible frame during a camera push;
- captions that remained visible through pauses because the renderer selected the last
  started word rather than respecting its end time, amplified by impossible ASR spans.

All effects were present in the reviewed video. the project lead supplied screenshots only for the
moments on which he had comments. The failure is not missing review coverage, nor is the
text-behind-presenter technique rejected.

## Goal

Connect the system's story read to an executable design intention so that different
editorial jobs can receive different, coherent typography, depth, scale, and motion—and
so semantic text remains readable throughout the final camera trajectory.

## Non-goals

- Do not rebuild the complete screenwriting film.
- Do not ban consecutive rear typography.
- Do not introduce a quota for fonts, effects, or masked beats.
- Do not create source-specific templates for `SAMPLE PRESENTER`, `HERO → ZERO`, or the
  screenwriting look.
- Do not change masking, RVM, source media, audio mixing, input routing, shot detection,
  accepted camera templates, or the mode-mix policy.
- Do not silently rewrite canonical transcript evidence.
- Do not add unlicensed font files.

## Editorial decision contract

Every treated typography beat carries a small `design` object:

```ts
interface BeatDesign {
  job:
    | "identity"
    | "transformation"
    | "thesis"
    | "comparison"
    | "evidence"
    | "quote"
    | "annotation"
    | "utility"
    | "atmosphere";
  type_role: "attention" | "identity" | "editorial" | "annotation" | "utility";
  scale: "support" | "feature" | "environmental";
  depth: "front" | "rear" | "mixed" | "screen";
  readability: "full" | "recoverable" | "decorative";
  edge_policy: "contain" | "intentional_crop";
}
```

These values do not replace director judgment. They preserve it through delegation,
rendering, and verification.

Semantic invariants:

- `identity`, `evidence`, and `utility` require `readability: "full"`.
- `readability: "decorative"` is invalid for identity, transformation, thesis,
  comparison, evidence, quote, or utility.
- `intentional_crop` is allowed only for environmental type whose necessary reading is
  still explicitly recoverable.
- Repeating a treatment is allowed. Three nearby beats with the same treatment, scale,
  depth, and type role produce a warning for director review, not an automatic failure.

## Typography system

The look derives a coherent role palette per video:

- `attention` — major claims and transformations;
- `identity` — names and factual introductions;
- `editorial` — quotations and reflective language;
- `annotation` — handwritten/cursive accents used selectively;
- `utility` — labels, indices, dates, and proof;
- `caption` — continuous speech coverage.

One family may fill several roles. Different families are allowed when the register
supports them. The engine never chooses fonts randomly and never requires a fixed count.

## Treatment vocabulary

The generic kit adds one `type_treatment` renderer with five compositional variants:

- `identity_lockup` — complete, quickly readable identification;
- `hero_field` — oversized environmental type, normally rear or mixed depth;
- `thesis_build` — a phrase assembled in deliberate reading order;
- `editorial_note` — editorial/annotation type with restrained emphasis;
- `support_overlay` — the existing quiet side treatment.

`overlay_accent` remains supported for old beat maps.

The treatments are generic relationships, not stored examples. Beat data supplies the
words, timing, tone, placement, and design contract; per-video look data supplies fonts
and colors.

## Camera-safe layout

The camera engine exposes the visible world rectangle for any camera state. A treatment
uses the intersection of the visible rectangles sampled at:

- beat start;
- each camera-leg start and end;
- each camera-leg midpoint;
- beat end.

For `edge_policy: "contain"`, the semantic text box must fit inside that intersection
with the video's safe margin. `intentional_crop` may extend beyond the safe region but
still receives a director-reviewed recovery frame.

Presenter occlusion and frame-edge cropping are separate decisions:

- depth/readability govern what the presenter may cover;
- edge policy governs what the camera viewport may crop.

## Caption behavior and QC

At time `t`, a caption word is active only while:

```text
word.t <= t <= word.e + end_grace
```

The default end grace is short and configurable. A pause after the last word clears the
caption instead of holding it until the next word begins.

The data preflight fails on malformed, unsorted, overlapping, or impossible caption
timings, including extremely long single-word spans. It reports the offending word and
time range and never edits the transcript.

## Plan and verification behavior

The data preflight:

- validates the new design contract for `type_treatment` beats;
- validates renderer/content compatibility;
- validates caption timing and zero Devanagari;
- fails semantic contradictions;
- warns on local treatment repetition.

The director still judges:

- whether a treatment fits the story;
- whether recoverable text is actually recoverable;
- whether font pairing is coherent;
- whether repetition feels intentional;
- whether a clean frame would be stronger.

Review evidence for each treated moment includes surrounding handles plus start, arrival,
camera midpoint, landing, and release frames. A continuous section reel supplements—not
replaces—the individual effect previews.

## Compatibility

- Existing `overlay_accent` beat maps continue to render.
- New `design` fields are required only for `type_treatment` beats.
- Existing look files remain valid through fallbacks from the new role names to the old
  `display`, `kicker`, and `quote` keys.
- No existing benchmark data is rewritten merely to satisfy the new schema.

## Acceptance evidence

Automated:

- the preflight's regression tests demonstrate red→green behavior;
- all kit tests pass;
- `npm run lint` passes;
- current legacy edit data still passes compatibility checks;
- malformed caption fixtures fail with specific messages.

Rendered:

- identity proof: the complete name remains readable for the full treatment;
- hero-field proof: the complete transformation is understood despite controlled
  presenter occlusion;
- thesis proof: necessary text stays within the frame throughout the camera move;
- caption-gap proof: no caption remains visibly stuck during silence.

Only short proofs are required. A separate-genre proof is selected by the project lead before use.
