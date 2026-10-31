---
title: Locked-look contract — the frozen style every parallel worker obeys
type: rulebook
status: active
date: 2026-07-16
---

# Locked-look contract (`locked-look.md`)

## Why this exists

The preview/parallel workflow renders different scenes in **parallel workers** so the
director isn't waiting on one serial 5-minute render. But parallel workers with no shared
style each invent their own look — and you get five scenes that look like five different
videos, *faster*. That is the exact inconsistency this project already suffers, multiplied.

The fix is a **lock**: one director decides the whole-video look **once**, freezes it, and
hands the identical frozen contract to every worker. Workers **execute**; they never make a
style or story choice (the delegation-failed-twice rule — composition/taste stays with the
one director). The locked look is what makes parallelism safe.

This is the whole-video companion to the per-beat
[`visual-design-contract.md`](visual-design-contract.md): the visual-design-contract governs
*one hero beat*; the locked-look governs *the film's shared identity* that all beats and all
workers share.

**The locked look is the frozen *output* of the [`look-derivation-recipe.md`](look-derivation-recipe.md).**
Do not invent the palette/type/concept from taste alone or copy a previous video's — **derive**
them from *this* footage and register (accent from the scene's motivated light, type motif from
the genre, concept from the topic's real-world artefact), then freeze the result here. The
frozen tokens become the generic kit's `look.json`
([`presenter-world-kit`](../../research/presenter-world-kit/README.md)).

## When it is written and frozen

Written after Stage 4 (beat map) and Stage 4a (hero-beat contracts) are done, and **frozen
before any parallel proxy render is dispatched** (runbook Stage 5b). A change to the locked
look after workers have started means re-issuing the new lock to every worker — so lock it
deliberately, not casually.

## The frozen fields

```markdown
# Locked look — <edit-slug>  (status: frozen | draft)

- **Declared mix:** <paste declared_mix.intent + dominant + single_mode from beat-map.json>
- **Pace:** fast | medium | slow — target cut/treatment density and hold discipline (N1).
- **Palette:** background, surface, primary text, secondary text, accent, semantic states.
- **Typography role palette:** attention / identity / editorial / annotation / utility /
  caption — family, weight, size range, source, license, fallback, and which roles
  intentionally share a family. This is a coherence contract, not a demand for six fonts.
- **Material language:** clean digital | paper | print | archival | photographic | screen —
  one justified family for the film; per-section deviations must be named here.
- **Motion character:** the film's default easing/entry/exit feel and the default hold.
- **Camera vocabulary:** which accepted N10 atoms (T1–T4) are in play and their default
  magnitude/perceptibility floor. T5 is never allowed.
- **Capability register:** the default combination for an effect moment when the topic
  allows it — masking + on-screen element + camera move + caption together (the source reference
  register, the project lead 2026-07-16), not a lone caption. Name where the film deliberately goes
  minimal instead.
- **Engine routing:** default engine per family (reuse-first policy) — HyperFrames for
  presentation/motion-design, Remotion for overlay/alpha depth, FFmpeg for audio/assembly —
  so workers on different scenes still emit portable, consistent contracts.
- **Proxy spec:** the low-resolution/preview settings every worker renders at (e.g.
  640×360, draft quality, watermarked "PROXY") so previews are cheap and never mistaken for
  the final conform.
- **Section overrides:** any section that intentionally departs from the above, with the
  story reason (mirrors the beat map's sections).
- **Treatment vocabulary:** which reusable type relationships are available in this film
  (`identity_lockup`, `hero_field`, `thesis_build`, `editorial_note`,
  `support_overlay`) and any section-specific restraint. A vocabulary is permission, not
  a quota.
```

## The contract workers receive

Each parallel worker is handed exactly three things and nothing else it must decide:

1. this **frozen locked-look**;
2. its **beat spec(s)** from `beat-map.json` (the `is_effect_moment` beats it owns);
3. read access to the **cached analysis facts** (transcript, beats, mask) for its window.

A worker renders a **proxy** of its moment(s) at the locked proxy spec and returns the clip
+ the exact command it ran. It does not choose mode, palette, typography, timing, or which
beats get treated — those are already decided. If a worker finds its beat spec is
impossible as written, it **stops and reports back**; it does not improvise a different look.

## Relationship to the mode-mix gate

The locked look's **Declared mix** is copied straight from `beat-map.json`'s `declared_mix`,
which the [`check-mode-mix`](../../skills/check-mode-mix/SKILL.md) gate enforces. So the lock
can never quietly disagree with the gate: same declaration, one source of truth.
