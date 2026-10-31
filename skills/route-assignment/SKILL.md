---
name: route-assignment
description: Invoke at the very start of ANY editing assignment to classify cut authority and color authority before any selection, reorder, retiming, replacement, or new editorial timing. Wraps the input-routing rulebook — do NOT infer permission from file type or a style adjective; read-only inventory may proceed while authority is unresolved, structural editing may not.
tier: JUDGMENT
---

# route-assignment

**Job:** be the first thing you do on any edit. It classifies how much editorial control
the user actually granted and whether color work is permitted, so structural editing
never begins on assumed authority. This is a thin governance wrapper so the routing rule
pages in by description-match even if the working contract gets trimmed — the full rule
is the source of truth.

## Read this now

[`docs/rulebook/input-routing.md`](../../docs/rulebook/input-routing.md) — the assignment
router in front of the whole creative-director workflow. Follow it exactly; this skill
does not restate it.

## The one rule

**User intent plus explicit authority outranks file type.** A folder of raw clips does
not grant recut permission; a flattened MP4 does not mean its structure is locked.
Read-only inventory and analysis may continue while authority is unresolved. Selection,
shortening, reordering, replacement, and newly authored editorial timing may **not**
begin until authority is clear.

## What to record before any structural mutation

Write the compact route contract from `input-routing.md` into the edit's working log,
with exactly one mode and its matching authority:

- `POLISH_LOCKED` / `locked`
- `ASSEMBLE_RAW` / `assemble`
- `COMPOSE_FROM_PARTS` / `compose`
- `HYBRID_SCOPED` / `scoped`

Record `color_authority` separately. It defaults to `unchanged` on every route and
becomes `explicit` only when the user names color correction, grading, white balance,
exposure, contrast, saturation, gamma, hue, temperature, or a LUT. "Cinematic," "visual
polish," and "make it pop" never grant a grade.

If `unresolved_authority` is not `none`, inventory only and ask one concrete question
that distinguishes the plausible routes.

## Boundaries

This is a router, not a renderer, planner, or second director. Once authority is locked,
hand the accepted route to the orchestration runbook and the catalogued skills. It reads
intent, never pixels.
