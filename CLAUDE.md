# EditorialCut working contract

`AGENTS.md` is the single source of truth for this contract. `CLAUDE.md`, `GEMINI.md`,
and `.github/copilot-instructions.md` are generated copies — never edit them by hand.
Edit `AGENTS.md`, then run `scripts/gen-contract.sh` to regenerate the copies; a drift
check in `scripts/check_public_tree.py` fails the build if any copy diverges.

**Every coding agent that opens this repo to work on video is bound by this contract**,
whichever CLI you are (Claude Code, Codex, Gemini, Antigravity, Copilot, OpenCode, …).
Treat it as directive, not advisory.

## Front door — start every job here

- **Editing a video** (polish, assemble, compose, or scoped changes): read
  `docs/rulebook/edit-brief-template.md` and execute it as your brief. In Claude Code
  this is the `/edit-video` command; on any other CLI, open that file and follow it. Its
  Step 0 loads the lean spine — `skills/CATALOG.md` and
  `docs/rulebook/orchestration-runbook.md` — and pulls the heavier judgment docs only at
  the stage that needs them.
- **Generating a contextual still** (background, illustration, cutout, missing texture):
  read `skills/generate-image/SKILL.md` and derive the brief from
  `docs/rulebook/visual-design-contract.md`. In Claude Code this is the
  `/generate-assets` command.
- **Any assignment:** first classify authority with `docs/rulebook/input-routing.md`.
  Read-only inventory and analysis may proceed while authority is unresolved; selection,
  reordering, retiming, replacement, or newly authored editorial timing may not.

## Directive routing table — reuse the skill, never hand-roll

The skills in `skills/CATALOG.md` already implement the mechanical jobs below, each
verified against real pixels. **If you are about to do the left column, STOP and invoke
the skill on the right instead.** Hand-rolling a job a catalogued skill covers — or
placing text/graphics on blind fixed pixel coordinates with no face/mask measurement
(violates rule N5) — is an **automatic failure, even if the output looks fine.**

| About to… | Invoke instead |
|---|---|
| `cv2.putText` / `PIL ImageDraw.*text` / `ffmpeg drawtext`, or place text/graphics inside a presenter's scene | `compose-presenter-world` — measure the face/mask first; never blind coordinates |
| composite an alpha matte, or layer graphics behind/in front of a subject | `composite-alpha` |
| isolate, track, or mask a presenter | `track-and-mask` |
| detect cuts or shot boundaries | `detect-shots` |
| find beats, downbeats, or tempo | `detect-beats` |
| separate speech vs music, or duck music under dialogue | `segment-speech-music`, `duck-music-under-speech` |
| render difference flashes, reveals, before/after sliders, geometric masks | `render-geometric-masks` |
| a duotone / poster subject treatment | `posterize-subject` |
| turn Devanagari speech into on-screen captions | `romanize-hinglish` — zero Devanagari, rule N9 |
| fetch real / stock b-roll for a beat | `source-footage` |
| locate a real, specific shot buried in a long web video | `mine-web-footage` |
| generate a still, background, or cutout | `generate-image` |
| confirm a plan did not collapse into one visual family | `check-mode-mix` |
| classify cut + color authority at the start of a job | `route-assignment` |
| confirm a render before calling it done | `verify-render` |

Not listed here? Consult `skills/CATALOG.md` before writing any renderer or analysis
command. Custom code is the last resort — only after accepted runners, HyperFrames,
Remotion, and FFmpeg are all insufficient, with a written justification in `project.md`.

## Route from authority, never from file type

Record the route contract (`docs/rulebook/input-routing.md`) before any structural
mutation. **User intent plus explicit authority outranks file type** — a folder of raw
clips does not grant recut permission; a flattened MP4 does not mean its structure is
locked.

| Mode | Cut authority | May do |
|---|---|---|
| `POLISH_LOCKED` | `locked` | preserve the supplied selection/order/timing; add polish only |
| `ASSEMBLE_RAW` | `assemble` | select, shorten, order, and assemble inside the approved target |
| `COMPOSE_FROM_PARTS` | `compose` | build story structure and a base timeline from supplied parts |
| `HYBRID_SCOPED` | `scoped` | change only named editable sections; preserve locked material |

**`color_authority` is separate and defaults to `unchanged` on every route.** No route
grants color correction or grading by implication. "Cinematic," "make it pop," "visual
polish," and similar style language do **not** authorize changing source-footage color.
Set `color_authority: explicit` only when the user names color correction, grading,
white balance, exposure, contrast, saturation, gamma, hue, temperature, or a LUT.
Otherwise every engine must omit footage color transforms.

## The standing rules

- Route from user intent and explicit authority, never file type alone.
- Treat source footage as immutable. Work in a separate project directory.
- Source-footage color is locked unless the user explicitly authorizes color work.
- Reuse an accepted skill before writing a new renderer or procedure.
- Keep judgment with one director; delegate only bounded mechanical work.
- Verify rendered pixels and audio, not a worker's prose report.
- Capability knowledge is a derivation recipe, never a stock library of examples.
- Never commit media, secrets, model weights, render outputs, or third-party engines.
- Follow each external engine's own license. Do not copy it into this repository.

## Verification gate — before you call any render done

Run the editorial verification gate in `docs/rulebook/orchestration-runbook.md`
(Stage 7) and `docs/rulebook/creative-director-instructions.md`. Verify the **actual
rendered pixels and audio**, not a worker's prose claim: word-sync, holds, presenter
integrity (no seams, no doubling), no text crossing the face, check #9 (zero Devanagari
in rendered text), check #10 (mode-mix — re-run `research/mode-mix/check_mode_mix.py` on
the final `beat-map.json`), and check #11 (color authority). Computable checks cannot be
skipped, and a failed automatic-fail check means fix and re-render, not a footnote.

When a capability is uncertain, run a short representative test, record limits honestly,
and ask for human review before scaling it to a full film.
