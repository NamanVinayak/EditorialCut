---
description: Generate a contextual still (background, illustration, cutout, texture) through the EditorialCut image node.
---

Generate a contextual image asset through the project's image-generation node — never by
hand-drawing pixels or writing compositing code.

Read `skills/generate-image/SKILL.md` and follow it exactly. In particular:

1. Every hero or section-level asset needs a `contract_id` and is derived from the
   canonical `docs/rulebook/visual-design-contract.md`. The provider prompt is a derived
   output; the durable design knowledge stays in the contract.
2. If a donor is used, record its registry ID and run the donor verifier with
   `--donor-id <id> --require-usable` against `research/open-design-donors/donors.json`
   — this mechanically rejects missing, `reference-only`, and `rejected` records.
3. Delegate generation to an installed image-capable CLI (Codex `codex exec` by default
   for flat/literal assets; Antigravity `agy -p` for a photographic look). If you ARE
   Codex or Antigravity, use your native image tool directly.
4. Pixel-check every returned image against the contract's `acceptance_evidence`. Verify
   pixels, not the generator's own description. Re-brief once on failure; if the second
   attempt fails, change route rather than stacking prompt patches.
5. Write the provenance line and land accepted files in the edit's `assets-generated/`.

This is the post-base-cut image node in `docs/rulebook/input-routing.md`. It supplies a
still asset only — never the story, cut, timing, typography, depth decision, or motion.

$ARGUMENTS
