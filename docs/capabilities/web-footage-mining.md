---
title: Web Footage Mining (open-web / YouTube b-roll)
aliases:
  - Mine Web Footage
  - YouTube B-roll Mining
  - Open-Web Sourcing
  - Shelf 3
type: capability
status: benchmarked-v1 (pipeline proven on 2 real cases; pending the project lead's in-edit taste acceptance)
updated: 2026-07-22
---

# Web Footage Mining (open-web / YouTube b-roll)

## Decision

**The mining mechanic is proven end-to-end on two real cases and recommended for v1 as a
delegated sub-agent job.** Given a beat that wants a *real, specific* visual that stock
libraries don't hold and generation can't reproduce, the system searches YouTube, downloads a
short shortlist as low-res proxies, uses **CLIP to locate the exact seconds** the visual appears
inside long videos, has a vision pass verify them, and then HD-pulls **only the chosen seconds**.
The director only ever sees a tiny shortlist — the downloaded videos and thousands of frames
never touch the main thread.

**What is NOT accepted yet:** (1) how a mined clip should *appear* in the edit (cutaway vs inset
vs mosaic) — the same pending taste-treatment layer as Shelf 1; (2) automatic *selection* — the
pick is a human/vision judgment, never an automatic CLIP-score pick; (3) the specific-person
**reference-image** mode is *coded and possible but not yet demonstrated on a real miss* (see
below). This page documents the **find** layer, not the **place** layer.

This is **Shelf 3** of the b-roll model — the same F11 "source" arm as Shelf 1, extended from
curated stock libraries to the **uncurated open web**. Real footage (stock or web-mined) and
AI generation are **peer** editorial choices per beat, never retrieval-first-with-fallback. See
[`docs/rulebook/beat-to-primitive-rules.md`](../rulebook/beat-to-primitive-rules.md) and the
b-roll sourcing model. Stock is Shelf 1
([`footage-sourcing`](footage-sourcing.md)); generate is Shelf 2 (built, cost-guarded, unfired).

## Editorial purpose

Some beats want a shot that is *real and specific* and lives nowhere else — a Spider-Man trailer
frame, the Taj burning during 26/11, White Rock BC's pier, a the prototype worked example hospital scene buried
inside a five-minute compilation. Stock (Shelf 1) doesn't hold specific real things; generation
(Shelf 2) can't reproduce a *real, specific* one convincingly. The open web does — but the wanted
shot is almost always **a few seconds buried inside a longer video that's about something else**
(an anchor talking, music playing, a whole scene compilation). The transcript can't tell you
*where* those seconds are, or even reliably *whether* they're there.

### The core split — transcript routes, CLIP locates, the LLM verifies

1. **Transcript / metadata = ROUTING.** Title, description, and (for talky topics) cheap captions
   pick *which* videos are topically about the right subject and worth downloading. For pure-visual
   targets (a trailer, scenery) even routing is title/thumbnail-driven; transcript barely matters.
2. **CLIP = LOCATING.** Visual search finds the exact moment inside a long video — the needle the
   transcript can't point to. This is the primary lens for b-roll.
3. **LLM = VERIFYING.** A vision pass looks at the top candidate windows and confirms it's the
   *right specific thing*, not a lookalike, at a usable framing/length. CLIP alone can't judge;
   the LLM alone can't cheaply scan thousands of seconds. The coarse-sniff → fine-judge split is
   required, not optional.

### The LLM is the engine — and it can web-search

The single most important input is the **visual query**, and writing it is an LLM job. World
knowledge turns an abstract reference into concrete visual language CLIP can match ("White Rock
BC" → "long wooden pier over the ocean, seaside promenade, large white boulder on the beach").
When the reference is obscure, or an accurate/current visual is needed, the LLM **searches the
web** (WebSearch/WebFetch) to derive the distinguishing visual traits — or to fetch a **reference
image** for image→image search (see the specific-person mode below).

## Use it for

- A beat that needs a **real, specific** thing stock can't serve and generation can't reproduce:
  a named landmark, a real event's footage, a specific place, a recognizable scene.
- Finding the exact **few seconds** a visual appears inside a long video (news clip, trailer,
  scene compilation, drone flyover, music video) where the transcript gives no marker.
- The **download-once / embed-once / hunt-many** shape: pull one corpus of topic-relevant videos,
  embed every frame once, then locate *every* moment an edit needs against the shared embeddings
  (proven on the prototype worked example — 8 opportunities against one 5-video corpus in a single pass).

## Do not use it as

- **An automatic clip picker.** CLIP score is a ranking aid on *literal content* only. It does
  not capture dramatic register and (proven on Shelf 1 and here) anti-correlates with it. The pick
  is a human/vision judgment. Never ship the top score unseen.
- **A specific-identity recognizer.** CLIP knows *generic categories* ("a domed hotel", "a pier",
  "a menacing man") far better than *specific entities* ("the Taj Mahal Palace Hotel", "the
  villain Rukma"). On the the prototype worked example test a "menacing villain" text query returned the **hero**
  (the most prominent man on screen), because CLIP can't know who the villain is. → the LLM verify
  step is mandatory, and specific *people* need the reference-image mode.
- **A rights-clearance tool.** It *finds* clips; it does not clear rights. yt-dlp downloading
  violates YouTube ToS and short-excerpt reuse is a copyright gray area. That editorial/legal call
  stays with the project lead — documented as a boundary, not a blocker.
- **The place layer.** How/where/how-long a mined clip appears, and in what treatment, is
  downstream editorial under the same color/authority rules — the same pending taste pass as
  Shelf 1.

## Query construction — describe the LOOK, never the ROLE

CLIP matches what a shot **looks like**, not who someone *is* or what a scene *means*. This is the
single biggest lever on quality, and the most common way to get it wrong.

- **Describe the visible content:** subjects, setting, lighting, action, framing. "a man in a dark
  coat glaring across a dim room" — not "the villain". "a person in a hospital gown lying in a
  ward bed" — not "the sick hostage". A role/name/character label gives CLIP nothing to match; a
  concrete visual description gives it everything.
- **The the prototype worked example proof:** "a menacing intense villain man staring, dramatic thriller antagonist"
  returned the **protagonist** — CLIP matched "menacing man" to the most prominent face, having no
  concept of which character is the antagonist. Naming the role actively misled it.
- **Lead with the subject**, then setting, then register — same rule that fixed the Shelf 1
  hospital/fugitive beats. Keep it inside CLIP's 77-token limit; concrete nouns over adjectives.

## Specific-person mode — find who they are, then search by their face (reference image)

Text can't disambiguate a specific *person* — "menacing man" matched the hero. For a named or
recognizable individual, use the **reference-image** path instead of (or alongside) a text query:

1. The LLM **web-searches to identify the person** and find a clear reference still of them (their
   real face, the real landmark, the real event).
2. Pass that still to `mine.py --ref-image ref.jpg`. CLIP does **image→image** search natively —
   matching the actual face/object across every downloaded video, far more precise than any text
   query for a specific entity.
3. `--ref-image` can combine with `--query` (the query vector is the mean of the text and image
   embeddings) — useful to bias "this face **in an action setting**".
4. The LLM verify pass still confirms it's the right person, not a lookalike.

**Status:** `--ref-image` is coded and CLIP does image→image natively, but it has **not yet been
demonstrated on a real miss** — the the prototype worked example "villain → returned the hero" failure is the exact
case it's meant to fix, and closing that loop is the next validation. Same technique serves
specific *places/objects* (a still of the real Taj → image→image across all downloaded videos).

## The delegated sub-agent shape (why this is a sub-agent, not inline)

The whole job runs inside **one mining sub-agent** (delegated to protect the director's context;
it keeps the user's model because it does visual judgment — per the two-axis delegation policy it
is *not* downgraded). The bulk work is deterministic **code**, not nested agents: parallel
download is a `ThreadPoolExecutor`, sampling + CLIP are scripts. The director sends a small source
brief out and gets a small shortlist back (video URL + in/out timecodes + peak frame + why +
confidence). The 5–15 downloaded videos, thousands of frames, and all CLIP scores live in the
sub-agent and on disk — never in the main thread.

## The pipeline

Given a **source brief** `{beat, reference, visual_query text and/or reference_image,
acceptance_criteria, count}`:

1. **Search & route** — LLM expands the reference into YouTube queries (world knowledge, + web
   search when obscure); for talky topics, cheap captions shortlist the ~5–15 likely videos.
2. **Proxy download** — `yt-dlp` at ~480p into a temp dir, parallelized (thread pool).
3. **Sample** — frames at a fixed fps (0.5–1). (Shot-detection not yet wired — see limits.)
4. **CLIP locate** — embed all frames + the text query and/or reference image; cosine-rank → group
   high-scoring frames into candidate **moments** `(video, in, out)` → `candidates.json` + contact
   sheet.
5. **LLM verify** — look at the top windows; confirm the right specific thing, usable framing.
   Return the small shortlist to the director.
6. **Director picks** — reviews thumbnails + timecodes, picks.
7. **HD conform** — `yt-dlp --download-sections "*in-out" --force-keyframes-at-cuts` pulls ONLY the
   chosen seconds at max quality; proxies discarded. (Runbook Stage 6.)

## Accepted envelope (benchmark, 2026-07-22)

Two real cases, both verified by looking at the contact sheets:

- **White Rock BC pier (easy / pure-scenery case).** `mine.py` located the pier buried inside a
  10-minute drone flyover; **all 8 candidates were the real pier, zero lookalikes.** `conform.py`
  HD-pulled two of them in full **4K** as 9 s / 21 s clips (24 MB / 53 MB) after mining only the
  480p proxy. Proves stock can't serve White Rock, YouTube can, and the proxy→conform two-pass
  finds the exact seconds cheaply.
- **the prototype worked example (harder / buried-moment case).** `mine_multi.py` downloaded one corpus of 5
  scene compilations, embedded 599 frames once, and hunted **8 b-roll opportunities** against the
  shared embeddings. **~6/8 landed usable scenes pulled from inside multi-scene compilations**
  (hero, hospital ward + bandaged-head injury, family-in-danger, marriage tension; action and
  standoff usable). This validated the download-once/embed-once/hunt-many production shape **and
  both predicted failure modes**: "on the run" was weak (dramatic-register wall), and "villain"
  returned the hero (specific-identity limit → the reference-image mode's target case).

## Boundaries & honest limits

- **Find, not place, not pick.** Selection and treatment are judgment; only download + sample +
  CLIP-rank + conform are mechanical.
- **CLIP score is not quality** and does not decide source-vs-generate. Ranking aid on literal
  content only; the pick and the source-vs-generate call are made by looking.
- **Generic > specific.** CLIP recognizes categories better than specific entities → the LLM
  verify step is mandatory; specific people need the reference-image mode.
- **Dramatic register wall.** A still can't feel "the moment he realizes he's betrayed" or
  "fleeing". Same ceiling as Shelf 1. The LLM look-pass partly covers it; don't expect CLIP to.
- **Short-insert recall.** A 1–2 s insert can fall between sampled frames. Fixed-fps sampling is
  used today; wiring the accepted [`detect-shots`](../capabilities/shot-detection.md) skill would
  sample smarter. Report recall honestly.
- **No diversity constraint yet.** Top moments can cluster in the single best video / near-
  duplicate angles. A per-video cap / MMR is a wanted refinement.
- **yt-dlp at scale.** Small runs are fast; a 40-video run may hit throttling. Keep the transcript-
  route + shortlist tight.
- **ToS / copyright.** yt-dlp downloading violates YouTube ToS; short-excerpt reuse is a legal gray
  area. The tool finds clips; rights clearance is the project lead's editorial call.
- **Color / authority.** Mined footage is real footage → the color-lock and authority rules apply
  unchanged. Placement/treatment is the pending taste layer, not part of this build.
- `transformers` must be `<5` for the vendored CLIP embedder (pre-5.x tensor API).

## Evidence & reference implementation

- `research/web-footage-mining/` — `mine.py` (search → proxy download → sample → CLIP
  locate → candidates), `mine_multi.py` (download-once / embed-once / hunt-many), `conform.py` (HD
  section pull), `RESULTS.md`, `out/smoke-whiterock/`, `out/run1/opportunities.jpg`. Own
  `.venv` (yt-dlp + CLIP `transformers<5`); reuses the vendored `clip_embedder` from Shelf 1.
- Skill: [`skills/mine-web-footage/SKILL.md`](../../skills/mine-web-footage/SKILL.md). Our own
  design: instead of indexing short stock clips, it indexes moments *inside* long videos keyed by
  `(video, start, end)` — download-once, embed-once, hunt-many across a shared frame index.
