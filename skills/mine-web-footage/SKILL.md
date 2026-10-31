---
name: mine-web-footage
description: Invoke when a beat wants a REAL, SPECIFIC visual that stock libraries don't hold and generation can't reproduce (a named landmark, a real event, a specific place, a recognizable scene) — and it likely lives as a few seconds buried inside a longer web/YouTube video. Runs as a delegated sub-agent that searches YouTube, downloads low-res proxies, uses CLIP to LOCATE the exact seconds, has a vision pass VERIFY them, and returns a tiny shortlist; HD-conform pulls only the chosen seconds. Do NOT auto-pick by CLIP score; it finds candidates only — the pick and the real-vs-generate call are judgment.
---

# Mine Web Footage (open-web / YouTube b-roll — Shelf 3)

## Overview

Locate a *real, specific* visual buried inside long web videos and return a small shortlist of
exact-second candidates. This is **Shelf 3** of the b-roll model — the same F11 "source" arm as
Shelf 1, extended from curated stock to the uncurated open web. Real footage (stock or web-mined)
and generation are **peer** choices per beat, never a fallback chain. See
[`docs/capabilities/web-footage-mining.md`](../../docs/capabilities/web-footage-mining.md).

**Tier: SUB-AGENT.** Run the whole job inside **one mining sub-agent** so the downloaded videos,
thousands of frames, and all CLIP scores never touch the director's context. The sub-agent keeps
the user's model (it does visual judgment — per the two-axis delegation policy it is *not*
downgraded). The bulk work is deterministic code (thread-pool download, ffmpeg sampling, CLIP
scripts), not nested agents. The director sends a small brief out and gets a small shortlist back.

## When to reach for this (vs Shelf 1 stock / Shelf 2 generate)

- The beat needs a thing that is **real AND specific** — a named landmark, a real event's actual
  footage, a specific place, a recognizable scene. Stock (Shelf 1) holds generic human/emotional
  situations, not specific real things; generation (Shelf 2) can't reproduce a real specific one.
- The wanted shot is likely **a few seconds inside a longer video about something else** (a news
  clip, a trailer, a scene compilation, a drone flyover), so the transcript can't locate it.
- These are **peers**, not a ladder. Choose web-mine when the beat must look *true and specific*;
  don't fall through to it only after stock fails.

## The lightweight trigger (ask first — do not auto-fire)

At the moment a beat could use open-web b-roll, **ask the project lead one simple go/no-go question** and
honor his session preference — do NOT auto-search and do NOT write a heavy proposal:

> "Want me to search YouTube for real footage of *[X]* for this beat?"

Follow the stated preference for the session: `ask-each` (default — ask per beat), `auto` (go
without asking this session), or `no` (don't). Downloading is against YouTube ToS and short-excerpt
reuse is a copyright gray area; the go/no-go and rights call are the project lead's, not the tool's.

## Inputs — the source brief (director → sub-agent)

```
beat                : which beat, and the spoken idea
reference           : the real specific thing wanted ("White Rock BC pier", "Taj during 26/11")
visual_query        : a LOOK description for CLIP text search (see the query rule below)
reference_image     : (optional) path to a still of the specific person/place/object — image search
acceptance_criteria : what makes a candidate the RIGHT one (not a lookalike); usable framing/length
count               : how many candidate moments to return
```

Proven environment: `research/web-footage-mining/.venv` (CPython 3.12; `yt-dlp` + CLIP
`pillow numpy torch transformers<5`). `transformers` **must be `<5`** — the vendored embedder uses
the pre-5.x `get_text_features`→tensor API. Reuses the vendored `clip_embedder` from Shelf 1.

## The two rules that decide quality

### 1. Describe the LOOK, never the ROLE (text query)

CLIP matches what a shot **looks like**, not who someone *is* or what a scene *means*.

- **Do:** "a man in a dark coat glaring across a dim room", "a person in a hospital gown in a ward
  bed", "a long wooden pier over the ocean at sunset". Subject → setting → lighting → action →
  register. Concrete nouns over adjectives. Stay inside CLIP's 77-token limit.
- **Don't:** "the villain", "the sick hostage", "the hero's darkest moment". A role/name/character
  label gives CLIP nothing to match and actively misleads it.
- **Proof:** on the the prototype worked example test, "a menacing intense villain man staring" returned the
  **protagonist** — CLIP matched "menacing man" to the most prominent face, having no concept of
  which character is the antagonist. Same rule that fixed Shelf 1's hospital/fugitive beats.

### 2. Specific person → find who they are, then search by their face (reference image)

Text can't disambiguate a specific *person* — "menacing man" matched the hero. For a named or
recognizable individual (or a specific landmark/object):

1. **Web-search to identify them** and fetch a clear reference still of their real face (or the
   real landmark/event) — WebSearch/WebFetch.
2. Pass it to `mine.py --ref-image ref.jpg`. CLIP does **image→image** search natively, far more
   precise than any text query for a specific entity.
3. `--ref-image` can combine with `--query` (query vector = mean of text + image embeddings) — e.g.
   bias "this face **in an action setting**".
4. Still run the LLM verify pass — confirm it's the right person, not a lookalike.

> Status: `--ref-image` is coded and CLIP does image→image natively, but not yet demonstrated on a
> real miss. The the prototype worked example "villain → returned the hero" failure is its exact target case.

## Workflow (inside the mining sub-agent)

1. **Search & route** (LLM). Expand the reference into YouTube search queries with world knowledge;
   **web-search when the reference is obscure or needs an accurate/current visual**. For talky
   topics, pull cheap captions (`mcp__youtube-transcribe-local__*`, or `yt-dlp --write-auto-subs
   --skip-download`) to shortlist the ~5–15 videos most likely to contain the visual. Transcript =
   routing (which videos), CLIP = locating (which seconds).
2. **Mine** (code). `mine.py --search "<yt query>" --n <k> --query "<LOOK description>"` (and/or
   `--ref-image ref.jpg`) `--fps 0.5 --out out/<run>`. It downloads ~480p proxies in parallel,
   samples frames, CLIP-embeds + ranks, groups high-scoring frames into candidate moments
   `(video, in, out)`, and writes `candidates.json` + `candidates.jpg`. For the download-once /
   embed-once / **hunt-many-opportunities** shape (one topic corpus, many beats), use the
   `mine_multi.py` pattern — embed the corpus once, run each opportunity's query against the shared
   embeddings.
3. **Verify** (LLM, vision). **Look at `candidates.jpg`** — confirm each top moment is the RIGHT
   specific thing per `acceptance_criteria` (not a lookalike), at usable framing/length. Discard
   register-only misses and wrong-identity hits. Do not trust the CLIP score as quality — it's a
   literal-content ranking aid and anti-correlates with dramatic register.
4. **Return the small shortlist** to the director: `[{url, in, out, peak_t, peak_frame_path, why,
   confidence}]` — nothing else crosses the boundary.

## Outputs — the shortlist contract (sub-agent → director)

Return **only** the small shortlist (video URL + in/out timecodes + peak frame thumbnail + one-line
why + confidence). Never dump raw videos, frame directories, or full CLIP score tables into the
main thread — they stay in the sub-agent and on disk. The director reviews thumbnails + timecodes
and **picks by looking**.

## HD conform (runbook Stage 6, after the director picks)

`conform.py --from-candidates out/<run>/candidates.json --pick <i> <j> --dest out/hd` (or
`--url <URL> --in <sec> --out <sec>`) pulls **only the chosen seconds** at max quality via
`yt-dlp --download-sections "*in-out" --force-keyframes-at-cuts`; proxies are discarded. It
`ffprobe`s each output so you can confirm the real duration/resolution (White Rock benchmark:
480p mine → 4K conform of just the picked 9 s / 21 s).

## Accepted envelope (benchmark, 2026-07-22)

Two real cases, verified by looking:
- **White Rock BC pier (easy/scenery):** located the pier inside a 10-min drone flyover; all 8
  candidates were the real pier, zero lookalikes; conformed two in 4K.
- **the prototype worked example (harder/buried-moment):** one 5-video corpus, 599 frames embedded once, 8
  opportunities hunted; ~6/8 usable scenes pulled from inside compilations; validated both failure
  modes (register wall on "on the run"; specific-identity miss on "villain" → the reference-image
  target case). Full write-up: `research/web-footage-mining/RESULTS.md`.

## Boundaries

- **Find, not place, not pick.** Selection and treatment are judgment; only download + sample +
  CLIP-rank + conform are mechanical. Placement/treatment is the pending taste layer (same as
  Shelf 1), under the same color/authority rules — mined footage is real footage.
- **CLIP score is not quality** and does not decide source-vs-generate. Ranking aid on literal
  content only; the pick is made by looking.
- **Generic > specific.** LLM verify is mandatory; specific people need the reference-image mode.
- **Register wall.** A still can't feel "fleeing"/"betrayed". Don't expect CLIP to close it.
- **Recall.** A 1–2 s insert can fall between fixed-fps frames; wiring `detect-shots` would sample
  smarter. Report recall honestly.
- **ToS / copyright.** yt-dlp downloading violates YouTube ToS; short-excerpt reuse is a legal gray
  area. The tool finds clips; rights clearance is the project lead's editorial call — hence the go/no-go ask.
- **Context protection.** Run in a sub-agent; only the shortlist crosses back. `transformers<5`.
