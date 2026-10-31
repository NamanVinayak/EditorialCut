# Getting started

## 0. Fetch the engines

EditorialCut's rules and skills live in this repo, but the third-party engines they
call out to (Remotion, HyperFrames, video-use, RVM, and the Python
research/ dependencies) are not vendored here. After cloning:

```
./scripts/setup.sh
```

One command fetches the working system: it clones HyperFrames, video-use, and
RobustVideoMatting into a git-ignored `engines/` directory,
downloads and checksum-verifies the RVM masking checkpoint into `models/`,
installs each Remotion composition's npm dependencies, and builds a Python
virtualenv at `.venv` carrying `requirements.txt` plus the pipeline CLIs
(demucs, yt-dlp, beat_this, and mlx-whisper on Apple Silicon). What remains
manual is deliberately short — API keys, and the two masking backends that
need isolated environments — and is printed at the end of the run.

## 1. Bring a project

Create a separate working directory for each video. Keep source footage immutable and
write transcripts, masks, renders, and review artifacts beneath that working directory.
Do not place media inside the EditorialCut repository.

## 2. Choose cut authority

Read `docs/rulebook/input-routing.md` and declare one route:

- `POLISH_LOCKED`: timing and structure are fixed.
- `ASSEMBLE_RAW`: an editor may create the base cut from raw footage.
- `COMPOSE_FROM_PARTS`: an editor may build the base edit from supplied parts.
- `HYBRID_SCOPED`: only explicitly named ranges may change structurally.

Also declare `color_authority: unchanged | explicit`. The default is `unchanged`.

## 3. Connect your tools

Use the engines you already trust. EditorialCut describes portable contracts for timing,
alpha, masks, audio stems, assets, and rendered clips; it does not require a particular
renderer. Install third-party engines separately and follow their licenses.

Only set provider keys in your shell or an ignored local `.env` file. Never put a real
key in a plan, prompt, manifest, or commit.

## 4. Run the editorial loop

1. Inventory the inputs without changing them.
2. Get the route and base edit accepted.
3. Build a beat map and visual plan.
4. Use `skills/CATALOG.md` to select proven mechanics.
5. Render a short representative excerpt first.
6. Review moving video, revise, and run the verification gate.
7. Render and verify the final deliverable.

The runbook is the process spine; the creative-director instructions and beat rules are
the judgment layer. They belong on one director's desk, not in competing agents.

