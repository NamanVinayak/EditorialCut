# Open Design donor audit and benchmark protocol

## Purpose

This folder turns the useful parts of Open Design into an auditable reference layer for
EditorialCut. It does not install Open Design, create a runtime dependency, or turn worked
examples into a stock library.

The useful abstraction is:

```text
external reference
  -> immutable evidence and license state
  -> portable relationship or implementation pattern
  -> explicit do-not-copy boundary
  -> local overlap check
  -> one narrow rendered benchmark
  -> accept or reject for that editing job
```

## Immutable audit snapshot

- Repository: <https://github.com/nexu-io/open-design>
- Audited commit: `3a6221a54b84bdc29d7f1bfe9b9da71c0935a229`
- Audit date: 2026-07-16
- Root license: Apache-2.0
- Local registry: `donors.json`
- Deterministic verifier: `verify_donors.py`

All paths in `donors.json` refer to that immutable upstream commit. Later upstream
changes do not silently change the project record.

## What was actually found

The audited tree contains 151 design-system directories and 23 packaged video
templates (22 `frame-*` directories plus `vfx-text-cursor`). The design systems are
primarily instructions, tokens, and examples; there are no current asset or font files
under their per-system `assets/` or `fonts/` paths.

The executable video layer is more relevant, but much of it is HTML/CSS/GSAP, several
examples are direct forks already present in the local HyperFrames registry, and the
catalog's prose counts drift from the tree. One native Remotion donor,
`frame-data-rollup`, is structurally interesting but has data-honesty problems that
prevent direct promotion.

The template folders include many hashed font binaries but no colocated per-font
license records in those font directories. Template-specific screenshots, logos,
sound effects, music, and images also require file-level provenance rather than trust
in the root repository license.

## Why this is a donor registry, not an asset import

EditorialCut stores derivation knowledge: how to produce a fitting visual for unseen footage.
It does not store source-specific poster layouts, product screenshots, example text,
or disposable graphics as permanent answers.

Every donor record therefore says:

- what relationship or implementation idea is portable;
- what identity-bearing material must not be copied;
- whether an accepted project route already covers the job;
- what adaptation is required;
- whether license and nested provenance are complete;
- whether the donor is reference-only, a candidate, benchmarked, accepted, or rejected.

## Initial decisions

| Donor | Current decision | Reason |
|---|---|---|
| `reference-design-contract` | candidate | Its keep/change/do-not-copy and evidence-handoff method has been adapted into EditorialCut's fifteen-field visual contract; rendered value remains unproven. |
| `frame-data-rollup` | reference-only | Useful native Remotion architecture, but scale switching is unlabeled, zero is visually inflated, and negative values are unsupported. |
| `frame-bold-poster` | reference-only | Potential editorial hierarchy donor; no compatible story beat has been selected. |
| `frame-creative-voltage` | reference-only | Potential split-field/kinetic relationship; no compatible story beat has been selected. |
| `frame-light-leak-cinema` | reference-only | Local HyperFrames and Foundation Texture Pack routes already cover the likely job. |
| `direct-hyperframes-forks` | rejected | All eight direct forks already exist locally; import would duplicate and possibly stale the preferred route. |
| `bundled-template-fonts` | rejected | Direct binary copying fails the project's exact per-font provenance requirement. |
| `template-assets-audio` | reference-only | No nested media asset is eligible without its own provenance and license audit. |

## Local overlap evidence

The verifier requires every declared partial or duplicate overlap path to exist. The
current overlaps are:

- local `data-chart` for part of the DataRollup job;
- local `light-leak` plus Foundation Texture Pack v1 for the cinema-title material;
- eight local HyperFrames examples matching the eight direct forks;
- the existing creative-director instructions as the partial local reasoning layer
  improved by the visual contract.

An existing path proves local availability, not creative equivalence. The director
still reads both routes before making a judgment.

## First benchmark question

**Does a visual contract produce a more story-specific and coherent contextual visual
than the existing brief alone, and does one audited donor add value beyond the
contract?**

This is one editing job. It does not simultaneously test camera templates, data
visualization, a font pack, a new renderer, or a third autonomous full-film edit.

## Required user gate

the project lead must confirm the **exact 8–12-second excerpt** and the intended contextual-visual
job before any benchmark media is cut or any image is generated.

The confirmation records:

- exact immutable source path and excerpt timestamps;
- the line/beat being treated;
- what the viewer should understand or feel;
- whether unpublished frames may be sent to an external image provider (default: no);
- the output raster, frame rate, and intended review surface.

Familiarity with an existing source is not approval to use it.

## A/B/C treatments

- **A — baseline:** the existing F11/`generate-image` brief without a visual contract.
- **B — contract-only:** a brief derived from the canonical visual contract, with no
  external donor.
- **C — contract-plus-one-donor:** the same visual contract plus one audited donor
  chosen because its relationship fits the story job.

The donor in C must be `candidate`, `benchmarked`, or `accepted`; a `reference-only`
donor must be promoted to `candidate` with a recorded reason before the render. A
`rejected` donor cannot be used.

## Held-constant variables

To isolate the value of the contract and donor, all three treatments use the same:

- source footage and exact time range;
- output duration, raster, frame rate, and audio;
- image provider and model route;
- number of generated candidates and allowed re-brief count;
- generation resolution and reference-image permission state;
- composition mechanics, camera behavior, depth treatment, and renderer;
- caption and audio treatment.

Only the brief construction changes from A to B. Only the compatible donor grammar
changes from B to C.

## Review package

Deliver:

1. three directly playable clips;
2. one contact sheet showing the same checkpoint times for A/B/C;
3. one manifest recording source identity, prompts, contract ID, optional donor ID,
   provider, versions, generation attempts, accepted-asset hashes, timing, and media
   measurements.

No custom review site is justified for three candidates. the project lead reviews each clip as
`keep`, `kill`, or `change-what`.

## Acceptance and rejection logic

The director first verifies factual accuracy, legibility, source preservation,
provenance, timing, and contract compliance. the project lead then judges the intended feeling
and whether the visual belongs to the footage.

- **B beats A and C does not beat B:** adopt the contract; reject the donor for that
  job.
- **C beats B:** retain the donor as `benchmarked` for that narrow editing job; do not
  generalize beyond the evidence.
- **Neither B nor C improves A:** record the failed hypothesis and create no capability
  or skill.
- **A is strongest:** keep the existing brief workflow for that job and inspect whether
  the contract was over-specified before testing it elsewhere.

No result becomes an accepted capability merely because its files render or its
manifest passes.

## Font and nested-asset policy

Open Design's hashed font files are never copied. A useful family name is only a
discovery lead. Re-source any selected font from the canonical foundry or open-font
repository and record exact file, version, license, fallback, checksum, role, and
intended size.

The same rule applies to template images and audio. Template-level attribution does
not establish the provenance of each nested screenshot, logo, sound effect, music
bed, or source image. Each file needs an independent audit before use.

## How to verify this folder

From the project root:

```bash
python3 -m unittest discover \
  -s research/open-design-donors \
  -p 'test_*.py' -v

python3 research/open-design-donors/verify_donors.py \
  research/open-design-donors/donors.json \
  --workspace .

python3 research/open-design-donors/verify_donors.py \
  research/open-design-donors/donors.json \
  --workspace . \
  --donor-id reference-design-contract \
  --require-usable
```

The verifier checks schema completeness, immutable commit shape, allowed states,
unique IDs, nonempty evidence and limitation records, workspace-safe local paths, and
the existence of every claimed local overlap. With `--donor-id <id>
--require-usable`, it also fails missing, `reference-only`, and `rejected` selections.
It does not judge visual quality.

## Current status

The visual contract and donor registry are implemented as an experimental workflow.
No Open Design source tree, template, font binary, image, or audio file has been
vendored into EditorialCut. No donor has rendered benchmark evidence yet.

Next gate: the project lead confirms one exact 8–12-second excerpt and contextual-visual job;
only then produce A/B/C review clips with the variables above held constant.
