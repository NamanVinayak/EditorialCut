---
name: generate-image
description: Invoke to produce a contextual still asset (topical background, illustration, isolated cutout, missing texture) by delegating to an image-capable CLI — do NOT hand-draw pixels or write compositing/drawing code. Derive the brief from the visual design contract, verify the returned pixels against acceptance evidence, and re-brief once before changing route. Stills only; motion comes from animating them downstream.
---

# generate-image — contextual AI image assets via CLI delegation

**Tier: TOOL+JUDGMENT.** The generation tool is an *external CLI agent with a real
image model* (the project lead's paid Codex / Antigravity subscriptions); the brief, the
accept/re-brief decision, and every pixel check are the director's judgment. Approved
by the project lead 2026-07-16 (delta HD-D, `docs/rulebook/review notes`).

## What it makes

Per-beat contextual stills the rulebook's F11 route calls for: topical backgrounds,
images depicting what's being said, cutout elements for presenter-world placement
(source reference register), and one-off textures the foundation pack lacks. Stills only —
image-to-motion is a future technique (the project lead, 2026-07-16); motion comes from animating
these stills in HyperFrames/Remotion per the reuse-first policy.

## Provider selection (measured 2026-07-16, aged-paper probe)

- **Codex — the default, especially for flat/literal assets.** GPT-Image behind
  `codex exec`. Output is prompt-faithful, flat, texture/asset-friendly. the project lead also
  rates ChatGPT's generator ahead of Antigravity's.
- **Antigravity — the photographic look.** Editorializes (adds staging, shallow DOF
  that wasn't asked for). Choose it when a styled photograph *is* the asset; expect to
  re-brief against unwanted staging.
- Same brief through both = two candidate looks; cheap way to give the director a
  choice on a hero asset.

## Recipes

**If you ARE Codex or Antigravity** (this file is read by every CLI via the
CLAUDE.md/AGENTS.md/GEMINI.md symlink): use your native image tool directly; skip the
shelling.

**From Claude Code — Codex:**

```bash
codex exec --skip-git-repo-check -C <workdir> -s workspace-write \
  "Generate one AI image with your image-generation tool. <BRIEF>. Save it as <name>.png in the current working directory and print the absolute path. Do not write code to draw an image."
```

**From Claude Code — Antigravity:**

```bash
agy -p "Generate one AI image using ONLY your built-in image-generation tool. Do NOT run shell commands and do NOT write code. <BRIEF>. Let the tool save the file natively, then print its absolute path."
# then copy the printed path (lives under ~/.gemini/antigravity-cli/brain/<id>/) into the workdir
```

Gotchas: `agy --dangerously-skip-permissions` is blocked by Claude Code's classifier
and `--mode accept-edits` cannot approve agy's internal "command" permission headlessly
— the no-shell recipe above is the reliable one. Codex costs ~44k tokens of the Codex
subscription per image; batch briefs thoughtfully.

## Writing the brief from the visual contract (the whole game)

Every hero or section-level generated asset requires a `contract_id` and a path to the
canonical [`visual design contract`](../../docs/rulebook/visual-design-contract.md).
The provider prompt is a derived output; the durable design knowledge stays in the
contract.

Build one asset per brief in this order:

1. extract the story job and intended audience effect;
2. state the composition/angle and focal hierarchy (flat/top-down for overlay assets);
3. state the background or alpha need (**"isolated on a plain solid white background"**
   for keyed cutout elements);
4. state color roles and the justified material language;
5. state literal facts that must remain accurate;
6. state the contract's negative constraints: staging, props, logos, text, or other
   likely failure modes;
7. state dimensions and the ≥1.2× final-box resolution floor;
8. omit motion/depth timing and renderer-authored typography that belong to
   HyperFrames/Remotion.

If a donor is used, record its registry ID and run the registry verifier with
`--donor-id <id> --require-usable`. This mechanically rejects missing,
`reference-only`, and `rejected` records. Prefer adding words in the renderer; when
generated text is unavoidable, verify it character by character.

Pixel-check the output against the contract's `acceptance_evidence`. Re-brief once
using the observed failure. If the second attempt fails, change route rather than
accumulating prompt patches.

## Cutout path (elements that sit in the presenter world)

1. Brief for a plain solid background (or ask Codex for a transparent-background PNG —
   verify the alpha actually exists before trusting it).
2. If keying is needed, key the solid background out deterministically (ffmpeg
   colorkey / PIL threshold) — this is a command, not an LLM job.
3. Placement, depth (behind/in front via the presenter matte), and timing belong to
   `compose-presenter-world` / the renderer — not to this skill.

## Hard rules

- **The director looks at every generated image before it enters a composition.**
  Verify: on-brief, on-register, no AI text garbling, no unwanted staging, resolution
  ≥ 1.2× its final on-screen box, background actually plain if a cutout is intended.
  Verify pixels, not the generator's own description.
- **Text briefs only, by default.** Sending frames of the project lead's footage to an external
  CLI as reference images uploads his unpublished material — only with his explicit OK,
  per asset.
- **Provenance line per accepted asset** in the edit's project log, in this exact
  format:
  `provider=<provider>; date=<YYYY-MM-DD>; contract_id=<id>; donor_id=<id-or-none>; sha256=<64-hex>; brief=<full brief>`.
  Tool identity is provenance, never the extracted style (source reference rule).
- **Generated assets are per-edit disposables** under the edit's working directory
  (`assets-generated/`). They graduate to `assets/` only when the project lead accepts one as a
  reusable production material (foundation-pack precedent: manifest + license note +
  checksum).
- AI-generated images have no third-party license chain, but they are **not** license
  proof for depicted logos/brands/celebrity likenesses — brief around those.
