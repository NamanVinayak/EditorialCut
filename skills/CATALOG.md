# Skill Catalog — what exists, where its code is, how to run it

The front-door index of every accepted skill, so the agent **uses what's already
built instead of re-deriving or hand-writing it.** Read this before doing any editing
step. Each skill is a `SKILL.md` (the procedure) plus, for the mechanical ones, real
runnable code in `research/<capability>/` (each with its own `.venv`). Exact
invocation flags live in the skill's own `SKILL.md`.

**Tiers** (see the [orchestration runbook](../docs/rulebook/orchestration-runbook.md)):
- **[MECHANICAL]** — deterministic tool; run its script, get the answer. Automatable; often *more* reliable than doing it by hand.
- **[TOOL+JUDGMENT]** — the tool runs, but *whether/how* to use it on this shot is an LLM decision.
- **[JUDGMENT]** — the SKILL.md guides the LLM through reasoning; code is only scaffolding/render.
- **[SUB-AGENT]** — delegated to a small-model sub-agent + a deterministic check.

| Skill | Tier | What it does | SKILL.md | Runnable code |
|---|---|---|---|---|
| detect-shots | MECHANICAL | Cut / shot-boundary detection over a video | `skills/detect-shots/SKILL.md` | `research/shot-detection/src/shotbench/` (`cli.py`; own `.venv`) |
| detect-beats | MECHANICAL | Beat + downbeat + tempo map of a music track | `skills/detect-beats/SKILL.md` | `research/audio-intelligence/detect_beats.py` (`.venv`) |
| segment-speech-music | MECHANICAL | Speech / music / silence layers (Demucs + silero-VAD) | `skills/segment-speech-music/SKILL.md` | `research/audio-intelligence/seg_label.py` (`.venv-seg`) |
| duck-music-under-speech | MECHANICAL | Dialogue-aware ducking + frequency carve | `skills/duck-music-under-speech/SKILL.md` | `research/audio-intelligence/make_ducking.py`, `verify_ducking.py` |
| composite-alpha | MECHANICAL | Layer an alpha matte over a background plate (contract-checked) | `skills/composite-alpha/SKILL.md` | `research/alpha-compositing/` (`verify.py` + Remotion) |
| posterize-subject | MECHANICAL | Inner-luminance subject treatment | `skills/posterize-subject/SKILL.md` | `research/luminance-mask/process.py` (`.venv`) |
| track-and-mask | TOOL+JUDGMENT | Presenter matte (RVM default). Tool runs; per-shot suitability/settings are a judgment call | `skills/track-and-mask/SKILL.md` | `research/masking/src/maskbench/` (`cli.py`), backend `backends/rvm/run.py` |
| render-geometric-masks | JUDGMENT | Geometric masks at concept level | `skills/render-geometric-masks/SKILL.md` | `research/geometric-masks/` (`verify.py`) |
| compose-presenter-world | JUDGMENT | In-scene graphics behind/in front of the subject, text-on-word, camera travel (station + continuous). Method + per-video composition | `skills/compose-presenter-world/SKILL.md` | **Whole-video generic kit: `research/presenter-world-kit/`** (data-driven Remotion: `look.json` + `beat-map.json` payloads + `captions.json` → `FullVideo`; renderers clean/overlay_accent/pulse_list/station_compare/card). Original proof: `research/presenter-world/`. Look is DERIVED per video via `docs/rulebook/look-derivation-recipe.md` |
| romanize-hinglish | SUB-AGENT | Hindi Devanagari ASR → modern Hinglish captions; enforced by a zero-Devanagari `grep` | `skills/romanize-hinglish/SKILL.md` | LLM sub-agent + `grep` backstop (no standalone script) |
| generate-image | TOOL+JUDGMENT | Contract-guided contextual stills (backgrounds, illustrations, cutouts); checks project/HyperFrames/donor routes before generation, then director pixel-verifies | `skills/generate-image/SKILL.md` | External CLIs: `codex exec` (default) / `agy -p`; invoker `.claude/commands/generate-assets.md` consumes `docs/rulebook/visual-design-contract.md` and verifies `research/open-design-donors/donors.json` |
| check-mode-mix | MECHANICAL | Mode-mix gate (check #10): fails a plan that collapses into one visual family (all-overlay / all-presentation) unless single-mode is declared with a reason | `skills/check-mode-mix/SKILL.md` | `research/mode-mix/check_mode_mix.py` (pure stdlib, no venv); reads `beat-map.json` per `docs/rulebook/beat-map-schema.md` |
| source-footage | TOOL+JUDGMENT | Fetch real/stock b-roll for a beat from free libraries (Pexels proven); optional CLIP re-rank as an aid. Finds candidates only — pick + real-vs-generate are judgment, never an auto CLIP-score pick | `skills/source-footage/SKILL.md` | `research/footage-sourcing/` (`source_clips.py`, `rank_clips.py`, `make_contact_sheet.py`; in-house Pexels adapter `pexels.py`/`base.py` + CLIP embedder `clip_embedder.py`; own `.venv`, `transformers<5`) |
| mine-web-footage | SUB-AGENT | Locate a REAL, SPECIFIC visual buried inside long web/YouTube videos: search → 480p proxy download → CLIP-locate exact seconds → vision-verify → tiny shortlist → HD-conform only the chosen seconds. Describe the LOOK not the ROLE; specific people use a web-found reference image (image→image). Finds candidates only — pick + real-vs-generate are judgment | `skills/mine-web-footage/SKILL.md` | `research/web-footage-mining/` (`mine.py`, `mine_multi.py`, `conform.py`; reuses vendored `clip_embedder`; own `.venv`, `transformers<5`) |

Design contracts are judgment-layer documents, not a separate skill. Use
`docs/rulebook/visual-design-contract.md`; external donor records and their verifier
live under `research/open-design-donors/`.

## Front-door commands

Two entrypoint commands wrap the docs so any CLI has a single "start here". They are thin
pointers — all logic lives in the file each names, so they never drift:

- **`/edit-video`** (`.claude/commands/edit-video.md`) → read
  [`docs/rulebook/edit-brief-template.md`](../docs/rulebook/edit-brief-template.md) and
  execute it. The front door for any edit.
- **`/generate-assets`** (`.claude/commands/generate-assets.md`) → run the
  [`generate-image`](generate-image/SKILL.md) node from
  [`docs/rulebook/visual-design-contract.md`](../docs/rulebook/visual-design-contract.md),
  verifying `research/open-design-donors/donors.json` (a runtime file) via
  [its verifier](../research/open-design-donors/verify_donors.py).

Codex/Antigravity/other CLIs read the same front door from `AGENTS.md` (mandatory first
step) and open the named file directly.

## Operational routers (not runnable skills)

- [`docs/rulebook/input-routing.md`](../docs/rulebook/input-routing.md) classifies the
  assignment mode and cut authority, gates authorized base-edit creation, and hands an
  accepted/frozen base cut to the catalogued skills. It does not render, select an
  engine, or replace the director.

## Governance skills (thin wrappers exposed for description-matching)

Two skills wrap the routers/gates above so a description-match pages them in even when the
working contract is trimmed. They add no new capability — they point at the canonical docs:

- [`route-assignment`](route-assignment/SKILL.md) — wraps `input-routing.md`: classify cut
  + color authority at the start of any assignment, before any structural edit.
- [`verify-render`](verify-render/SKILL.md) — wraps the Stage-7 gate + `check-mode-mix`:
  verify actual pixels and audio before declaring any render done.

## How to use this catalog

1. **Before a mechanical step, check here first.** If a skill covers it (transcript-adjacent audio, shots, beats, masking, compositing, captions), run *its* code — do not re-derive an `ffmpeg`/analysis command or hand-write a composition that already exists.
2. **Match the tier to who does the work** (runbook delegation policy): MECHANICAL/SUB-AGENT → delegate/run directly, keep the director's context clear; JUDGMENT → the director does it.
3. **Not listed here?** Transcription is a fixed tool call (`mlx_whisper` Large V3, word timestamps — see `CLAUDE.md` → Extraction tooling), and frame-extraction / contact sheets are plain `ffmpeg`. Those are commands, not skills.
4. **Provenance / acceptance** of each capability lives in its `docs/capabilities/*.md` page; taste rules live in `docs/rulebook/beat-to-primitive-rules.md`; the order to run things in is the [orchestration runbook](../docs/rulebook/orchestration-runbook.md).

Keep this table in sync when a skill is added, its code moves, or a capability is accepted.
