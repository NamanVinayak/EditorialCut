---
title: Input Routing and Base-Edit Authority
type: process-rule
status: approved-v1
updated: 2026-07-19
governing_spec: ../superpowers/specs/2026-07-16-input-routing-and-base-edit-design.md
---

# Input Routing and Base-Edit Authority

## Purpose

This is the assignment router in front of the creative-director workflow. It decides
how much editorial control the user granted, whether a base edit must be created, and
which review gates must pass before visual polish begins.

It is not a renderer, skill, planner factory, or second director. One director keeps
the full story and taste context. Existing skills, HyperFrames, Remotion, FFmpeg, and
selected Video Use patterns remain execution options.

## Rule

**User intent plus explicit authority outranks file type.** A folder of raw clips does
not automatically grant recut permission. A flattened MP4 does not automatically mean
its structure is locked.

Read-only inventory and analysis may continue while authority is unresolved.
Selection, shortening, reordering, replacement, or newly authored editorial timing may
not begin until authority is clear.

**Color authority is separate from cut authority and is source-locked by default.**
No route grants color correction or grading by implication. “Cinematic,” “visual
polish,” “complete pass,” “cohesive look,” “make it pop,” or similar language may guide
design and pacing, but it does not authorize changing source-footage color. The user
must specifically request color work; otherwise preserve the source appearance.

## Modes

| Mode | Authority | Typical request | Base-cut rule |
|---|---|---|---|
| `POLISH_LOCKED` | `locked` | A supplied edit plus “package this,” “add graphics,” or “make it pop” | Preserve the supplied selection, order, and editorial timing unless authority is expanded. |
| `ASSEMBLE_RAW` | `assemble` | Raw footage, multiple takes, an interview, or a long recording that must become a reel/edit | Select, shorten, order, and assemble material inside the approved story target. |
| `COMPOSE_FROM_PARTS` | `compose` | A script, voice-over, audio, stills, screen recordings, notes, data, or mixed parts that must become a video | Create story structure and a base timeline inside the approved brief. |
| `HYBRID_SCOPED` | `scoped` | A partial edit plus pickups, replacement sections, or optional raw material | Preserve named locked material and change only named sections or sources. |

The modes describe authority, not engine or quality. No mode is automatically more
creative than another.

## Route contract

Record this compact contract in the edit's working log before structural mutation:

```yaml
assignment_mode: POLISH_LOCKED | ASSEMBLE_RAW | COMPOSE_FROM_PARTS | HYBRID_SCOPED
requested_outcome: string
cut_authority: locked | assemble | compose | scoped
color_authority: unchanged | explicit
requested_color_work: none | exact-user-request
locked_material: string-or-none
editable_material: string-or-none
target_length_or_platform: string-or-unresolved
story_source: supplied-cut | supplied-brief | transcript-derived | mixed
required_review_gate: supplied-base | strategy-and-rough-cut | scoped-rough-cut
unresolved_authority: none-or-exact-question
```

If `unresolved_authority` is not `none`, inventory and analysis may continue but
structural editing must wait. Ask one concrete question that distinguishes the
plausible routes.

`color_authority` defaults to `unchanged` on every route. Set it to `explicit` only
when the user's request specifically names color correction, grading, white balance,
exposure, contrast, saturation, gamma, hue, temperature, LUT application, relighting,
or another source-image color change, and copy that request into
`requested_color_work`. If color work seems desirable but was not requested, omit it;
do not infer permission from a style adjective.

With `color_authority: unchanged`, HyperFrames, Remotion, FFmpeg, Resolve, and any
other execution engine must omit corrective or aesthetic color-transform nodes and
filters. A technical color-space conversion is allowed only when necessary to preserve
the source appearance through delivery; document it and verify a visual match. This
does not prevent choosing colors for newly added graphics, provided those graphics do
not alter the underlying footage's color.

## Decision table

Apply the first row supported by the user's requested outcome and granted authority.

| Evidence | Route | Action |
|---|---|---|
| Supplied cut plus a visual/audio packaging request | `POLISH_LOCKED` | Identify it as the base cut and enter polish. |
| Explicit request to turn raw footage or multiple takes into a reel/edit | `ASSEMBLE_RAW` | Analyze, approve strategy, create selects/EDL, and review the rough cut. |
| Explicit request to create from script, voice-over, notes, stills, screen recordings, or mixed parts | `COMPOSE_FROM_PARTS` | Approve story/asset strategy, build the base timeline, and review the rough cut. |
| Protected material plus named replaceable sections or sources | `HYBRID_SCOPED` | Record the scope map and change only the editable region. |
| Files imply several routes but authority is absent | unresolved | Inventory only and ask what may change. |
| An unfamiliar job has clear authority | nearest supported mode | Decompose it into catalogued capabilities and report any genuine missing dependency. |

Do not select `ASSEMBLE_RAW` merely because raw media exists. Do not select
`POLISH_LOCKED` merely because one flattened video exists.

## Gates and convergence

### `POLISH_LOCKED`

Identify the supplied edit as the base cut. Record its file/timeline identity and the
locked authority. No separate rough-cut construction gate is needed unless the user
later expands the requested scope.

### `ASSEMBLE_RAW`, `COMPOSE_FROM_PARTS`, and `HYBRID_SCOPED`

Before structural cutting, approve a concise user-facing strategy covering:

- intended story and audience outcome;
- likely structure and selection rule;
- protected material and editable scope;
- target duration/platform; and
- important uncertainty.

A direct user instruction that already supplies these choices may satisfy the strategy
gate when it is recorded in the route contract.

Then create and render the rough cut. Do not begin full visual polish until the user
accepts that render. On acceptance, record:

- the rough-cut file and SHA-256, or a stable timeline/version identity;
- source manifest and fingerprints;
- selects/EDL or structure record;
- assignment mode and cut authority;
- locked/editable scope where applicable;
- known issues intentionally deferred to polish; and
- acceptance status and date.

A later structural change reopens the rough-cut gate and produces a new base-cut
identity.

### Convergence

Every accepted base cut then enters the same downstream workflow:

```text
accepted/frozen base cut
  -> story read
  -> beat map
  -> visual contract and asset route
  -> build through accepted skills / HyperFrames / Remotion / FFmpeg
  -> editorial verification
  -> rendered review
```

Analysis assets created before assembly are reusable. Do not re-run transcription,
shot detection, or contact-sheet extraction merely because the route has converged.

## Mechanical source-analysis rules

- Use local MLX Whisper **Large V3** with word timestamps and the project's existing
  ASR quality-control rules. Do not adopt Video Use's transcription default.
- Run shot detection, audio analysis, and contact-sheet extraction as relevant.
- Preserve source fingerprints and timecode provenance.
- Preserve source-footage color unless the route records
  `color_authority: explicit` and the exact requested color work.
- Reuse Video Use's selects, EDL, word-boundary, short padding/fade, and rendered
  boundary-review patterns only inside authorized base-edit modes.
- Hindi speech rendered as on-screen text follows the existing Hinglish register and
  zero-Devanagari verification rule.
- Originals remain immutable. Derived assets and renders live in the edit's approved
  working directory.

## Image-generation node

Image generation is a capability node, not an intake mode, editor, or renderer.

### Default placement

The default route is:

```text
accepted/frozen base cut
  -> story and beat decision
  -> visual contract with asset_route: generated-still
  -> plan check
  -> image brief derived from that contract
  -> native image-generation ability
  -> director pixel acceptance or one re-brief
  -> accepted still in assets-generated/
  -> animation/compositing in HyperFrames or Remotion
  -> editorial verification
```

The image generator may create a background, illustration, photographic plate,
isolated cutout, or missing texture. It does not choose the story, source selection,
cut, timing, typography, depth, or motion.

### Narrow early exception for `COMPOSE_FROM_PARTS`

After the story/asset strategy is approved, the director may generate an early
contracted structural still when a placeholder cannot make the rough cut meaningfully
reviewable. Generate only what is required to judge the base edit. Re-check the asset
against frozen timing after rough-cut acceptance. This is not permission to polish the
whole film before its structure is approved.

Every early or ordinary generated still requires a visual contract and director pixel
acceptance. Text-only briefs remain the default. Uploading unpublished footage frames
requires the project lead's per-asset approval. Preserve provider, date, contract ID, optional
donor ID, full brief, and SHA-256 provenance under the existing `generate-image`
contract.

## Unexpected jobs

When a request does not match a named workflow:

1. classify the requested result and granted authority;
2. decompose it into editing jobs rather than repository names;
3. consult `skills/CATALOG.md` before proposing new implementation;
4. reuse accepted analysis assets and portable contracts;
5. select the nearest supported assignment mode when authority matches;
6. state the exact missing permission or dependency when one genuinely exists; and
7. use custom code only after accepted runners, HyperFrames, Remotion, and FFmpeg are
   insufficient.

Do not install a new dependency, overwrite source, fabricate a story, or silently
expand authority. If the supplied facts cannot support a coherent story, state the gap
or the honest competing structures.

## Failure rules

- **Ambiguous permission:** inventory only and ask before structural editing.
- **Missing or unreadable source:** report the exact file/stream failure and preserve
  other valid work.
- **Low-confidence transcript:** apply the existing ASR QC before word-precise cuts.
- **No viable story:** state the gap or honest alternatives; do not fabricate evidence.
- **Rejected rough cut:** revise structure/EDL; do not conceal the problem with
  graphics.
- **Locked area needs change:** request expanded scope and issue a new route contract.
- **Generated image fails twice:** change asset route instead of stacking prompt
  patches.
- **Missing tool or provider:** state the requirement and fallback; do not install or
  upload without authority.
- **Source safety:** originals remain immutable; derived artifacts retain provenance.

## Scenario checks

1. **Finished rough cut + “make it pop”:** `POLISH_LOCKED`; no structural recut; image
   generation only after a beat and visual contract justify it.
2. **Twelve raw takes + “make a 45-second reel”:** `ASSEMBLE_RAW`; strategy, EDL,
   rough-cut review, then polish.
3. **Script + voice-over + stills:** `COMPOSE_FROM_PARTS`; strategy, optional early
   contracted structural stills, rough-cut review, then final assets.
4. **Partial cut + raw pickups for the middle:** `HYBRID_SCOPED`; opening/end locked,
   middle editable, new base identity before polish.
5. **Unlabelled media folder + “see what you can do”:** unresolved authority;
   read-only inventory and one authority question before cutting.
