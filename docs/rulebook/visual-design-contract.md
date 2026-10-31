---
title: Visual Design Contract
type: rulebook
status: experimental-until-rendered-benchmark
date: 2026-07-16
governing_spec: ../superpowers/specs/2026-07-16-visual-contract-open-design-donors-design.md
---

# Visual Design Contract

## Purpose and boundary

A visual design contract is the handoff between the creative director's story decision
and an asset generator, donor adaptation, or renderer. It records what a designed
visual must communicate, what world it belongs to, what it may borrow as a
relationship, and what the director must see before accepting it.

The contract is project-native and provider-neutral. It is not another director, a
prompt template, a style library, or a rendering engine. The director still owns why,
what, when, and how much. Existing project skills, HyperFrames, Remotion, and FFmpeg
still own execution.

One contract covers one coherent section or one hero beat. Do not stretch a contract
across unrelated story modes merely to make the film look consistent. Coherence comes
from a shared storytelling grammar; it is not permission to repeat one layout.

Contract IDs use:

```text
vc-<edit-slug>-<section-or-beat-slug>-v<integer>
```

Example: `vc-product-film-hidden-queue-v1`.

## When a contract is required

Write a contract before any of these expensive or identity-bearing choices:

- contextual image generation for a hero beat or coherent section;
- adaptation of an external design donor;
- custom motion design or a new section world;
- a new typographic hierarchy that depends on externally sourced fonts;
- a designed visual whose factual accuracy, depth relationship, or recurring grammar
  materially affects the story.

A separate contract is not required for routine captions, deterministic media work,
or an already-accepted mechanical treatment used within its proven envelope. Those
moves still inherit the section direction and pass the editorial verification gate.

If the story job or intended audience effect is unknown, stop before generation. “It
would look good” is not a valid story job.

## Route order

Resolve each visual through the lightest credible route in this order:

1. `accepted-project-route` — an accepted EditorialCut capability, skill, or licensed reusable
   material already solves the job;
2. `local-hyperframes` — an existing local HyperFrames registry component or example
   supplies the needed execution grammar;
3. `audited-donor` — an external donor provides a meaningfully different relationship
   or implementation pattern and has a non-rejected registry record;
4. `generated-still` — the story needs a contextual background, illustration,
   photograph, or cutout that does not already exist;
5. `original-authoring` — create the visual in HyperFrames or Remotion from the
   contract;
6. `custom-code-last-resort` — only after recording why the earlier routes were
   insufficient.

Novel appearance is not a reason to skip an existing route. External donors teach
relationships and methods; they do not supply a permanent shelf of source-specific
graphics.

Before sourcing paper, grain, dust, scratches, flicker, or light leaks, check
Foundation Texture Pack v1, shipped at `../../assets/foundation-textures-v1/`, and
apply it under the judgment rules in [`texture-language.md`](texture-language.md).

## The fifteen required fields

Every contract contains all fifteen fields. If a field genuinely does not apply, write
`not-used: <reason>` rather than omitting it.

1. `story_job` — the exact claim, turn, explanation, evidence, or emotion the visual
   helps land.
2. `audience_effect` — the concrete intended perception or feeling, not an empty
   adjective such as “premium.”
3. `evidence_lanes` — keep the project lead-stated taste, directly verified mechanics, and
   director inference visibly separate.
4. `keep` — qualities from the footage, section grammar, or donor that must survive.
5. `change` — content, composition, palette, motion, and proportions that must become
   specific to the current story.
6. `do_not_copy` — donor words, logos, trademarked identity, signature arrangement,
   source-specific graphics, and unlicensed assets or fonts.
7. `composition` — focal hierarchy, subject placement, negative space, depth order,
   active-frame alignment, measured safe regions, necessary reading, permitted presenter
   occlusion, and camera-edge policy.
8. `color_roles` — background, surface, primary text, secondary text, accent, and
   semantic-state colors where used.
9. `typography_roles` — attention, identity, editorial, annotation, utility, and caption
   roles where used, each with file, source, license, fallback, intended scale, and any
   intentional role sharing.
10. `material_language` — the justified surface family: clean digital, paper, print,
    fabric, archive, photographic, screen, or another explicit choice.
11. `motion_grammar` — setup, entry, emphasis, hold, exit, camera relationship, and
    motion family. It obeys the accepted perceptibility and scarcity rules.
12. `asset_route` — exactly one primary route from the route order above, plus an
    audited donor ID when applicable.
13. `negative_constraints` — visual clichés, AI failure modes, competing movement,
    misleading imagery, and unwanted props, staging, or text.
14. `technical_contract` — dimensions, alpha/background requirement, resolution floor,
    timing window, layer destination, and renderer-neutral output format.
15. `acceptance_evidence` — exact frames or timestamps to inspect and observable pass
   or fail conditions. For moving-camera text, include setup, arrival, every leg midpoint
   and landing, and release.

## Contract template

Copy this shape into the edit's working record:

```markdown
### Contract `<contract_id>`

- **Story job:**
- **Audience effect:**
- **Evidence lanes:**
  - the project lead-stated:
  - Directly verified:
  - Director inference:
- **Keep:**
- **Change:**
- **Do not copy:**
- **Composition:**
- **Color roles:**
- **Typography roles:**
- **Material language:**
- **Motion grammar:**
- **Asset route:**
- **Negative constraints:**
- **Technical contract:**
- **Acceptance evidence:**
```

The working record also names its source/beat plan, contract author, date, and status:
`draft`, `ready-to-execute`, `accepted`, `rejected`, or `superseded`.

## Filled documentation example

This is a **documentation example—not an approved benchmark**. It uses a fictional
comparison beat and no protected project media.

### Contract `vc-example-hidden-queue-v1`

- **Story job:** A presenter contrasts a visible two-second interface delay with a
  hidden queue that adds eight seconds. Make the audience understand that the larger
  problem is behind the visible surface.
- **Audience effect:** First recognition, then a mild reveal: “the obvious delay was
  not the real bottleneck.”
- **Evidence lanes:**
  - the project lead-stated: contextual visuals should depict what is being said rather than fall
    back to stock icons.
  - Directly verified: the fictional script supplies two seconds visible and eight
    seconds queued; no other quantity is asserted.
  - Director inference: spatial depth—small foreground wait, larger rear queue—will
    make the comparison legible faster than two unrelated number cards.
- **Keep:** The presenter's central authority, the comparison's exact 2s/8s values,
  one stable horizontal reading direction, and a quiet frame before the reveal.
- **Change:** Any donor wording, dataset, product identity, palette, or layout becomes
  specific to this fictional queue comparison.
- **Do not copy:** No source logo, branded interface, donor text, signature arrangement,
  or bundled font. Do not imitate an identifiable company's loading screen.
- **Composition:** Presenter remains left of optical center. A small `VISIBLE 2s` plate
  occupies the right foreground. At the reveal, it separates to expose four queued
  blocks receding behind it with a single `HIDDEN 8s` label. Nothing crosses the face.
- **Color roles:** warm off-white background; near-black primary text; muted gray queue
  blocks; one rust accent only on the hidden total; no semantic red/green state.
- **Typography roles:** utility/label uses the project's existing system sans;
  attention uses the same family at a heavier weight; narrative/editorial is
  `not-used: the beat is a functional comparison`; external font is
  `not-used: no external font required`.
- **Material language:** clean diagram with a light paper grain from Foundation Texture
  Pack v1 at low opacity; no additional distressed texture.
- **Motion grammar:** hold clean through 0.00–1.20s; foreground plate arrives at 1.20s;
  queue separates in one depth move from 3.20–3.65s; values hold through 6.20s; all
  diagram elements release by 6.70s. Camera stays quiet during the depth reveal.
- **Asset route:** `original-authoring`; use an existing local diagram/layout component
  if one fits after registry inspection. No external donor is selected.
- **Negative constraints:** no spinning loader, clock icon, dashboard-card grid,
  purple-blue glow, rounded-container pile, fake UI chrome, AI-generated text, or
  simultaneous camera push.
- **Technical contract:** 1920×1080 composition; transparent diagram layers; labels
  authored in the renderer; relative window 0.00–7.00s; foreground/right-safe region;
  standard PNG/SVG assets or native renderer shapes.
- **Acceptance evidence:** inspect 1.30s for a legible foreground `2s`, 3.70s for clear
  front/behind separation and unobstructed presenter, 5.50s for simultaneous readable
  `2s`/`8s`, and 6.90s for a clean release. Fail if the hidden queue is not visibly
  larger, any number changes, the presenter is crossed, or template identity remains.

## Director acceptance checklist

Before any expensive execution:

- Can the story job be traced to the beat and spoken idea?
- Is the audience effect concrete enough to recognize in a rendered frame?
- Are stated taste, verified evidence, and inference still separate?
- Does the route order prove that project assets and local HyperFrames were checked?
- If a donor is named, does its registry status allow use and does the contract state
  what is prohibited from copying?
- Do composition and depth reflect the actual active frame rather than a generic
  canvas?
- Is every necessary word either fully readable or explicitly contracted as recoverable,
  and does that remain true throughout camera motion?
- Are color, type, material, and motion roles coherent but not monotonous?
- Is the visual factually honest and free of automatic noun-to-icon translation?
- Are negative constraints specific to likely failure modes?
- Can the technical contract be handed to a different renderer without losing intent?
- Do acceptance checkpoints reveal both correctness and likely visual failure?

After execution, the director personally inspects every specified checkpoint and the
motion between them. Generator or worker prose is not acceptance evidence.

## Provider-prompt derivation

Derive a provider prompt from the durable contract in this order:

1. state the story-specific subject and communicative job;
2. state the composition, viewpoint, focal hierarchy, and background/alpha need;
3. state the color roles and justified material language;
4. state literal facts that must remain accurate;
5. state negative constraints, including unwanted staging, props, logos, and text;
6. state dimensions and resolution requirements;
7. omit motion, depth timing, and renderer-authored typography that belong to the
   composition stage.

Generate one asset per brief. Prefer renderer-authored text because image models can
garble characters. If generated text is unavoidable, verify it character by character.
Provider identity is recorded as provenance, never promoted into design knowledge.

## Provenance and font rules

An accepted generated asset records:

```text
provider=<provider>; date=<YYYY-MM-DD>; contract_id=<id>; donor_id=<id-or-none>; sha256=<64-hex>; brief=<full brief>
```

Generated files remain per-edit disposables under `assets-generated/`. They graduate
to the project `assets/` directory only after the project lead accepts them as reusable production
materials and a manifest, license note, preview, and checksum exist.

Open Design's hashed font binaries are not project assets. A font may enter a contract
only after it is re-sourced from the canonical foundry or open-font repository and the
exact file, version, license, fallback, checksum, and role are recorded. A repository's
root license does not silently settle a third-party font or media asset's nested
license.

Text briefs are the default for external image providers. Sending unpublished footage
frames requires the project lead's explicit permission for that asset.

## Failure and fallback behavior

- Missing `story_job` or `audience_effect`: stop; do not decorate the beat.
- Missing or rejected donor record: use the nearest same-grammar project/local route or
  leave the beat clean.
- Uncertain font or nested-asset license: keep it reference-only and replace it with a
  canonically sourced, licensed asset before use.
- Donor identity overwhelms the current story: strip the identity-bearing qualities or
  reject the donor.
- First generated result fails: write the observed failure against the contract and
  re-brief once.
- Second generated result fails: change route. Do not accumulate prompt patches.
- Composition cannot meet the depth or safe-region contract: simplify within the same
  grammar or remain clean.
- Contract grows unwieldy: retain all fifteen fields and use `not-used: <reason>` for
  irrelevant roles; do not create an undocumented short form.

Fallbacks preserve the intended audience effect. An unrelated flashy treatment is not
a fallback.

## Benchmark status

This workflow is experimental until the project lead reviews rendered evidence. The first
benchmark will compare one confirmed 8–12-second contextual-visual job using:

- A: the existing brief without a visual contract;
- B: a contract-derived brief with no external donor;
- C: the same contract plus one story-compatible audited donor.

Footage, timing, audio, provider, generation count, and composition mechanics remain
constant. the project lead must confirm the exact excerpt and intended visual job before media is
cut or generated. Until the clips are reviewed, this document is an implemented
workflow proposal—not an accepted visual capability.
