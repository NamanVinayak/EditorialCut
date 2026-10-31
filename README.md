# EditorialCut

**AI tools don't have taste. EditorialCut is a filmmaker's — encoded, and sitting behind whatever renderer you already use.**

[What it is](#what-it-is) · [How it works](#how-it-works) · [Quickstart](#quickstart) · [The 14 skills](#the-14-skills) · [The rulebook](#the-rulebook-judgment-you-can-read) · [Receipts](#receipts-tested-limits-not-promises) · [License](#licensing)

<!-- LAUNCH VIDEO SLOT — embed the reveal video here the day it goes live,
as a clickable thumbnail image linking to the YouTube video, captioned:
"Every treatment you just watched — the cuts, the type, the ducking — was
planned and placed by this repo. That video is the demo." -->

## What it is

Rendering engines like Remotion, HyperFrames, and FFmpeg know how to draw a frame — they don't know what belongs in it. EditorialCut is the layer in between: it reads your material — raw footage or a rough cut — classifies the assignment, maps the narrative beats, sources and assembles the footage each beat needs, and picks the visual primitives — typography behind the presenter, camera travel, beat-synced accents, music ducking under dialogue — the same calls a working editor makes, before handing the mechanical work to the engine you already run (Remotion, HyperFrames, video-use, FFmpeg). It ships 14 field-tested skills, a written rulebook instead of a black box, and hard gates for human review wherever taste — not correctness — is the deciding factor.

**What it is NOT:** not a renderer, not a one-click generator, and not a replacement for your judgment. It plans like an editor and stops where a director should look.

## How it works

1. **Route the assignment** — declare cut authority (`POLISH_LOCKED`, `ASSEMBLE_RAW`, `COMPOSE_FROM_PARTS`, `HYBRID_SCOPED`) so the system knows what it may and may not touch.
2. **Map the beats** — the rough cut becomes a beat map: what the audience must feel, where, and why.
3. **Plan the treatment** — beats get primitives under the rulebook's laws: scarcity, one grammar per section, motivate movement through narration, know when clean is stronger.
4. **Render through your engines** — each job routes to the tool already best at it.
5. **Review where taste matters** — excerpt first, moving pixels verified, director signs off before the full render.

## Works behind the engines you already use

| Engine | Role | How it arrives |
|---|---|---|
| [Remotion](https://www.remotion.dev) | footage & compositing specialist (alpha layers, presenter depth) | npm, per composition |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | motion-design default (type, cards, canvases) | cloned by setup |
| [FFmpeg](https://ffmpeg.org) | native media operations, audio, final assembly | you install |
| [video-use](https://github.com/browser-use/video-use) | real-footage cutting & assembly orchestration | cloned by setup |
| [RVM](https://github.com/PeterL1n/RobustVideoMatting) | subject masking (checkpoint checksum-verified) | cloned + downloaded by setup |

Outputs use portable contracts — timing JSON, alpha media, audio stems, rendered clips — so any engine can be swapped later.

## Quickstart

```bash
git clone https://github.com/NamanVinayak/EditorialCut.git
cd EditorialCut && ./scripts/setup.sh
```

One command fetches the engines, the RVM checkpoint, seven npm projects, and a Python env with the pipeline CLIs (demucs, yt-dlp, beat_this, mlx-whisper on Apple Silicon). Then paste this into your coding agent:

```
Read skills/CATALOG.md, docs/rulebook/input-routing.md, and
docs/rulebook/orchestration-runbook.md. My rough cut is at <path>.
Route the assignment (POLISH_LOCKED unless I say otherwise), build the
beat map, and propose a visual plan for my review before rendering anything.
```

## The 14 skills

Every skill declares its tier — who does the work, and where an LLM is allowed to decide:

| Skill | Tier | What it does |
|---|---|---|
| detect-shots | MECHANICAL | cut/shot-boundary detection |
| detect-beats | MECHANICAL | beat + downbeat + tempo map |
| segment-speech-music | MECHANICAL | speech/music/silence layers |
| duck-music-under-speech | MECHANICAL | dialogue-aware ducking + frequency carve |
| composite-alpha | MECHANICAL | contract-checked alpha compositing |
| posterize-subject | MECHANICAL | inner-luminance subject treatment |
| check-mode-mix | MECHANICAL | fails plans that collapse into one visual family |
| track-and-mask | TOOL+JUDGMENT | presenter matting; per-shot suitability is a call |
| generate-image | TOOL+JUDGMENT | contract-guided contextual stills |
| source-footage | TOOL+JUDGMENT | licensed b-roll candidates; the pick stays human |
| render-geometric-masks | JUDGMENT | geometric masks at concept level |
| compose-presenter-world | JUDGMENT | graphics behind/around the presenter, camera travel |
| romanize-hinglish | SUB-AGENT | Devanagari ASR → Hinglish captions, grep-enforced |
| mine-web-footage | SUB-AGENT | locate a specific visual buried in long web video |

Full invocations and acceptance criteria: [`skills/CATALOG.md`](skills/CATALOG.md).

Alongside these 14 capability skills, two thin **governance** skills — `route-assignment`
and `verify-render` — wrap the assignment router and the verification gate so an agent
pages them in by description-match even if the working contract is trimmed. They add no
new capability; they point at the canonical rulebook docs.

## The rulebook: judgment you can read

The creative decisions live in markdown, not in a model's latent space — derived from a 24-video taste study and accepted rule by rule: [routing](docs/rulebook/input-routing.md), [creative direction](docs/rulebook/creative-director-instructions.md), [beat-to-primitive rules](docs/rulebook/beat-to-primitive-rules.md), [texture language](docs/rulebook/texture-language.md), [the locked-look contract](docs/rulebook/locked-look-contract.md). Disagree with a rule? It's a diff, not a fine-tune.

## Receipts, tested limits, not promises

Every capability in [`docs/capabilities/`](docs/capabilities/) records what was actually verified — including where it breaks. The research code that produced those results ships in [`research/`](research/), runnable. If a technique isn't proven against real pixels, the docs say so.

## What you bring

Your footage and the rights to use it · your model/provider keys · a rough cut (or explicit authority to assemble one) · a human willing to look at the frames that matter.

EditorialCut does not bundle footage, renderer repositories, model weights, secrets, or the private reference library its rules were derived from.

## Licensing

All original EditorialCut material is **MIT OR AGPL-3.0-only**, at your option — the whole repo, no per-file carve-outs. See [`LICENSE`](LICENSE) and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
