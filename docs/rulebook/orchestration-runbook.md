---
title: Orchestration Runbook — the process spine ("the plumber")
type: process
status: draft-v1
updated: 2026-07-19
---

# Orchestration Runbook

The **process spine** an editing agent reads *before touching a video*. It sequences
the work, names the mechanical tool for each mechanical step, marks where the agent
must stop and use its own judgment, and enforces the checks. It is provider-neutral —
any CLI (Claude Code, Codex, Antigravity) reads this same file and follows it.

## What this is, and what it is emphatically NOT

- **It controls process, never taste.** It says *what order* and *which tool*, never
  *which creative choice*. The creative choices live in the agent's own judgment at the
  stages marked **[JUDGMENT]**, guided (not dictated) by the rulebook
  ([`beat-to-primitive-rules.md`](beat-to-primitive-rules.md)) and the
  [`creative-director-instructions.md`](creative-director-instructions.md).
- **One director, one model, all the information.** There is a single director agent
  on the user's chosen model. This runbook, the rulebook, and the director instructions
  are *reference papers on that one director's desk* — not separate agents, not separate
  system prompts, not a second brain.
- **It is a document, not a program.** Writing and reading it is cheap. It is **not**
  the automated planner/assembly factory (pipeline design Phases 4–5); it is the thin
  structure that guides even a fully manually directed edit. Its first real use is the
  manually directed short test — an LLM follows this spine while doing the judgment live.

## Two kinds of work — the tag on every stage

Every stage below is tagged, and the tag is the whole point:

- **[MECHANICAL]** — scripted, identical every video, safe to delegate, must pass a
  check. The runbook says exactly how.
- **[JUDGMENT]** — the director's own creative read. The runbook only supplies the
  inputs and the shape of the output; it stays silent on the actual choices.

## Delegation & model policy (two independent axes — do not weld them)

1. **Delegate?** — a question about **context (desk space).** Offload boring work to a
   sub-agent so the director's context stays free for creative thinking. Delegating does
   **not** imply a weaker model.
2. **Downgrade the model?** — a *separate* question about **task difficulty.** Sub-agents
   keep the **user's chosen model by default.** Drop to a smaller/cheaper model **only**
   for a job that is *certainly* trivial. Today that is exactly one job: **Hindi→Hinglish
   romanization** ([`romanize-hinglish`](../../skills/romanize-hinglish/SKILL.md)).
   Anything with reasoning, complex steps, or creative thinking is **never** downgraded,
   even when delegated.
3. **Third bucket — pure deterministic commands** (ffmpeg tiling, a `grep`) are **not an
   LLM job at all.** Just run the command (or a minimal worker). No thinking model, big or
   small.
4. **Head-session only (never delegated):** interpretation, relevance/taste judgment, and
   composition/motion/geometry authoring — delegation failed twice on the last (empty
   layers, doubled presenter).

## The stages

### 0. Read, route, and lock authority — [MECHANICAL]
The runbook spine and `skills/CATALOG.md` are already loaded (edit-brief Step 0). Now load
only the [`input-routing.md`](input-routing.md) assignment router, to route and lock
authority. Do **not** re-load the rulebook or the director instructions here — they load
at the judgment stages that use them (2–5) and before the gate; re-reading them at Stage 0
was a redundant ~123 KB per run. Confirm the user's review surface (Rule zero — for the project lead:
rendered video / excerpts, never a written plan) and their captioning language needs (N9:
Hindi speech → Hinglish, never Devanagari).

Read the user's requested outcome before inferring anything from filenames. Record the
router's compact route contract with exactly one mode and its matching authority:

- `POLISH_LOCKED` / `locked`;
- `ASSEMBLE_RAW` / `assemble`;
- `COMPOSE_FROM_PARTS` / `compose`; or
- `HYBRID_SCOPED` / `scoped`.

User intent plus explicit authority wins over file type. Read-only inventory may
continue while `unresolved_authority` contains an exact question; selection,
shortening, reordering, replacement, and newly authored editorial timing may not.
Record color authority separately: it defaults to `unchanged` on every route and may
become `explicit` only when the user specifically requests color work. Style language
such as “cinematic” or “visual polish” does not grant grading permission.

### 1. Extract the route's raw facts — [MECHANICAL] (delegate; keep full model except where noted)
Analyze the supplied base cut or the raw/partial/parts source set named by the route
contract. Run applicable jobs in parallel; each produces a reusable analysis asset.

**Per-source analysis cache — compute once, reuse across runs.** The objective facts below
are deterministic measurements of the immutable source; reusing them carries no creative
choice, so they persist in a cross-run cache at `workbench/analysis-cache/<source-sha256>/`
(e.g. `transcript.json`, `beats.json`, `speech-music.json`, `mask/`). Each artifact has a
sidecar `.meta` stamp recording `{source_sha256, tool, tool_version_or_model, date}`.
Before deriving any cacheable fact, check the cache and reuse **only** when the source
SHA-256 **and** the tool/model version both match the stamp. On any miss, version mismatch,
missing/unreadable/partial stamp, or doubt, **recompute and rewrite the stamp** — the
fail-safe is always "recompute," never "reuse something unverified." This cache holds
objective facts only; every creative artifact (beat map, briefs, contracts, compositions,
renders) stays in the clean room and is never reused across runs (edit-brief Step 1).

- **Transcript** — local `mlx_whisper` Large V3, word timestamps on (`frame = round(word.start × fps)`). Delegate; full model / not-a-model (it's a command). **Cacheable.**
- **Hinglish captions** — if the speech is Hindi, hand the Devanagari transcript to the `romanize-hinglish` sub-agent. **This is the one job that may use a small/cheap model.** Not cached (register-doc-sensitive; cheap to re-run on the cached transcript).
- **Shot / scene structure** — `detect-shots` skill. **Cacheable.**
- **Audio** — `detect-beats`, `segment-speech-music` skills. **Cacheable.**
- **Contact sheets** — extract frames and tile them (a *command*, not a thinking model) so the director later reviews a handful of images, not hundreds.
- **Presenter mask** — `track-and-mask`, but **on demand only** (see stage 5); do not mask every video up front. **Cacheable** (keyed by source SHA + RVM model version).

For base-edit routes, preserve source fingerprints and timecode provenance. Reuse
Video Use's selects/EDL, word-boundary, short padding/fade, and rendered boundary-review
patterns where useful, but do **not** adopt its transcription default: the project
standard remains local MLX Whisper Large V3 with the existing ASR quality-control
evidence. Analysis assets survive route convergence; do not rerun them merely because
a rough cut has been accepted.

### 1a. Establish and accept the base cut — [JUDGMENT] strategy → [MECHANICAL] assembly/gates

- **`POLISH_LOCKED`:** identify the supplied edit as the base cut and record its
  file/timeline identity. Preserve selection, order, and editorial timing unless the
  user expands authority.
- **`ASSEMBLE_RAW`:** the director defines the story/select strategy, then creates a
  source-mapped selects/EDL and rough cut inside the approved target.
- **`COMPOSE_FROM_PARTS`:** the director defines the story/asset structure, then creates
  the base timeline from the approved script, voice-over, stills, recordings, data, or
  mixed material.
- **`HYBRID_SCOPED`:** record a locked/editable scope map, preserve every locked region,
  and build only inside the named editable sections or sources.

For the three base-edit modes, obtain strategy approval **before structural cutting**.
The concise strategy covers intended story, likely structure, selection rule,
protected material, target duration/platform, and important uncertainty. A direct user
instruction that already supplies these choices may satisfy the gate when recorded in
the route contract. Present any unresolved choice in the user's chosen review surface.

`COMPOSE_FROM_PARTS` has one narrow early image-generation exception: after strategy
approval, a visual contract may request only the structural stills required to make the
rough cut meaningfully reviewable when placeholders are inadequate. The generator
still does not choose the story, cut, timing, typography, depth, or motion, and the
asset must be pixel-checked and re-checked against the later frozen timing.

Render the base edit and obtain rough-cut acceptance before full visual polish. Record:

- the rough-cut file and SHA-256, or a stable timeline/version identity;
- source manifest and fingerprints;
- selects/EDL or structure record;
- assignment mode, cut authority, and locked/editable scope;
- known issues intentionally deferred to polish; and
- acceptance status and date.

This accepted identity is the downstream base cut. A later structural change reopens
this gate and produces a new identity. Every mode reaches stage 2 with a supplied or
newly accepted base cut; from there, the existing polish workflow is shared.

### 2. Understand the story — [JUDGMENT]
The director watches the accepted base cut and reads the transcript/contact sheets
itself:
thesis, narrative + emotional beats, evidence, explanations, turns, climax, breathing
spaces. No script — just: use these inputs, write your read.

### 3. Classify the frame(s) — [JUDGMENT] (vision), bounded by [MECHANICAL] (mask)
Classify shot type and composition by a **vision read of the whole frame** (wide /
medium / MCU / close-up; where the empty space is; the vibe) — not from a silhouette
outline. When precise geometry is needed, the **mask** supplies it (occlusion,
anti-doubling, and the zoom ceiling as a *formula of the measured subject size*, not a
fixed number). Vision judges; the mask bounds. Mechanics:
`skills/compose-presenter-world` step 4.

### 4. Direct — author the beat map — [JUDGMENT]
Per beat, decide: what deserves treatment vs stays clean; **the spatial mode
(`clean` / `overlay` / `presentation`) — and deliberately plan the MIX across the video,
not one family for the whole film** (the project owner (2026-07-16)); the camera move and *why*
(semantic OR rhythmic motivation — N7; accepted atoms T1–T4 only); which grammar fits the
speech rhythm (back-to-back ideas → continuous glide; idea-gap-idea → go, return to anchor,
go again); intensity and scarcity class; what context-specific element should exist (F11 —
derive/author/generate/adapt/source, never a keyword→icon lookup); typography, captions,
audio treatment. **Default toward a fast pace and, where the topic allows, combine
capabilities inside an effect moment — masking + on-screen element + camera move + caption
together (the source reference register) — rather than a lone treatment.**

For every designed typography beat, name its communicative job before choosing a
composition, then persist `type_role`, `scale`, `depth`, `readability`, and
`edge_policy`. Names/evidence/utility require a full read; rear environmental type may
be recoverable; atmosphere alone may be decorative. Compare the proposed treatment with
nearby beats so a shared grammar does not collapse into one repeated layout.

Emit the structured **`beat-map.json`** per [`beat-map-schema.md`](beat-map-schema.md),
including the top-level **`declared_mix`** (the planned overlay/presentation balance the
Stage 5 mode-mix gate holds you to). One family for the whole video is allowed only when
you set `declared_mix.single_mode = true` with a story reason. The runbook fixes the
*format*; the director fills the *content*.

### 4a. Contract and resolve designed visuals — [JUDGMENT] contract → [MECHANICAL] lookup
For every hero beat or coherent section that needs expensive generation, donor
adaptation, or custom motion design, fill the canonical
[`visual-design-contract.md`](visual-design-contract.md). Then resolve the route in
order: accepted project capability/material → local HyperFrames → audited donor →
generated still → original authoring → documented custom-code last resort. External
donors must resolve to a usable `candidate`, `benchmarked`, or `accepted` record in
`../../research/open-design-donors/donors.json`. The verifier checks the
exact selected ID with `--donor-id <id> --require-usable`; the director still decides
whether the mechanically eligible donor belongs in the story.

### 5. Check the plan — [MECHANICAL]
Validate `beat-map.json` before spending a render. **Run the computable mode-mix gate
(check #10) now, while fixing it is free:**
`python3 research/mode-mix/check_mode_mix.py <edit>/beat-map.json` (skill
[`check-mode-mix`](../../skills/check-mode-mix/SKILL.md)) — a non-zero exit means the plan
collapsed into one visual family without declaring it; fix and re-run. Also validate:
overlapping treatments, holds past the N1/N2 budget, excessive density, repeated scarcity
effects, missing inputs, choices that contradict the section's grammar, missing required
visual contracts, and donor IDs that are missing or `rejected`. Fail → back to stages 4/4a.

For an edit using the generic presenter-world kit, also run:

```bash
cd research/presenter-world-kit
node scripts/check-edit-data.mjs <edit>/beat-map.json <edit>/captions.json
```

This preflight mechanically rejects malformed treatment intent, semantic-readability
contradictions, Devanagari, impossible word spans, and invalid caption chronology. Its
local repetition finding is a warning for director review, not a ban.

### 5a. Acquire contextual assets — generate or source — [JUDGMENT] brief → [TOOL] generate/source → [JUDGMENT] accept
For every beat whose plan calls for a derived visual (F11 route "generate"): the
director derives the asset brief from its visual contract, delegates generation to an
installed image-capable CLI per
[`skills/generate-image/SKILL.md`](../../skills/generate-image/SKILL.md)
(Codex default for literal/flat assets, Antigravity for a photographic look), then
**looks at every returned image** and accepts or re-briefs. Text briefs only by
default — sending the project lead's footage frames to an external CLI needs his per-asset OK.
Accepted files land in the edit's `assets-generated/` with a provenance line
(provider, full brief, date, contract ID, optional donor ID, output SHA-256). Invoker:
the `/generate-assets` command. Approved by the project lead
2026-07-16 (delta HD-D/HD-E). Stills only for now; motion comes from animating them
in stage 6, not from image-to-video models (a possible future technique). This is the
default post-base-cut image node in [`input-routing.md`](input-routing.md); its only
earlier use is the contracted `COMPOSE_FROM_PARTS` structural-still exception in stage
1a. Image generation supplies a still asset — never the story, cut, timing, typography,
depth decision, or motion.

For every beat whose plan calls for a real-world visual the presenter footage can't show —
an establishing shot, a human situation, a concrete object (F11 route "source"): acquire
genuine motion footage via [`skills/source-footage/SKILL.md`](../../skills/source-footage/SKILL.md)
(Shelf 1) instead of generating. Real footage and generation are **peer** choices per beat —
pick real when the beat must look *true*, generate when the concept has no real referent —
never a source-first fallback chain. Write the query subject-first with a POV/register keyword,
fetch free HD candidates, and **look at the frames and pick**; the CLIP re-rank is a tie-break
aid on literal content only, and its score must never auto-pick or auto-decide source-vs-generate
(it anti-correlates with dramatic register). For a copyrighted subject, source a metaphorical clip,
never the protected work. **Status:** the sourcing mechanic is proven
([`docs/capabilities/footage-sourcing.md`](../capabilities/footage-sourcing.md)); how a clip is
*placed and treated* in the cut is still owed a taste pass, so keep placement provisional until
the project lead accepts it in a real edit. (Image-to-video motion for a sourced or generated still — Shelf 2 — is **built and
cost-guarded but unfired**: `research/image-to-video/` can animate an approved
still via fal.ai, verified against live docs, but no real render has run and it is not yet
wired in as an available route. Until one paid clip proves motion quality, motion still
comes from animating stills in stage 6.)

When the "source" beat wants a **real, specific** thing that stock can't hold and generation can't
reproduce — a named landmark, a real event's footage, a specific place, a recognizable scene, and
it likely lives as a few seconds buried inside a longer web video — use the **open-web sub-route**
(Shelf 3), [`skills/mine-web-footage/SKILL.md`](../../skills/mine-web-footage/SKILL.md), instead of
stock. It is **delegated to one mining sub-agent** so the downloaded videos, thousands of frames,
and CLIP scores never touch the director's context — only a tiny shortlist crosses back. First
**ask the project lead one simple go/no-go question** ("Want me to search YouTube for real footage of X for
this beat?") and honor the session preference — never auto-fire (downloading is against YouTube ToS
and short-excerpt reuse is a copyright gray area; the rights call is his). The sub-agent routes with
transcript/metadata (which videos), **locates with CLIP** (which seconds), and **verifies with a
vision pass** (the right specific thing, not a lookalike). Two query rules decide quality: describe
the **LOOK, never the ROLE** (a "menacing villain" text query returned the *hero* on the the prototype worked example
test — CLIP matches the most prominent face, not a character label), and for a specific *person*
**web-search to find who they are and pass their photo as a reference image** (image→image search).
The director picks by looking; **HD conform pulls only the chosen seconds** at stage 6
(`conform.py --download-sections`). Stock (Shelf 1) and open-web (Shelf 3) are peer sub-routes of
the same "source" arm, both peers of generate — never a fallback chain. **Status:** the mining
mechanic is proven on two real cases
([`docs/capabilities/web-footage-mining.md`](../capabilities/web-footage-mining.md)); placement/
treatment is the same pending taste layer as Shelf 1.

### 5b. Lock the look — [JUDGMENT] freeze
Before dispatching any parallel render, write and **freeze** the whole-video
[`locked-look.md`](locked-look-contract.md): declared mix, pace, palette, typography,
material, motion character, camera vocabulary, capability register, engine routing, and the
proxy spec. This is the single shared style every parallel worker obeys — freezing it here
is what keeps parallel work from drifting into inconsistent slop. A later change to the lock
must be re-issued to every worker.

### 5c. Preview the effect moments — cheap, in parallel — [MECHANICAL dispatch → JUDGMENT review]
Render only the `is_effect_moment` beats, as **low-resolution proxies**, in **parallel
workers** — never the whole film, never the clean footage. Each worker (see
[`locked-look-contract.md`](locked-look-contract.md) → "The contract workers receive") gets
the frozen lock, its beat spec(s), and read access to the cached analysis facts, and returns
a proxy clip plus the exact command it ran. **Workers execute only — they never choose mode,
style, or timing** (delegation-failed-twice rule: taste stays with the one director).

The director assembles the returned proxies and shows the user **only the treated moments**
(Rule zero: rendered clips, never a written plan). Each proxy includes short clean handles
before and after the treatment. After the individual moments, assemble one continuous reel
per section so cumulative rhythm, repeated typography, and neighboring effects can be
judged in playback. The user approves, or asks for changes (swap an element, change a
color, retime) on specific moments — those single proxies re-render cheaply. Loop until
the treated moments are approved. This replaces "render the whole 5-minute film, then hear
it's bad" with "approve the moments that matter, cheaply, before the expensive render."

### 6. Conform — the single high-resolution build — [MECHANICAL]
Only after the effect moments are approved (5c): render the whole timeline **once**, at full
resolution — the "conform." For each beat, route to the proven skill-runner
(`compose-presenter-world`, `composite-alpha`, camera travel, captions,
`duck-music-under-speech`), reusing the approved proxy decisions — nothing creative is
reopened here. Pull the mask **on demand**, only where a move crosses the subject or risks a
leak/double. Reuse-first engine order: accepted runner → HyperFrames → Remotion
(alpha/heavy) → FFmpeg (audio/assembly). Custom code is last resort. The director owns the
seams and continuity between the parallel-built scenes. Render one timeline; mux source
audio.

Enforce the route's color authority during conform. With
`color_authority: unchanged`, do not add LUTs, grading layers, color-correction nodes,
or filters that modify white balance, exposure, contrast, saturation, gamma, hue, or
temperature. Any color-space conversion must be solely for faithful source
preservation, be recorded, and pass a source-match inspection. New graphic elements
may have their own palette; the footage beneath them remains color-locked.

### 7. The editorial verification gate — [MECHANICAL]
Run the full gate from
[`creative-director-instructions.md`](creative-director-instructions.md) — word-sync,
holds, active-frame alignment, presenter integrity (seams/doubling), opening chrome,
chips, scarcity, sound, **check #9: zero Devanagari in rendered text**, and **check #10:
mode-mix**, plus **check #11: color authority** — re-run `check_mode_mix.py` against the final `beat-map.json` so the shipped
film provably matches its declared overlay/presentation mix. Computable checks (#9, #10,
word-sync, holds, and the render-plan portion of #11) run automatically and cannot be skipped; only the un-computable ones
(seams, doubling, active-frame *feel*) are human/pixel work. Fail → fix → re-verify.

For every semantic typography treatment, inspect setup, arrival, every camera-leg midpoint
and landing, and release. Verify both contracts independently: the presenter may obscure
only what the beat declared recoverable, and the camera viewport may crop only what the
beat declared intentional. A clean matte seam or leak-free plate does not prove the words
are readable. During silent transcript gaps, verify that the caption band clears after the
last word's end rather than persisting until the next onset.

### 8. Present — [MECHANICAL]
Show the render in the user's chosen surface only after the gate passes. Reactions feed
the review-decision log (stated / verified / inference lanes) and, as recorded amendments,
the rulebook. Feedback fixes the director, not just the output.

## Status

Draft. This spine's first exercise is the manually directed short test (one director, one
model, doing the judgment live while following these stages). The automated planner
(Phase 4) and assembly harness (Phase 5) are a later, separate build and are not
authorized by this document — do not treat writing this runbook as a mandate to build
them.
