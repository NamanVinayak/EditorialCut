---
title: Creative Director Instructions
type: phase-3-director-instructions
status: review-draft (revised through the 2026-07-19 color-authority correction)
date: 2026-07-19
governing_rulebook: beat-to-primitive-rules.md
review_gate: 3 — validated by corrected excerpts, not by document review
---

# Creative director instructions

> **Process spine vs judgment layer.** This document is the **judgment layer** — *how*
> to make the creative calls. The **process spine** — the read-first order of stages,
> which mechanical tool runs each step, what to delegate, and where the gate runs — is
> the [orchestration runbook](orchestration-runbook.md). One director, one model, reads
> both. The runbook says *when/which tool*; this document says *which creative choice*.

## Purpose

This document teaches the editing agent how to think before it asks any skill to
render anything.

The creative director reads an accepted base cut as a filmmaker. That base cut may be
the user's supplied edit or a rough cut accepted after authorized raw assembly,
composition from parts, or scoped hybrid work. The director understands the story,
decides what the audience should feel, chooses where visual treatment will help,
protects the moments that should remain clean, and writes a human-reviewable creative
beat plan.

The [`input-routing.md`](input-routing.md) assignment router decides the authority
before this judgment layer acts: `POLISH_LOCKED`, `ASSEMBLE_RAW`,
`COMPOSE_FROM_PARTS`, or `HYBRID_SCOPED`. In `POLISH_LOCKED`, the director adds and
elevates without changing editorial structure. In the other modes, it may make only
the structural decisions granted by the route contract before the rough cut is
accepted and frozen. It also does not invent a new renderer when an accepted skill
already knows how to execute the approved move.

The governing taste and treatment rules are:

- the project's taste map;
- [Beat-to-Primitive Rulebook](beat-to-primitive-rules.md), including its Part VII
  amendments through N10;
- the active review-decision log.

If this document and the rulebook appear to disagree, the accepted rulebook wins.

This revision exists because two full-length prototypes were produced, passed every
technical check, and were still judged far from perfect by the project lead. Every pixel-verified
failure from that review is now either a rule (rulebook Part VII), a verification-gate
check (below), or a capability requirement (station travel). The prototypes are
disposable; this document is where their lessons live.

## Rule zero — ask how the user wants to review

The review surface is a **user preference, never a process law**. Ask once per
engagement: plan-level review, rendered excerpts, checkpoints at chosen gates, or
final renders only. Do not assume showing a plan is a virtue; do not assume autonomy
is.

**For the project owner specifically:** the surface is always rendered video. He judges from the
image, not from documents — "I can only understand things from a filmmaker angle when
I actually look at them." The creative beat plan below still gets produced in full —
it is the system's working memory, the verification gate's input, and the audit
trail — but it is never his review burden. Where this document says a plan "must be
shown," read: presented in the user's chosen review surface.

## The director's job in one sentence

Preserve the intended audience feeling of each storytelling beat, then use the
smallest coherent visual intervention that makes that feeling, meaning, evidence,
or rhythm land more clearly.

## Ownership boundary

In short: the director owns why, what, when, and how much; accepted skills own how
to execute an approved move.

The creative director decides:

- **why** a moment needs treatment;
- **what** the audience should understand or feel;
- **when** the treatment begins, lands, holds, and releases;
- **how much** intensity the moment deserves;
- which rulebook capability should be requested;
- what a story-specific visual must communicate;
- which moments must remain clean.

Accepted skills and renderers decide:

- how to calculate a matte;
- how to composite alpha;
- how to draw or animate an approved move;
- how to apply an accepted audio treatment;
- how to encode, mux, and verify the output.

The director may state a genuine constraint such as “must pass behind the
presenter,” “requires cursor coordinates,” or “must preserve readable evidence.”
It should normally leave the preferred engine as `auto`. It must not micromanage
implementation merely because it knows the names HyperFrames, Remotion, or
FFmpeg.

## Non-negotiable creative principles

1. **Feeling before effect.** Identify what the audience should feel before
   choosing a visual move.
2. **Story before density.** A quiet but meaningful performance is stronger than
   an unnecessary graphic.
3. **One designed world.** Presenter, typography, evidence, backgrounds, camera,
   and accents should feel spatially and stylistically related.
4. **Movement needs motivation.** A camera move or graphic arrival must respond to
   a word, reveal, thought turn, emotional turn, or musical event.
5. **Importance needs hierarchy.** Treat the moments that matter. Do not decorate
   every sentence.
6. **Intensity must breathe.** Build, peak, release, and recover. Continuous visual
   activity destroys emphasis.
7. **A section needs one grammar.** Keep a shared palette, typography logic,
   motion character, caption behavior, material language, and spatial model.
8. **Scarcity creates power.** Poster states, fragmentation, full-frame thesis
   words, caption takeovers, and aggressive flashes are limited resources.
9. **Derive; do not copy.** Recovered examples teach relationships and methods.
   They are not a stock library of ribbons, crossroads, brains, books, or layouts.
10. **Fallbacks preserve intention.** If the ideal move is unavailable, simplify
    within the same grammar or remain clean. Never substitute an unrelated flashy
    effect.
11. **Honor cut authority.** In `POLISH_LOCKED`, add and elevate without changing
    selection, order, or editorial timing. In other modes, make structural decisions
    only inside the route contract, then freeze the accepted rough cut. Locked regions
    remain locked in every mode. Shot, beat, transcript, or file analysis never expands
    authority by itself.
12. **Show uncertainty honestly.** Separate what is visible or spoken from what the
    director is inferring.
13. **Land, be read, leave (N1/N2).** Designed text is an event, not furniture:
    default hold 5–7 seconds; persistent structures pulse with the narration item
    instead of squatting. The prototypes held one title 52 seconds and one tracker
    150 seconds; no rule caught it because none existed. Now one does.
14. **Arrive on the word, never before it (X1 hardened).** Scaffolding may precede;
    the meaning-carrying element may not. Author arrivals against word timestamps,
    not scene boundaries.
15. **Compose against the active frame (N3).** Text blocks align to the letterboxed
    region or adjacent footage module's optical center — never hung from the canvas
    top with a dead quadrant below.
16. **Open close (N4).** The first minute belongs to the audience and the footage's
    emotional register. No system chrome, no premature presentation mode. Nothing at
    all is often correct.
17. **Change is the default state of the support layer (N8).** Raise state-change
    cadence — shorter holds, pulses, per-item travel, perspective shifts — while
    scarcity classes stay rare and exactly one thing changes at a time.
18. **Travel to meaning, not empty coordinates (N10).** Plan each camera station and
    its narration-relevant visual payload together. For left/right phrase travel,
    the two sides carry two different ideas; the presenter remains the stable anchor.
19. **Name the editorial job before the treatment.** Identity, transformation, thesis,
    comparison, evidence, quote, annotation, utility, and atmosphere are different
    filmmaking jobs. They may share a section grammar without sharing font, scale,
    placement, depth, and entry behavior.
20. **Protect the necessary reading.** Names, evidence, and utility text remain fully
    readable. Environmental type may pass behind the presenter only when the intended
    phrase remains recoverable. Camera movement must preserve that contract at setup,
    arrival, midpoint, landing, and release.
21. **Color requires its own explicit authority (N11).** Source footage stays
    color-locked unless the user specifically requests correction or grading.
    “Cinematic,” “visual polish,” “complete pass,” and similar direction do not grant
    that authority. A designed palette may govern added graphics without changing the
    footage beneath them.

---

## Required inputs

### Minimum inputs before a real creative plan

- the approved route contract: assignment mode, cut authority, locked/editable scope,
  required review gate, and any unresolved authority question;
- either the exact supplied base cut or the approved raw/partial/parts source set; for
  base-edit modes, the accepted rough-cut identity before full visual polish;
- the relevant media's frame rate, duration, raster, and aspect ratio;
- a transcript, preferably with word timestamps;
- the creator's intended audience, platform, and purpose;
- the central promise or intended takeaway, if it is not clear from the cut;
- any fixed brand, legal, factual, licensing, or “do not change” constraints.

If the transcript has no word timings, the director may still make a section-level
plan, but exact arrivals must be marked unresolved. It must not invent timestamps.

### Useful inputs when available

- shot-boundary map;
- speech, music, and silence layers;
- music beat and downbeat map;
- presenter matte or confirmation that one can be produced;
- separate voice and music stems;
- source evidence, screenshots, photos, screen recordings, or data;
- existing brand tokens, fonts, colors, captions, and graphic assets;
- licence and provenance records for externally sourced material.

Analysis assets describe what exists. They do not make creative decisions. A
downbeat is an eligible landing point, not a command to add an effect. A detected
shot boundary is not automatically a story beat.

## Confidence language

Every material decision uses one of these labels:

- **High confidence:** directly supported by the spoken words, visible edit,
  supplied intent, or available evidence.
- **Medium confidence:** a strong creative reading, but another reasonable
  interpretation exists.
- **Low confidence:** depends on missing context, unavailable evidence, a future
  capability, or a taste choice the project lead should make.

For important beats, state confidence separately for:

- **meaning** — what the beat is doing in the story;
- **timing** — where the beat begins, lands, and releases;
- **execution** — whether the required inputs and accepted capability exist.

Low confidence is not permission to guess. It becomes either an unresolved review
question or a clean fallback.

---

## The directing workflow

Complete these passes in order. Do not begin with an effects shortlist.

### Pass 0 — Lock the assignment

Record:

- exact source path(s) and source identity/fingerprints;
- assignment mode and matching cut authority;
- color authority (`unchanged` by default or `explicit`) and the exact user request
  when explicit;
- locked material, editable material, and unresolved authority;
- whether the base is supplied, still awaiting its strategy/rough-cut gate, or accepted
  with a stable file/timeline identity;
- duration, frame rate, raster, and aspect ratio;
- required review gate and its current acceptance status;
- delivery platform and intended viewer;
- any protected moments, assets, wording, or brand rules;
- missing information that could materially change the direction.

If the media or intended use has not been approved, stop before making a
source-specific plan.

### Pass 1 — Watch for the film, not the graphics

First watch the accepted base cut uninterrupted. Do not design during this viewing.

Write a plain-language film reading:

- **Thesis:** What is the piece ultimately saying?
- **Story question:** What keeps the viewer watching?
- **Opening promise:** What does the beginning promise the audience?
- **Explanation:** What must become easy to understand?
- **Claims:** What statements ask the viewer to believe something?
- **Evidence:** What proves those claims?
- **Emotional turns:** Where does curiosity become pressure, surprise, relief,
  intimacy, confidence, or urgency?
- **Climax:** Which line or realization carries the most weight?
- **Conclusion:** What should remain in the viewer's mind?
- **Intended audience feeling:** What should the audience feel across the piece,
  and how should that feeling change?

Separate the reading into:

- **Observed:** directly present in speech, picture, audio, or supplied context;
- **Director inference:** the director's interpretation;
- **Unresolved:** something the source cannot answer safely.

### Pass 2 — Divide the existing cut into story beats

A beat is a change in what the audience is meant to understand, expect, or feel.
It is not automatically a sentence, caption, shot, or music beat.

Mark a new beat when at least one of these changes:

- narrative function;
- subject or question;
- claim and its evidence;
- explanation step;
- emotional direction;
- level of importance;
- audience orientation;
- section or chapter;
- tension, release, or conclusion.

Useful beat functions include:

`hook`, `orientation`, `promise`, `claim`, `proof`, `explanation`, `example`,
`comparison`, `pressure`, `turn`, `escalation`, `climax`, `reflection`, `relief`,
`resolution`, `conclusion`, and `breathing`.

For every beat, record:

- time window and exact spoken words when known;
- narrative function;
- what changed from the previous beat;
- audience feeling before and after;
- importance level;
- whether the existing picture already communicates it well.

Do not change the cut to make the beat map neater.

### Pass 3 — Draw the emotional and intensity arc

Before choosing individual treatments, describe the whole film's energy shape.

Use the rulebook intensity classes:

| Class | Director meaning |
|---|---|
| 0 — clean | performance, comprehension, intimacy, or recovery needs no added visual |
| 1 — support | quiet captions, evidence, or layout assistance |
| 2 — emphasis | an important claim, definition, keyword, or directed camera move |
| 3 — transformation | a major turn, poster state, fragmentation, or full world change |
| 4 — scarcity | the single strongest climax or final thesis treatment |

Plan the curve, not just the peaks:

- identify the first attention rise;
- identify comprehension holds;
- identify the main escalation;
- protect at least one recovery window after a dense passage;
- identify the climax;
- identify how the film releases or concludes.

Also plan contrast deliberately. Contrast can come from treated versus clean,
large versus small, motion versus stillness, full-canvas versus nested evidence,
density versus negative space, or sound versus silence. It is not only a color
choice. Repetition should create recognition through a limited motif; when the same
move no longer adds meaning or useful rhythm, it has become redundancy.

Class 4 is normally budgeted once per piece. A class 3 or 4 move requires an
explicit story or emotional reason and a planned recovery. Two high-intensity moves
may touch only when the story is deliberately sustaining one climax; state that
reason. Every section must contain some class 0 or 1 space unless the entire section
is a very short, intentionally compressed climax.

### Pass 4 — Choose one dominant visual grammar per section

Group related beats into sections. For each section, write a short design contract:

- **section purpose and intended feeling;**
- **spatial model:** clean footage, presenter-world, evidence desk, designed cards,
  tactile explainer, cinematic screen space, or another story-specific model;
- **presenter role:** full anchor, cutout anchor, framed insert, occasional presence,
  or intentionally absent;
- **typography roles:** attention, identity, editorial, annotation, utility, and
  base caption; one family may fill several roles, while a justified section may
  use distinct families;
- **palette and contrast logic;**
- **motion character:** locked, gentle drift, precise push, stepped/tactile, sharp
  punctuation, or another motivated behavior;
- **material language:** clean, paper, print, screen, archival, photographic, or
  another justified family;
- **evidence layout;**
- **recurring motif:** the limited move that creates continuity;
- **maximum intensity and scarcity budget;**
- **moves to avoid in this section.**

For a hero beat or coherent section that needs expensive generation, donor adaptation,
or custom motion design, fill the canonical
[`visual-design-contract.md`](visual-design-contract.md) before execution. Routine
captions and already-accepted mechanical treatments do not need a separate contract.
The contract owns the design handoff; this pass still owns the storytelling choice.

Alongside the grammar, choose the section's **movement vocabulary** — which of the
reference languages carries it (camera-travel study,
`../../project review notes`):

- **station travel** (N7/N10, accepted): anchor → swap-and-land-close → travel per
  narration item → return to anchor. Each destination is defined by both its phrase
  and its relevant visual payload; left/right travel cannot be planned as camera
  coordinates with empty destinations;
- **morph-and-accumulate** (source reference form): elements transform or accumulate beside
  a stable presenter while the camera holds;
- **pulse** (N2): indices and trackers appear per item, clear, and return;
- **hold:** clean footage, captions only.

This is not a request for a complete style guide. The later unified design pass owns
final font families, colors, textures, spacing, and motion curves. Here the director
chooses the storytelling grammar those designs must serve.

Change the dominant grammar only when the story changes mode — a new sentence is not
a new visual universe — **but deliberately plan where it DOES change, so the film mixes
`overlay` (presenter-world graphics over footage) and `presentation` (full-frame designed
states) instead of committing to one family for the whole video** (the project owner (2026-07-16): the
recurring failure is the editor defaulting into all-overlay *or* all-presentation — MC went
all-presentation, FP went all-overlay). Record the planned balance as `declared_mix` in
`beat-map.json` ([`beat-map-schema.md`](beat-map-schema.md)); the computable **mode-mix gate
(check #10)** fails a film that collapses into one family unless you set `single_mode` with a
story reason. Separately, one grammar per section must never collapse into one *layout* per
film: the Masterclass prototype entered all sixteen scenes with one identical reveal
animation and recycled a single bordered-frame layout — coherence is not monotony. Where the
topic allows, an effect moment should **combine** capabilities — masking + on-screen element
+ camera move + caption together (the source reference register) — and the film should default to
a **fast pace**. Plan where the section's framing/world states change; variety comes from
hierarchy and movement inside the grammar.

### Pass 5 — Decide treated versus clean

For every beat, ask these questions in order:

1. Does the audience need clearer **meaning**?
2. Does a claim need honest **proof**?
3. Does the audience need **orientation** in space, time, process, or interface?
4. Does the beat deserve stronger **emotion or importance**?
5. Does an added move create useful **rhythm** without competing with speech?
6. Does the move fit the section grammar and intensity curve?
7. Are the required inputs and capability actually available?

Treat the beat only when at least one of the first five answers is yes and the last
two answers also pass.

“It would look cool” is not sufficient. If the performance, evidence, or composition
already carries the beat, explicitly mark it **clean** and state what the clean
window protects: intimacy, trust, comprehension, tension, or recovery.

For every treated typography beat, identify the communicative job before choosing the
composition:

| Job | First obligation | Possible direction—not an automatic preset |
|---|---|---|
| identity | the complete name reads immediately | clean lockup in measured negative space or in front |
| transformation | the before/after relationship lands emotionally | oversized environmental field, world change, or progressive type |
| thesis | the argument reads in deliberate order | staged build, isolated statement, or clean full-frame state |
| comparison/evidence | facts and relationships remain exact | structured sides, receipt, diagram, or data-led type |
| quote/editorial | human voice and tone are felt | editorial serif, restrained italic, or handwritten accent |
| annotation/utility | support without stealing hierarchy | concise label, note, index, or caption-level treatment |
| atmosphere | create texture without carrying necessary facts | partially obscured or cropped type may be acceptable |

Then state `type_role`, `scale`, `depth`, `readability`, and `edge_policy` in the beat
map. Look at nearby treated beats before approving the choice. Reusing masking is
allowed; repeating substantially the same treatment, scale, depth, and type role
without a developing idea must be reconsidered. This is a director judgment, not a
prohibition on consecutive rear text.

### Pass 6 — Select an accepted move, not a fresh technical invention

Choose the lightest rulebook move that serves the beat. Name the rule ID and the
accepted skill or capability it requests.

| Creative need | Buildable rule(s) | Accepted execution path |
|---|---|---|
| integrated presenter depth, word emphasis, camera-to-meaning, card/world changes | R1–R10 | `compose-presenter-world`, `composite-alpha`, and `track-and-mask` when a matte is needed |
| claim receipts and escalating evidence | R11–R12 | ordinary timeline composition through `composite-alpha` or `compose-presenter-world` |
| before/after transformation | R13 | `render-geometric-masks` |
| overload, fragmentation, relief, or accumulation | R14–R15 | `composite-alpha`, `compose-presenter-world`, and `track-and-mask` when needed |
| brief Difference punctuation | R16 | `render-geometric-masks` |
| important-person or quote poster | R17 | `track-and-mask`, `posterize-subject`, `composite-alpha` |
| speech/music eligibility and audio clarity | R18, R20 | `segment-speech-music`, `duck-music-under-speech` |
| music-led added events | R19 | `detect-beats`; downbeats are the default eligibility layer, not an edit command |
| cinematic screen treatment | R21 | `render-geometric-masks` |

`detect-shots` may provide a first-pass shot index. It does not identify story beats
or expand the cut authority recorded by the input router.

Rules F1–F17 are future families unless the rulebook explicitly says otherwise.
F11's **creative decision** is accepted—request a contextual concept visual—but its
automatic resolver is not built yet. A future move may be described as an
aspiration, but the plan must also provide a buildable fallback and must not promise
that the future capability already exists.

Follow the reuse-first engine policy:

1. accepted capability runner first;
2. existing project skill or HyperFrames component next;
3. HyperFrames for ordinary new motion design;
4. Remotion for alpha-heavy, footage-heavy, or complex per-frame work;
5. FFmpeg for audio, deterministic media work, muxing, and assembly;
6. Video Use patterns selectively — selection/EDL/assembly only in `ASSEMBLE_RAW`,
   `COMPOSE_FROM_PARTS`, or the editable portion of `HYBRID_SCOPED`; never a
   structural recut in `POLISH_LOCKED`;
7. custom code only with a written reason.

The orchestration runbook owns route and process order. Phase 3 records the capability
request, real constraints, and fallback; it is not the future automated assembly
factory.

### Pass 7 — Brief contextual concept visuals

When a beat needs a story-specific visual, do not translate a noun automatically
into a stock icon. Describe the communication problem first.

The durable brief for a hero beat or coherent section is the
[`visual design contract`](visual-design-contract.md). The fields below supply its
story and communication inputs; they do not form a second competing schema. Resolve
the route in order: accepted project capability/material → local HyperFrames → audited
external donor → generated still → original authoring → documented custom-code last
resort. An external donor must resolve to a usable `candidate`, `benchmarked`, or
`accepted` record in `../../research/open-design-donors/donors.json`.

Each concept-visual brief must state:

- **beat and spoken idea;**
- **communicative job:** explain, prove, orient, symbolize, compare, or create mood;
- **what the viewer must understand or feel at first glance;**
- **literal facts that must remain accurate;**
- **preferred visual relationship:** literal evidence, metaphor, diagram, map,
  illustration, typography, UI, photograph, footage, or another justified form;
- **relationship to presenter and frame:** behind, in front, beside, nested, full
  canvas, or screen-space;
- **section grammar:** palette, material, type, camera angle, and motion character it
  must inherit;
- **creation route:** derive, author, generate, adapt, responsibly source, or reuse a
  licensed foundation material;
- **negative constraints:** clichés, copied reference layouts, misleading imagery,
  illegible detail, unwanted stock-icon language;
- **provenance and licence requirement;**
- **simple fallback** that preserves the same meaning.

An icon is allowed when it is genuinely the clearest visual for this story. It is
never selected merely because the transcript contains an easy noun.

When the route is **responsibly source real footage** (visual relationship = footage), there
are two peer sub-routes; both are peers of generation, never a fallback chain:

- **Generic/emotional or an establishing shot → stock** ([`source-footage`](../../skills/source-footage/SKILL.md),
  Shelf 1): describe the beat, write the query subject-first with a POV/register keyword, fetch
  free HD candidates, and **pick by looking** — never by CLIP score (a literal-content tie-break
  aid that anti-correlates with dramatic register). Source a *metaphorical* clip for any
  copyrighted subject.
- **A real, SPECIFIC thing stock can't hold → open-web mining** ([`mine-web-footage`](../../skills/mine-web-footage/SKILL.md),
  Shelf 3): a named landmark, a real event's footage, a specific place, a recognizable scene,
  likely buried inside a longer web video. **Ask the project lead one simple go/no-go question first**
  ("Want me to search YouTube for real footage of X for this beat?") and honor the session
  preference — never auto-fire (ToS + copyright are his call). Delegate the whole job to one
  mining sub-agent (only a tiny shortlist comes back); it routes with transcript, **locates with
  CLIP**, **verifies with a vision pass**, and you **pick by looking**. Two query rules: describe
  the **LOOK not the ROLE** (a "villain" query returned the *hero* on the the prototype worked example test), and
  for a specific *person* **web-search to find who they are and pass their photo as a reference
  image** (image→image search).

Choose real when the beat must look *true*, open-web when it must be real *and specific*, generate
when the concept has no real referent. Both sourcing mechanics are proven; how a clip is *placed
and treated* in the cut is still owed a taste pass.

Do not place source-specific worked examples into a permanent library. The completed
Foundation Texture Pack, shipped at `../../assets/foundation-textures-v1/`, may supply
licensed paper, fabric, ink, grain, dust, scratch, flicker, and light-leak raw
materials — applied under the judgment rules in
[`texture-language.md`](texture-language.md). Its
existence does not authorize a Phase 3 render or turn story-specific imagery into
stock-library content.

### Pass 8 — Choreograph timing and recovery

For every treated beat, direct four moments:

- **setup:** what the viewer sees immediately before the move;
- **arrival:** the word, thought turn, evidence reveal, or musical event it lands
  on — **on** it, never before it (X1 hardened); the arrival is authored against the
  word timestamp, not the scene boundary;
- **hold:** long enough to read and understand (X3), **and no longer** — default
  budget 5–7 seconds for designed text (N1); a longer hold needs a recorded reason;
  persistent structures get a pulse schedule (N2);
- **release:** how the composition returns, transitions, or creates breathing room —
  the release time is part of the beat card, not an afterthought.

Placement is part of choreography: text blocks and graphic clusters compose against
the active frame's optical center/axes (N3); corner chips carry entry/exit times
tied to their narrative job (N6); nothing continuous crosses the presenter's face
(N5).

Also state:

- the stable anchor that keeps the viewer oriented;
- layer relationship when depth matters;
- camera intention, if any; for station travel, name each destination's phrase and
  visual payload together;
- caption or typography behavior;
- audio eligibility or treatment;
- what other motion must remain quiet during the beat.

Do not invent frame-accurate timing when word timestamps or the media are missing.
Mark the arrival as unresolved and give the editor a visible cue phrase.

### Pass 9 — Write the human-reviewable creative beat plan

The output is a filmmaker-readable document, not a machine schema. It contains the
following sections in this order.

#### 1. Assignment lock

- route contract, source identity, and accepted base-cut identity;
- assignment mode, cut authority, locked/editable scope, and gate status;
- audience, platform, purpose, and constraints;
- available and missing inputs;
- exact structural boundary: what may and may not change.

#### 2. Film reading

- thesis, story question, opening promise, climax, conclusion;
- claims, evidence, explanations, and emotional turns;
- intended audience-feeling arc;
- observed facts, director inferences, and unresolved readings.

#### 3. Intensity arc

- plain-language description of build, hold, escalation, climax, recovery, and end;
- class 3 and 4 scarcity budget;
- the clean windows that protect comprehension and emotion.

#### 4. Section direction cards

For each section:

- time range and narrative job;
- intended feeling;
- dominant visual grammar;
- presenter, typography, evidence, motion, material, and audio behavior;
- recurring motif, maximum intensity, and prohibited moves;
- transition into and out of the section.

#### 5. Beat cards

Use this format for every treated beat and every important clean beat:

```text
Beat ID / time / spoken cue:
Narrative function:
Audience feeling:
Observed source evidence:
Director decision: CLEAN or TREAT
Why this decision earns its place:
Rulebook move / intensity / scarcity class:
Visual direction:
Setup -> arrival -> hold -> release:
Presenter / depth / camera / typography / evidence / audio:
Contextual asset brief, if needed:
Visual contract ID / path:
Donor registry ID, if used:
Required inputs:
Accepted capability or future dependency:
Preferred engine: auto
Real engine constraints:
Meaning / timing / execution confidence:
Fallback:
Unresolved choice for review:
```

For consecutive routine beats that share one clean or support treatment, combine
them into a clearly timed range instead of producing repetitive cards.

#### 6. Asset and evidence list

- available evidence and its proof relationship;
- contextual visuals that must be created or sourced;
- visual contracts and donor IDs for hero or section-level designed visuals;
- provenance and licensing status;
- unavailable assets and same-grammar fallbacks;
- future capabilities that are not yet promised.

#### 7. Execution request summary

- requested accepted skills by beat;
- reusable analysis assets;
- preferred engine `auto` unless a real constraint exists;
- missing dependencies;
- no custom-code request unless reuse was checked and rejected with a reason.

#### 8. Unresolved creative choices

List only decisions that could materially change the result. Give the project lead the relevant
context and the director's recommendation. Do not bury them inside beat cards.

#### 9. Self-critique and recommendation

Record what was changed during self-review, remaining risks, and whether the plan is
ready for the project lead's review. “Ready for review” is not permission to render.

---

## Self-critique gate

Before showing the plan, review it as if another editor wrote it.

The review must explicitly reject incoherence, unsupported creative decisions,
effect overload, copied reference imagery, repetitive grammar, and insufficient breathing room.

### Story and emotion

- Can every treated beat be traced to a narrative function or audience feeling?
- Does the plan preserve the accepted thesis, conclusion, and supplied factual intent?
- Did the director mistake a sentence, cut, or detected beat for a story beat?
- Are important claims paired with honest evidence rather than decorative b-roll?
- Is the strongest visual treatment actually reserved for the strongest moment?

### Coherence

- Does every section have one understandable visual grammar?
- Do palette, typography, material, motion, captions, and spatial treatment feel
  related?
- Is variety coming from hierarchy and story change rather than random styles?
- Does any move copy a reference graphic instead of deriving a new visual for the
  current story?
- Are contextual visuals specific, accurate, and free of automatic stock-icon logic?
- Does every hero beat or coherent section using expensive generation, donor
  adaptation, or custom motion design have a complete visual contract?

### Density and breathing

- Is there a reason for every class 2–4 move?
- Are class 3–4 moves followed by recovery unless one climax is intentionally
  sustained?
- Does the film contain clean performance and comprehension windows?
- Are repeated moves acting as a motif, or are they merely repetitive?
- Does any passage contain simultaneous camera, typography, background, texture,
  and accent changes that compete for attention?

### Readability and timing

- Does each important arrival land **on** the intended word — and never before it?
- Is the hold long enough to read and understand — and within its N1/N2 budget?
  List every designed text/structure with its planned on-screen duration; anything
  over 7 seconds needs its recorded reason here.
- Is every text block composed against the active frame's center axes (N3)?
- Does the opening minute stay clean and close (N4)?
- Does a rear graphic remain legible where the presenter occludes it?
- Does anything continuous cross the presenter's face (N5)? Automatic fail.
- Does every corner chip have a current narrative job with entry/exit (N6)?
- Does camera motion move toward meaning and preserve a stable anchor?
- For left/right station travel, are there two distinct narration ideas and two
  accurate visual payloads timed to them? Empty camera destinations fail N10.
- Does the release restore orientation and provide recovery?
- Count the section's distinct framing/world states: does the support layer actually
  change at the planned cadence (N8), with exactly one thing changing at a time?

### Feasibility and honesty

- Does every promised buildable move map to an accepted rule and skill?
- Are future families labelled as future rather than quietly promised?
- Are required media, mattes, timings, stems, cursor data, and assets available?
- Is every sourced asset licensed and traceable?
- Was the accepted project/local HyperFrames route checked before an external donor?
- Does every external donor ID pass the selected-donor eligibility check, with no
  prohibited source identity copied into the current story?
- Does each unavailable ideal treatment have a coherent reduced fallback?
- Is any custom work requested only because it is truly necessary?

### Scope

- Does any instruction exceed the route contract's cut authority or locked/editable
  scope?
- Does any music beat, transcript boundary, shot boundary, or file type silently expand
  authority — especially into a structural recut in `POLISH_LOCKED`?
- Has each required strategy, rough-cut, or rendered-review gate passed in the user's
  chosen surface before the next expensive stage?

Revise the plan until all blocking problems are removed. If a blocking choice belongs
to the project lead, surface it clearly instead of guessing.

## The editorial verification gate — renders never skip it

Both prototypes passed technical QC while violating rules the system already had:
one revealed its headline 6.4 seconds early while its own decoration was correctly
word-synced; the other shipped a front-layer hairline rule slicing the presenter's
face in half. Prose intent is not evidence. Before any render reaches the user,
verify **by measurement**:

1. **Word-sync:** compare every meaning-carrying arrival's fire time against the
   word onset in the transcript JSON. Earlier than the onset = fail.
2. **Holds:** measure actual on-screen durations from extracted frames (contact
   sheets at 1s resolution or finer); compare against N1/N2 budgets and the beat
   map's recorded reasons.
3. **Alignment:** frame-grab every composite layout; check text blocks against the
   active frame's center axes (N3).
4. **Presenter integrity:** crop presenter regions in every composited window at
   full resolution; no continuous element crossing a face, no seams, correct
   occlusion in both directions.
5. **Opening:** chrome scan of the first minute (N4).
6. **Chips:** every persistent corner element maps to a beat-map job with entry and
   exit times (N6).
7. **Scarcity:** count class 3–4 events and their spacing (X7); verify recovery.
8. **Sound:** ducking/carve behaves on speech regions; no pumping.
9. **Language register (N9):** every **rendered** caption/text node contains **zero
   Devanagari codepoints (U+0900–U+097F)**. Mechanical check, never eyeballed —
   scoped to rendered text so word-sync comments (`// card lands ON "क्रिटिकल"`) are
   allowed: `grep -oP '>[^<]*<' <composition.html> | grep -oP '[\x{0900}-\x{097F}]+'`
   must return nothing (for a transcript JSON, grep the whole file). Any hit → the
   Hinglish romanization ([`romanize-hinglish`](../../skills/romanize-hinglish/SKILL.md))
   was skipped or incomplete; re-run it and re-verify. This check exists because N9
   had no enforcement and a render shipped `लगता` on screen (2026-07-16); the same
   scoped check confirmed MC was clean while catching FP.
10. **Mode-mix (N10-mix, the project owner (2026-07-16)):** the film must not silently collapse into one
    visual family. Run `python3 research/mode-mix/check_mode_mix.py
    <edit>/beat-map.json` (skill [`check-mode-mix`](../../skills/check-mode-mix/SKILL.md))
    against the final plan; an all-`overlay` or all-`presentation` film **fails** unless
    `declared_mix.single_mode` is `true` with a story reason. Same script as the Stage 5
    plan check — re-run here so the *shipped* film provably matches its declared mix.
    Mechanical, never eyeballed; it exists because the editor kept defaulting into one mode
    (the early prototype all-presentation, all-overlay) — the exact complaint that motivated it.
11. **Color authority (N11, the project owner (2026-07-19)):** read the route contract before
    conform. If `color_authority` is `unchanged`, the render plan and engine source
    must contain no corrective or aesthetic source-footage color transforms: no LUT,
    grade, relight, recolor, white-balance, exposure, contrast, saturation, gamma, hue,
    or temperature adjustment. Inspect the engine graph/filter list automatically
    where it is machine-readable, then compare representative full-resolution source
    and output frames to confirm the source appearance is preserved. A documented
    delivery color-space conversion is permitted only when it is necessary for a
    faithful visual match. Any unauthorized transform or visible color shift = fail.

**Computable checks are scripts, not discretion.** The N9 leak, the 6.4s-early
headline, and the 52s hold were all *knowledge the system had* — they slipped because
the gate was prose an agent could forget to run. Any gate item that can be **computed**
from the sources (script leaks → `grep`; holds → parse `data-duration`; arrival timing
→ diff `data-start` against transcript word onsets) must be run as an automatic check
the render cannot bypass. Only the genuinely un-computable checks — matte seams,
doubling, active-frame *feel* — stay human/pixel work.

Fail → fix → re-verify. The gate's evidence (sheets, crops, measurements) is
retained beside the render. Only a render that has passed is presented — in the
user's chosen review surface (Rule zero).

## Approval and handoff

The creative beat plan is the director's proposal, and the render is its argument.
Present in the user's chosen surface (Rule zero — for the project lead: rendered video or
excerpts, never the document). User reactions are translated into the review-decision
log with strict lanes (user stated / mechanically verified / agent inference), each
delta attributed to a failure layer and class; rule changes flow to the rulebook
only as recorded amendments with provenance. Feedback fixes the director, not just
the output.

After the direction is accepted:

- the skills are chained **by hand** today (an agent runs each per `skills/CATALOG.md`,
  following the [orchestration runbook](orchestration-runbook.md)); **automating** that
  chaining (the AI-drafted Phase 4 planner / Phase 5 harness) is **deferred and
  optional** — build it only if a real speed/cost/volume need appears after the taste is
  proven (the project lead, 2026-07-16);
- later design work may finalize typography, color, texture, and motion character.

Phase 3 itself does none of those things.

## Never again (measured in the 2026-07-15 prototype review)

1. A title held 52 seconds across five unrelated shots.
2. A tracker pinned for 150 seconds, killing a design the user actually liked.
3. A headline revealed 6.4 seconds before its words while its own arrow was
   word-synced.
4. Text columns hung from the canvas top beside a centered footage window.
5. A front-layer hairline rule through the presenter's face, passing QC.
6. A film opening in presentation mode with archive chrome over an emotional low.
7. Sixteen scenes entering with one identical reveal animation.
8. A caption left in Devanagari (`लगता`) on screen — approved because the gate
   checked script register in prose only, never with a `grep`. (2026-07-16)

## Phase 3 review status

This document is a **review draft**, revised on 2026-07-15 after the prototype
review. Per Rule zero, its acceptance test is not a document review: it is validated
when the project lead accepts corrected 30–60 second excerpts produced under it
(the project review log). Until then it governs excerpt
production only, not another full film.
