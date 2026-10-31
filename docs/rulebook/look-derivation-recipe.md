---
title: Look-derivation recipe — how a video's visual look is DERIVED (genre-agnostic)
type: rulebook
status: active
date: 2026-07-18
---

# Look-derivation recipe

The stylistic wins the project lead approved on `representative long-form test` (2026-07-18) are
kept as a **method, not a template**. The engine must make the *same kind* of choices on any
footage, topic, or genre — and it does that by **deriving** the look from *this* video every
time, never by reusing one video's palette/fonts/concept.

This is the project's standing principle applied to visual design: *capability knowledge =
derivation recipes, never a stock library of source-specific examples* (CLAUDE.md). The
[`locked-look-contract.md`](locked-look-contract.md) is the *frozen output* of this recipe for
one video; this file is the *procedure that produces it*. The output feeds the generic
[`presenter-world-kit`](../../research/presenter-world-kit/README.md) as `look.json`.

> **Anti-rule (read first):** never carry `#E8B04B` amber, Courier kickers, or "case file"
> forward as *the* style. Those are the *screenwriting* video's derived answers. A different
> video derives different answers from the same four steps below.

## The four derivations (run per video)

### 1. Accent ← the footage's motivated light/colour
Sample the scene's **motivated key colour** — the dominant practical light, a signature
wardrobe/prop colour, or the graded highlight — and make that the single accent. This ties
the graphics to the room instead of importing a brand colour that fights it.
- *Method:* sample a mid-scene frame; take the dominant warm/attention hue of the key light or
  a recurring saturated object; pick one accent + optionally one semantic-negative that
  contrasts it. Keep to **one** accent (scarcity).
- *Worked:* screenwriting → warm amber `#E8B04B` from the room lamp; brick-red `#C25B4A` for
  conflict/critique.

### 2. Type ← the video's register/genre and each beat's job (role-based, F14)

Derive a coherent role palette — **attention / identity / editorial / annotation /
utility / caption** — whose motifs match the subject. This is not a requirement for six
different font families: one family may fill several roles, and a section may use a
distinct editorial or handwritten accent when the story benefits.

- *Method:* select an attention face for major claims; an identity/utility face for names
  and facts; an editorial face for reflective or quoted language; an optional annotation
  face for restrained handwritten/cursive interventions; and a clean caption face.
- *Beat selection:* the communicative job chooses which role is active. The look supplies
  the coherent palette; it does not force every beat through the attention face.
- *Worked:* screenwriting → Helvetica Neue can carry attention/identity; Courier can carry
  screenplay-derived utility; Georgia can carry editorial language; a licensed
  handwritten face could be assigned only to a genuine annotation. Exact families remain
  per-video answers.

### 3. Concept/material ← the genre's artefact
Name the real-world artefact the topic lives in, and let material + card grammar echo it —
subtly (texture ≤ ~8%, never skeuomorphic kitsch).
- *Worked:* screenwriting → "screenwriter's **case file**", subtle paper grain on cards.

### 4. Placement ← the measured frame (N3, N3.1)
Where graphics sit is derived from *this* framing, not a fixed grid: put elements in the
measured empty third, seat the presenter opposite, and **measure the subject for every
inset/crop** (N3.1). Camera opens the side the graphic will occupy (N7/N10).

## The same recipe on other genres (proof it is not one look)

| Genre / footage | 1. Accent (from footage) | 2. Type motif (register) | 3. Concept/material | 4. Placement note |
|---|---|---|---|---|
| **Screenwriting analysis** (warm room, lamp) | amber from the lamp; brick-red negative | Courier kicker = screenplay; grotesque display; serif quote | "case file"; subtle paper grain | presenter centre/left, list in darker right third |
| **Finance / business explainer** (cool office, screen glow) | the UI/brand teal or the ticker-green from the monitor | tabular-figure mono for numbers; strong grotesque display | "terminal / ledger"; crisp digital, no paper | numbers in a right rail; presenter left; push on the metric |
| **Cooking / food** (warm kitchen, produce) | a saturated ingredient hue (chilli red, herb green) | a warm humanist serif display; handwritten-feel kicker | "recipe card"; matte card stock, light grain | steps lower-third; overhead insets measured on the dish |
| **Travel vlog** (daylight, landscape) | the sky/scene's dominant hue (sunset orange, sea blue) | a clean geo/sans display; ticket-stub mono kicker | "field notes / passport"; airy, minimal | location chips over the horizon third; presenter as anchor |
| **Tech / product review** (neutral desk) | the product's own accent colour | precise grotesque; monospace spec labels | "spec sheet"; clean digital | spec list right; measured device inset |

Every row is the **same four steps** producing a different, footage-appropriate look. If two
different-genre videos come out looking the same, the derivation was skipped — that is the
failure this recipe exists to prevent.

## What stays fixed across all videos (the engine, not the look)
These are mechanics, not style, and do **not** get re-derived:
- masked-presenter depth (`compose-presenter-world`); motivated + perceptible camera via the
  N10 registry atoms (T1–T4) rendered from the highest-res source; word-synced captions with
  the active-word accent (F10/N9); the overlay↔presentation **mix** (gate #10); land-be-read-
  leave restraint (N1/N2/N8); subject-measured crops (N3.1); role-aware typography,
  camera-safe semantic text, and the N2 pulse list. Kicker→display→support card is one
  available grammar, not a universal mechanic. The generic kit implements these mechanics;
  `look.json`, beat design intent, and beat content change per video.

## Provenance
the project lead, 2026-07-18: approved the screenwriting look on the proxy review and directed that the
engine "make the same kinds of stylistic choices across other videos, other topics, other
genres… make sure our engine is versatile, not just working good with one video." This recipe
+ the generic kit are that generalization; the true test is re-running the identical engine on
a different-genre video and getting an equally footage-appropriate result.
