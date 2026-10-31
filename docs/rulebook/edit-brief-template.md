# Edit brief template — full-system video edit

This is the canonical brief for editing any video through this project's system. Slash
commands (`/edit-video` in Claude Code and Codex) expand to "read this file and execute
it." Edit only this file; the commands are thin pointers and must stay that way.

**Inputs** (from the invoking user message): the source video path, and optionally
the project lead's notes on what he wants for this video. If the source path is missing or
ambiguous, ask before doing anything. If notes are absent, proceed with director
judgment from the footage.

---

You are the creative director and editor for one video. This is a run of this project's
editing **system** — its runbook, rulebook, and skills. The system is mandatory tooling.
A beautiful edit that bypasses the system is a failure; working through the system is
the point.

## Step 0 — lean orientation (before any media work)

Load only the small spine now; pull the heavy judgment/taste docs at the stage that
actually needs them. This is CLAUDE.md's conserve-usage / progressive-disclosure rule
applied to the edit path: reading all six docs up front cost ~192 KB of context on
*every* run — ~19 KB of it (`CLAUDE.md`) already auto-loaded — for no benefit, and Stage 0
then re-read ~123 KB of it a second time.

Read now — the spine only (~18 KB):

1. `skills/CATALOG.md` — every accepted skill, where its runnable code lives, how to invoke it
2. `docs/rulebook/orchestration-runbook.md` — your process spine; execute its stages in order

Already in context — do **not** re-read: `CLAUDE.md` is auto-loaded as project
instructions; re-reading it is pure waste.

Load later, at the stage that needs it (never all up front):

- `docs/rulebook/input-routing.md` — at Stage 0, to route and lock authority.
- `docs/rulebook/beat-to-primitive-rules.md` — at the judgment stages (2–5). Still
  mandatory to consult — just at point of use, and prefer the relevant rules over the
  whole 64 KB file.
- `docs/rulebook/creative-director-instructions.md` — at the judgment stages and before
  the editorial verification gate.
- the project review log — on demand only: the transcription-QC/tooling-gotcha section when you
  reach that tool, or the current-state section if resuming prior work. Never the whole
  55 KB history up front.

In your first status update, confirm the spine you read, name the docs you will load
later and when, and list the runbook stages you will execute. Do not start extraction
before that confirmation.

## Step 1 — clean-room discovery (automatic)

Check whether this source has been edited in this project before: search the project review log,
`research/`, and `workspace/footage/edit/` for prior edits, beat maps,
captions, graphics, compositions, or renders derived from this source file.

- List every prior-edit artifact you found in your `project.md` under "Clean-room
  exclusions", and do **not** open, view, copy, or take inspiration from any of them.
  Prior creative decisions for this video must not influence yours.
- Folders named `_quarantine*` (and any path your Read tool reports as
  permission-denied) are hard-blocked prior edits: record the folder name in the
  exclusion list and move on — do not try to open them via shell commands or any
  other route.
- **Re-derive every creative decision fresh** — beat map, mode/grammar choices, camera
  choreography, asset briefs, design contracts, compositions. Never reuse a prior run's
  *reasoning*; that is the entire point of the clean room. If the system changed and you
  are re-testing a benchmark, the new run must invent all of these from zero.
- **Objective analysis facts may be reused from the per-source analysis cache** —
  transcript, beats, presenter masks, speech/music segments. These are deterministic
  measurements of the immutable footage and carry no creative choice, so reusing them
  cannot leak a previous agent's taste. Reuse **only** on a fully verified cache hit
  (source SHA-256 **and** tool/model version both match the stamp). On any miss, version
  mismatch, missing/unreadable stamp, or doubt, **recompute** — never reuse a fact you
  cannot fully verify. See the runbook Stage 1 cache convention.
- **The clean-room applies only to prior outputs for this specific video.** The
  rulebook, director instructions, runbook, skills, capability pages, foundation
  texture pack, and engines are the required toolchain, never "previous work to avoid."

## Assignment

- Source: the video path given at invocation — never modify it.
- Source-footage color: locked by default. Record `color_authority: unchanged` unless
  the project lead specifically requests color work; broad style language does not count.
- Job (default, unless the project lead's notes say otherwise): a full polish pass in the
  project's first-end-to-end-target sense — **add and elevate, do not re-cut**:
  word-synced Hinglish captions, presenter-world graphics (behind/in front via mattes),
  motivated camera movement, beat-synced accents, texture treatments, dialogue-aware
  audio mixing.
- Working directory: create `workspace/footage/edit/<slug>-<YYYYMMDD>/` with a
  `project.md`, and keep transcripts/analysis/renders/verify subfolders per the
  runbook. Final render in `renders/`.

## Non-negotiable technical rules

1. **Transcription**: local MLX Whisper **Large V3 full model** (path in `CLAUDE.md`),
   JSON with word timestamps. Never `whisper-large-v3-turbo`, never whisper.cpp. If ASR
   is unreliable in a range, apply the documented QC/retry gotchas (the project review log →
   transcription section) — do not hand-write replacement captions.
2. **Captions**: on-screen Hindi is always romanized Hinglish via
   `skills/romanize-hinglish/SKILL.md`, word-synced. Gate check #9 (zero Devanagari
   codepoints in rendered text) must pass.
3. **Masking/occlusion**: any graphic that can intersect the presenter goes through the
   accepted matte path — `skills/track-and-mask` (RVM) with `skills/composite-alpha` /
   `skills/compose-presenter-world`. Rule N5: nothing continuous crosses the
   presenter's face — **automatic fail**. Static cards pasted at fixed pixel positions
   with no subject-geometry awareness are forbidden.
4. **Engines — reuse-first policy**: HyperFrames is the default for motion-design
   graphics; Remotion for alpha/video-heavy per-frame compositing; FFmpeg for audio,
   deterministic media ops, muxing, final assembly. Custom render code is last resort
   and requires a written justification in `project.md` of why every existing route was
   insufficient.
5. **Camera movement**: follow N7/N8 — motivated by speech rhythm or semantics,
   mask-bounded geometry, smooth easing, no rotation; hold a static frame where
   movement is unmotivated.
6. **Audio**: dialogue-aware ducking per `skills/duck-music-under-speech` if any music
   bed is added; never degrade the source speech.
7. **Plan + mode-mix**: emit `beat-map.json` ([`beat-map-schema.md`](beat-map-schema.md))
   with a top-level `declared_mix`, and deliberately mix `overlay` (presenter-world graphics
   over footage) and `presentation` (full-frame designed states) across the video — default
   a fast pace and, where the topic allows, combine capabilities in an effect moment
   (masking + on-screen element + camera move + caption, the source reference register). The
   computable **mode-mix gate (check #10)** runs at Stage 5 and Stage 7; a collapse into one
   family is an automatic fail unless `declared_mix.single_mode` is `true` with a story
   reason.
8. **Preview before conform**: freeze the [`locked-look`](locked-look-contract.md), render
   the treated moments as cheap **parallel proxies** for approval (Stage 5c), then do the
   single high-resolution **conform** (Stage 6). Parallel workers execute the frozen look
   only — mode, style, and timing are already decided; taste stays with the director.
9. **Color authority**: source-footage color is locked unless the project lead specifically asks
   for correction, grading, relighting, recoloring, a LUT, or a named color adjustment.
   “Cinematic,” “visual polish,” “complete pass,” “cohesive look,” and “make it pop”
   never authorize a grade. With `color_authority: unchanged`, every engine must omit
   footage color transforms. A documented color-space conversion is allowed only to
   preserve source appearance across delivery. Added graphics may retain their own
   designed palette without altering the footage.

## Verification gate — blocking, with evidence

Before declaring the render done, run the complete editorial verification gate from
`creative-director-instructions.md` and write `verify/gate-report.md`: every check
listed, pass/fail, each with evidence — full-resolution frame crops for occlusion and
face-crossing checks, the Devanagari scan output (check #9), the mode-mix check output
(check #10 — `check_mode_mix.py` against the final `beat-map.json`), timing/hold
measurements, and the color-authority evidence (check #11: route value, engine
graph/filter inspection, and representative full-resolution source/output frame
comparison). A failed automatic-fail check means fix and re-render, not a footnote. ffprobe output and a
source-SHA check are integrity facts, not verification.

## Final report

End with: runbook stages executed; skills invoked with exact commands; engine choices
and any custom-code justification; gate-report summary; path to the final render. Do
not claim success without the gate report existing and passing.

## Protections

Never modify source media or the source file. Keep
separately installed rendering engines untouched. No git
operations, no system-wide installs. New files only under your working directory and
standard skill output locations.
