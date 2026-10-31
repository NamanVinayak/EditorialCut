---
title: Creative Director Pipeline Design
type: design-spec
status: approved-in-conversation
approved_by: the project lead
date: 2026-07-15
---

# Creative Director Pipeline Design

## Decision

Build the remaining editing agent through a **guided co-directing process**.
The agent does the recovery, synthesis, drafting, planning, execution, and
verification. the project lead remains the creative acceptance test at a small number of
meaningful review gates. the project lead does not need to repeat the 24 original video
walkthroughs or approve every sentence while it is written.

This plan was explicitly approved by the project lead on 2026-07-15.

> **Scope correction (the project lead, 2026-07-16) — what was and wasn't approved.** The approved
> thing is the *guided co-directing direction* and the capability/taste work (Phases
> 1–3). The **detailed Phase 4–5 automation** below (beat-map planner + assembly
> harness) was **AI-drafted and is NOT committed work.** the project lead clarified that building
> an automated pipeline is *optional and deferred*: the chosen next path is the
> **map-awareness layer** (make the system know and use its own already-built skills —
> `skills/CATALOG.md` + `docs/rulebook/orchestration-runbook.md`) plus a **manually directed
> short test**. Automation is only worth building if a real need (speed / cost / volume)
> appears *after* the taste is proven by hand. Read Phases 4–5 as a possible future
> shape, not a green-lit build.

> **Historical input-scope note (approved 2026-07-16).** This document's supplied
> rough-cut / add-only v1 remains the correct historical design for today's
> `POLISH_LOCKED` mode. The later approved
> [`2026-07-16-input-routing-and-base-edit-design.md`](2026-07-16-input-routing-and-base-edit-design.md)
> extends the system to explicitly authorized `ASSEMBLE_RAW`, `COMPOSE_FROM_PARTS`,
> and `HYBRID_SCOPED` base-edit work. It does not retroactively make the automated
> Phase 4–5 factory approved, and the original body below is intentionally preserved.
> The active operational rule is
> [`docs/rulebook/input-routing.md`](../../rulebook/input-routing.md).

## What already exists

The project already has the editor's eyes, ears, and several proven hands:

- shot detection;
- beat and downbeat detection;
- independent speech/music/silence layers;
- dialogue-aware music ducking and frequency carve;
- presenter masking and alpha compositing;
- inner-luminance subject treatment;
- geometric mask primitives;
- a working presenter-world slice with depth-split graphics, transcript-word
  timing, mild virtual-camera motion, and canvas swaps;
- 24 canonical reference documents;
- the accepted taste-grounded Phase 2 rulebook at
  `docs/rulebook/beat-to-primitive-rules.md`; it contains 12 creative-
  constitution principles, 21 fully specified buildable rules, and 17 future
  families.

The main missing component is editorial judgment: the layer that understands
the story, chooses the intended audience feeling, controls intensity and
restraint, selects a coherent visual language, and turns those decisions into an
executable timeline.

## Target workflow

```text
rough cut
  -> analysis assets
  -> story + emotion map
  -> creative direction
  -> beat map
  -> asset derivation/resolution
  -> skill execution + assembly
  -> design-consistency pass
  -> technical + editorial quality control
  -> polished edit
```

The first end-to-end version **adds and elevates; it does not recut** the project lead's
rough edit.

## Engine and reuse architecture — accepted direction 2026-07-15

The editing agent is the control layer above existing engines. It should not rebuild
rendering, compositing, audio, or orchestration capabilities that the project already
has.

| Layer | Default responsibility |
|---|---|
| Creative director + rulebook | Decide why, what, when, and how much |
| Accepted project skills | Define the editing job, inputs, procedure, and acceptance evidence |
| HyperFrames | Default authoring path for new typography, motion graphics, captions, cards, and section canvases |
| Remotion | Specialist for alpha/video compositing, presenter-world depth, footage-heavy or complex per-frame compositions, and accepted Remotion implementations |
| FFmpeg | Audio treatment, deterministic media filters, simple composites, transcodes, muxing, and final assembly |
| Video Use | Reusable orchestration, timeline, caption/explicitly-authorized-grading, assembly, and rendered-output review patterns; its automatic recutting is excluded from v1, and its grading path requires `color_authority: explicit` |
| Asset resolver | Author, generate, adapt, source, or reuse permitted visual/material assets |

Routing is reuse-first:

1. use an accepted capability's proven runner;
2. search existing skills, HyperFrames catalog/registry components, and project
   implementations;
3. use HyperFrames for ordinary new motion-design work;
4. route alpha-heavy, footage-heavy, or complex frame logic to Remotion;
5. route native media/audio/assembly operations to FFmpeg;
6. reuse Video Use helpers or patterns where they fit the add-only workflow;
7. author custom code only after recording why existing paths are insufficient.

The default engine is a routing preference, not a permanent dependency. Standard
contracts—timing JSON, masks/alpha media, normal image/video assets, audio stems, and
rendered clips—keep execution paths replaceable.

## Working relationship

### Agent owns

- recovering and deduplicating source evidence;
- drafting all documents and schemas;
- identifying contradictions and unresolved decisions;
- translating taste into explicit, reusable instructions;
- proposing beat maps and execution plans;
- running tools, rendering, and mechanical verification;
- inspecting pixels/audio directly before reporting success.

### the project lead owns

- whether the recovered taste feels true;
- whether the creative direction matches the intended audience feeling;
- visual-taste acceptance during the design pass;
- the final judgment on rendered edits.

the project lead reviews at defined gates rather than rewriting the documents or repeating
old context.

## Phase 1 — recover and validate the project lead's taste

### Primary evidence

own recovered turns for Videos 01-24, with the original tool, timestamp, source
path, and source fingerprints. It excludes agent summaries.

The canonical per-video study documents (private library, not shipped) remain supporting
evidence for verified mechanics, frames, timing, and implementation reasoning.
They do not override the project lead's stated reason for saving a video.

### Deliverable

Create one concise per-video taste map. Each video records:

- why the project lead saved it;
- what he specifically loved or considered important;
- the intended audience feeling;
- which visible choices created that feeling;
- what transfers to unseen footage;
- what is only a disposable example or provider detail;
- confidence/richness of the recovered first-person evidence;
- exact prompt and canonical-document provenance.

The taste map must distinguish **the project lead's stated taste**, **directly verified
mechanics**, and **the agent's inference**. Never merge those into one claim.

### Review gate 1

the project lead reviews the concise 24-video map and corrects only misunderstandings or
missing emphasis. Do not revise the rulebook before this gate is accepted.

**Accepted 2026-07-15:** the project lead approved the private 24-video taste
map (not shipped). The map is now the primary taste
input for Phase 2 alongside the recovered first-person prompt archive.

## Phase 2 — rebuild the beat-to-primitive rulebook

Improve the existing draft rather than replacing it blindly.

### Layer A: creative constitution

The rulebook begins with the principles that govern every move:

- preserve the intended audience feeling even when the content changes;
- make presenter and graphics feel like one designed world;
- motivate movement through narration or emotional change;
- elevate important moments rather than decorate every sentence;
- build and release visual intensity across a section;
- keep a coherent grammar within a section;
- use scarcity to protect high-impact moves;
- know when leaving the footage alone is stronger;
- derive elements for the current footage; do not treat worked examples as an
  asset library;
- polish the supplied rough cut; do not recut it in v1.

### Layer B: executable rules

Each rule includes:

- narrative purpose;
- intended audience feeling;
- detectable trigger or editorial judgment;
- editing move;
- timing, intensity, and depth settings;
- restraint and frequency rules;
- when not to use it;
- required inputs and executing skill;
- fallback behavior;
- first-person taste provenance and verified source evidence;
- buildable-now or future status.

Keep the two accepted source-versus-taste differences explicit: Video 04's
2-3-frame tutorial flash versus the project lead's accepted 4-5 frames, and Video 13's
roughly 0.5-octave notch versus the accepted 1.5-octave constructed-mix setting.

### Review gate 2

Review the rulebook in a few coherent sections, followed by one complete pass.
Do not update the rulebook's status to final until the project lead signs off.

**Accepted 2026-07-15:** the project lead approved the rulebook and chose contextual,
story-specific concept visuals for F11 instead of a permanent keyword-to-stock-
icon lookup.

## Phase 3 — creative-director instructions

Create the decision layer above the individual skills. It must:

1. understand the rough cut's thesis, story, evidence, explanations, emotional
   turns, climax, conclusion, and breathing spaces;
2. divide the timeline into narrative/emotional beats;
3. decide which moments deserve treatment and which should remain clean;
4. choose a dominant visual grammar per section;
5. control density, escalation, contrast, repetition, and recovery time;
6. select rulebook moves and the skills that can execute them;
7. describe new context-specific elements to derive, author, generate, adapt,
   or source;
8. output a beat map before rendering;
9. critique the plan for incoherence, effect overload, or unsupported choices.

The director owns **why, what, when, and how much**. Rendering skills own the
mechanics of **how to execute** an approved move.

### Review gate 3

the project lead reviews the director instructions and a sample plan before the automatic
assembly system is built.

## Phase 4 — beat-map planner

> **Deferred / optional (2026-07-16).** This is AI-drafted, not committed work. The
> *beat map as a document the director fills in* is used today by hand; the *automated
> planner* described here is only worth building if a real need appears after the taste
> is proven. See the scope correction at the top.

Define a human-readable beat map and a machine-readable equivalent. Each entry
contains:

- time window and spoken words;
- narrative function;
- intended audience feeling;
- selected visual treatment;
- depth/layer placement;
- camera behavior;
- typography/caption behavior;
- audio treatment;
- intensity and scarcity class;
- asset-derivation brief;
- capability identifier;
- preferred engine (`auto` by default) and genuine engine constraints;
- rationale, confidence, and fallback.

Planner validation must catch overlapping treatments, unreadable durations,
excessive density, repeated scarcity effects, missing inputs, and choices that
contradict the section's visual grammar.

Default first-version workflow: show the project lead the proposed beat map before a costly
render. Full autonomy can follow after the planner's judgment proves reliable.

## Phase 5 — assembly harness and mechanics dry-run

> **Deferred / optional (2026-07-16).** AI-drafted, not committed. Today the skills are
> chained *by hand* (an agent runs each per `skills/CATALOG.md`). Building an automated
> harness is optional and only justified by speed/cost/volume needs after the taste is
> proven. See the scope correction at the top.

Build the production line that:

- generates or reuses the accepted analysis assets;
- reads the beat map;
- invokes the correct skills;
- routes each approved capability through its proven runner or the reuse-first engine
  policy before allowing custom implementation;
- resolves context-specific visual elements without ossifying examples into an
  asset library;
- assembles picture, graphics, captions, and audio;
- renders one timeline;
- runs technical and editorial checks;
- produces lightweight review evidence.

First run a cheap roughly-one-minute mechanics test. It proves data flow,
timing, layer order, and assembly—not finished visual taste.

### Review gate 4

the project lead reviews the one-minute mechanics edit and identifies planning or assembly
failures without treating diagnostic styling as the final design.

## Phase 6 — unified design pass

Give the accepted mechanics one coherent contemporary visual language:

- typography roles and font families;
- adaptive caption families;
- color systems;
- textures and stylization;
- motion curves and animation character;
- spacing, layout, and negative space;
- transition language;
- effect scarcity and section-to-section continuity.

### Foundation Texture Pack v1 — completed 2026-07-15

A small, licensed foundation collection now exists at
`assets/foundation-textures-v1/` for material treatments that are stronger as
real still or moving plates than as purely procedural effects:

- paper and paper-fiber scans;
- crumpled, folded, torn, and rough-edged paper;
- canvas and fabric surfaces;
- ink bleed, ink misalignment, stains, and distressed reveal mattes;
- film-grain plates at a small number of useful intensities;
- seamless film-dust, scratch, flicker, and light-leak loops.

Every external asset records source, licence/reuse permission, resolution, frame
rate where relevant, tiling/looping behavior, recommended blend modes, and intended
material/story uses. Prefer a few excellent, adaptable assets per family over a
large undirected download dump.

This collection does not violate the derivation-recipe principle. The foundation
pack supplies reusable raw materials; the director still derives the treatment for
the current footage. Source-specific ribbons, icons, photos, example layouts, and
semantic graphics do not enter this pack. Procedural gradients, shapes, grids,
masks, halftones, and similar tunable effects remain code-generated when practical.

The completed pack contains 20 inspected production files (~111 MB), three
contact-sheet previews, a measured per-file manifest, license ledger, editing-use
guidance, and SHA-256 checksums. ambientCG/Openclipart foundations are recorded as
CC0/public domain; Pixabay assets are marked internal-production-only because its
Content License prohibits standalone stock redistribution. The one-minute mechanics
dry-run may still use procedural or diagnostic placeholders. The prerequisite that
Foundation Texture Pack v1 exist before representative style frames are approved at
Review gate 5 is satisfied.

Prioritize future capabilities that materially affect the first end-to-end
edit: adaptive captions, texture/stylization recipes, typography role selection,
and color/style unification. Other future families remain conditional on a real
edit need.

### Review gate 5

the project lead reviews representative style frames and motion samples before the full
five-minute test.

## Phase 7 — official five-minute test

the project lead provides an old roughly-five-minute rough cut and asks the system to make
it pop, with creative direction included. The system analyzes, directs, plans,
derives assets, assembles, checks, and renders the polished edit.

### Review gate 6

the project lead judges the completed edit by eye and ear. This is the acceptance test for
taste and mechanics together.

## Quality-control contract

Before presenting an edit, verify:

- graphic and typography arrivals match the intended words/beats;
- presenter mattes and depth contacts are visually correct;
- camera motion does not double or detach the presenter;
- typography and evidence remain readable for their full intended hold;
- audio treatment supports dialogue without obvious pumping;
- scarcity effects are not repeated casually;
- the intensity curve contains breathing space;
- the section maintains a coherent visual grammar;
- the final treatment serves the intended feeling rather than merely proving a
  renderer can draw the effect.

## Resolved decision

Rule F11 was accepted on 2026-07-15: treat “keyword -> icon” as “idea ->
contextual concept visual.” The director specifies the communicative need;
execution may author, generate, adapt, or source a suitable visual at run time.
The project knowledge does not become a permanent stock-icon library. An icon
remains available when it is contextually the best visual, never as an automatic
keyword response.

## Exact resume point

Start a fresh session. Read, in order:

1. `AGENTS.md`;
2. the private handoff log;
3. `CLAUDE.md`;
4. this design spec;
5. the private 24-video taste map (not shipped);
7. `docs/rulebook/beat-to-primitive-rules.md`.

Phases 1 and 2 are accepted, and F11 is resolved. The exact next action is
**Phase 3: create the creative-director instructions and a sample creative plan
for Review gate 3.** Do not build the automatic planner or render. Foundation
Texture Pack v1 is already complete at `assets/foundation-textures-v1/`; do not
expand it during Phase 3 unless a real missing material blocks the approved plan.

Fresh or compacted sessions should restart from
`docs/rulebook/phase-3-creative-director-resume-prompt.md` rather than reopening
the original chat archives or the completed Phase 1 prompt.

## Repository note

The workspace root is not a Git repository, so this design spec cannot be
committed here. It is preserved through the living project documentation and
matching project memory instead.
