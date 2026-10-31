---
title: B-roll Footage Sourcing (real / stock)
aliases:
  - Stock Footage Sourcing
  - Source B-roll
  - Fetch Real Footage
  - Shelf 1
type: capability
status: benchmarked-v1 (pending the project lead's in-edit taste acceptance)
updated: 2026-07-21
---

# B-roll Footage Sourcing (real / stock)

## Decision

**The sourcing mechanic is proven on a benchmark and recommended for v1.** Given a plain-language
description of a beat, the system fetches real, free, HD candidate clips from stock/archive
libraries (Pexels proven; ~15 more keyless/keyed adapters available), and can CLIP-rank them as
an *aid*. Zero cost beyond a free API key, seconds per beat, 100% fetch success on the benchmark.

**What is NOT accepted yet:** (1) how the b-roll should *appear* in the edit (full cutaway vs.
inset vs. composited into the 2.5D presenter world) — that is a taste treatment, still owed a
review pass; (2) automatic *selection* — the winning clip is a human/vision judgment, never an
automatic CLIP-score pick. This page documents the **find** layer, not the **place** layer.

This is **Shelf 1** of the b-roll model. Real footage and AI-generated footage are **peer**
editorial choices per beat (never retrieval-first-with-fallback) — see
`docs/rulebook/beat-to-primitive-rules.md` and the b-roll sourcing model. Shelf 2
(image → image-to-video) is separate and not yet built.

## Editorial purpose

Fill a beat that wants a real-world visual the presenter footage cannot show — an establishing
shot, a human situation, a concrete object — with genuine motion footage, so the cut carries the
*truth* of a thing that exists. This is the counterpart to generating a shot: reach here when the
beat needs to look **real**; generate when it needs to look **specific to a concept that doesn't
exist on film**.

### Two sub-layers (both mechanical tools; the decisions around them are not)

1. **Sourcing** — keyword search against a stock library → download candidates → extract a
   representative frame. Deterministic once the query is written.
2. **CLIP re-rank (optional aid)** — embed each candidate frame + a richer beat description with
   CLIP ViT-B/32 and rank by cosine similarity. Helps surface the best *literal-content* match
   when keyword order is poor.

### Use it for

- Beats that are human/emotional situations or real-world establishing shots — where stock is
  deep (proven: relationship tension, financial stress, hospital/paramedic urgency).
- Getting several real HD candidates fast and cheap, as raw material for a human/vision pick.
- CLIP re-ranking to break ties on **literal scene content** (e.g. "turned away / distant" beat
  an "arguing" clip when the description said distant).

### Do not use it as

- **An automatic clip picker.** CLIP score does **not** capture dramatic register and in the
  benchmark *anti-correlated* with it (a calm empty corridor scored higher than urgent
  paramedics). Selection is a human/vision judgment. Never ship the top CLIP score unseen.
- **A source-vs-generate decider.** Low CLIP score ≠ "generate instead." That call is taste, made
  by looking at frames — not by a threshold.
- **The place layer.** How/where/how-long the clip appears, and in what treatment, is an editorial
  decision downstream, gated by the same color/authority rules as the rest of the edit.
- A source of the actual subject when the subject is copyrighted (e.g. a specific TV show). Source
  **metaphorical** real footage for the concept instead.

## Query construction (benchmark-confirmed)

Query wording had a *large* measured effect — it fixed one weak beat entirely and materially
improved another. Rules:

- **Lead with the subject**, 2–4 keywords. "hospital emergency corridor" (too literal) → calm
  empty corridors; **"doctors rushing patient stretcher"** → paramedics/urgency.
- **Add a POV / register keyword** — handheld, drone, aerial, OTS, macro, top-down, locked-off —
  and/or the emotional register. "man running crowded city street" → marathons; **"person running
  night alley handheld"** → a fleeing figure.
- **Try synonyms on failure**, then the other library, and only then consider generating.
- A wrong POV is costlier to fix than a wrong grade — re-query rather than crop your way out.

## Accepted envelope (benchmark, 2026-07-21)

- Proven on 4 metaphorical beats from the the prototype worked example (the prototype worked example analysis)
  concept: **marriage collapse** and **financial stress** → strong real footage out of the box;
  **hospital/stakes** → solved after query sharpening; **on-the-run/fugitive** → improved but
  thin, a genuine Shelf-2 (generate) candidate.
- Pexels adapter, HD (1920×1080) landscape, 3–30 s clips, top-6 per beat, ~seconds/beat, free.
- In-context rough proof: full-frame cutaways over the real rendered edit
  (`research/footage-sourcing/out/demo/EditorialCut-demo.mp4`).

## Boundaries

- **Find, not place.** Placement/treatment/timing is a separate editorial step.
- **CLIP is an aid, not a judge.** Literal-content ranking only; register and selection are human.
- **Real-vs-generate is a peer taste choice**, decided by looking — not automated.
- **Copyrighted subjects:** source metaphorical footage, never the protected work itself.
- `transformers` must be `<5` for the CLIP embedder (pre-5.x tensor API). Pexels key
  lives in a gitignored `.env`.

## Evidence & reference implementation

- `research/footage-sourcing/` — the Pexels adapter (`pexels.py` + `base.py`) and CLIP
  embedder (`clip_embedder.py`), driver scripts, `RESULTS.md`, `out/contact_sheet.jpg`,
  `out/sharpen/sharpen_compare.jpg`, `out/demo/EditorialCut-demo.mp4`.
- Skill: `skills/source-footage/SKILL.md`. Pexels API: <https://www.pexels.com/api/>.
