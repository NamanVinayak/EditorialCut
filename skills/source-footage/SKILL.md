---
name: source-footage
description: Invoke when a beat wants a real-world visual the presenter footage can't show (establishing shot, human situation, concrete object) and you want genuine stock/archive motion footage. Fetches free HD candidates from stock libraries and optionally CLIP-ranks them as an aid. Do NOT auto-pick by CLIP score or hardcode a source-first fallback chain; it finds candidates only — the pick and the real-vs-generate call are human/vision judgment.
---

# Source Footage (real / stock b-roll)

## Overview

Given a plain-language beat description, fetch real, free, HD candidate clips from stock/archive
libraries and present them for a human/vision pick. Optionally CLIP-rank the candidates as a tie-
breaking *aid* on literal content. This is **Shelf 1** of the b-roll model — the peer of
generating a shot, not a fallback for it. See
[`docs/capabilities/footage-sourcing.md`](../../docs/capabilities/footage-sourcing.md).

**Tier: TOOL+JUDGMENT.** Search + download + CLIP-rank are mechanical. *Whether* a beat should use
real footage at all, and *which* clip wins, are director decisions. Never auto-ship a CLIP pick.

## Inputs

- A **beat description**: a short `query` (2–4 keywords, for the stock search) and a richer
  `clip_description` sentence (for CLIP scoring). See `beats.json` for the shape.
- Proven environment: `research/footage-sourcing/.venv` (CPython 3.12; `requests
  pillow numpy torch transformers<5`). `transformers` **must be `<5`** — the vendored embedder
  uses the pre-5.x `get_text_features`→tensor API.
- A free Pexels API key in `research/footage-sourcing/.env` (gitignored; never commit).

## Workflow

1. **Write the query well (this matters most).** Lead with the subject; 2–4 keywords; add a
   POV/register keyword (handheld, drone, OTS, macro, locked-off) or the emotional register.
   Measured effect is large: "hospital emergency corridor" returns calm empty halls, "doctors
   rushing patient stretcher" returns the urgency the beat wanted. A wrong POV is costlier to fix
   than a wrong grade — re-query, don't crop.
2. **Source.** Run `source_clips.py` — for each beat it searches Pexels video (landscape, ≥1280w,
   3–30 s), downloads the top N, extracts a representative frame (~1/3 in), and writes
   `out/manifest.json`. It drives the in-house `PexelsSource` adapter directly (no framework).
3. **Look.** Build `out/contact_sheet.jpg` (`make_contact_sheet.py`) and **view the frames** —
   don't judge from tags. Score each 1–5; use 3+ (5=use, 4=minor trim, 3=needs match). Below 3,
   re-query, try another library, or mark the beat for generation (Shelf 2).
4. **CLIP re-rank (optional aid).** Run `rank_clips.py` to embed frames + the `clip_description`
   and rank by cosine similarity. Use it only to surface the best **literal-content** match. **Do
   not** treat the score as quality: it anti-correlates with dramatic register (benchmark: a calm
   corridor outscored urgent paramedics). The green badge on the sheet is a suggestion, not a
   verdict.
5. **Pick — director/vision, not the tool.** Choose the clip by looking. Record which beats real
   footage served well and which stayed thin (→ Shelf 2 generate candidates).
6. **Placement is a separate step.** How/where/how-long/what treatment (cutaway vs inset vs
   composited into the 2.5D world) is downstream editorial, under the same color/authority rules.
   The rough in-edit proof is `make_demo.py` (full-frame cutaways) — a proof of concept, not the
   accepted treatment.

## Accepted envelope

Benchmarked 2026-07-21 on 4 metaphorical beats from the the prototype worked example concept.
Human/emotional situations (marriage, financial stress) and, after query sharpening, hospital
urgency → strong real footage. A specific dramatic register with no stock analogue (a chased
fugitive) → thin; that is a real Shelf-2 (generate) beat. Full write-up + evidence:
`research/footage-sourcing/RESULTS.md`.

## Boundaries

- **Find, not place, not pick.** Selection and treatment are judgment; only fetch + rank are
  mechanical.
- **CLIP score is not quality.** Ranking aid on literal content only. Never auto-pick; never use
  a low score to decide "generate instead" — that call is made by looking.
- **Real-vs-generate are peers.** Don't hardcode a source-first fallback chain.
- **Copyrighted subjects:** source *metaphorical* footage, never the protected work.
- **Keys & secrets:** Pexels key in gitignored `.env`; downloaded media and the venv are
  gitignored. Other libraries: ~7 keyless (Archive.org, Wikimedia, LoC, NASA/NOAA/ESA, Mixkit),
  more behind free keys (Pixabay). Pexels API docs: <https://www.pexels.com/api/>.
