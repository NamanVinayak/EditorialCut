---
title: Beat-map schema — the machine-readable plan the checks read
type: rulebook
status: active
date: 2026-07-16
---

# Beat-map schema (`beat-map.json`)

The runbook Stage 4 promised "output the **structured** beat map (the runbook fixes the
*format*; the director fills the *content*)." This file **is** that format. The director
still authors every creative choice; this only fixes the shape so a script can read it —
so the mode-mix check (and future plan checks) are **computable, not prose an agent can
forget** (the project's N9 lesson: a check that can be computed must be a script).

The director emits **one `beat-map.json`** per edit, saved in the edit's working folder.
Reasoning still lives in prose (`reason` fields here, plus the per-beat
[`visual-design-contract.md`](visual-design-contract.md) for hero beats) — the JSON is the
skeleton those hang on, not a replacement for judgment.

## Top-level shape

```json
{
  "edit_slug": "sample-project-full-polish-20260716",
  "source_sha256": "<64-hex of the source video>",
  "fps": 30,
  "declared_mix": {
    "intent": "One human sentence: the planned balance and why.",
    "modes_used": ["overlay", "presentation", "clean"],
    "dominant": "overlay",
    "single_mode": false,
    "single_mode_reason": null,
    "pace": "fast"
  },
  "sections": [
    { "id": "S1", "purpose": "cold open, orient the viewer", "start_s": 0.0, "end_s": 22.4, "beat_ids": ["b01", "b02"] }
  ],
  "beats": [
    {
      "id": "b01",
      "start_s": 0.0,
      "end_s": 6.2,
      "text": "verbatim words spoken in this beat",
      "spatial_mode": "clean",
      "presenter_role": "anchor",
      "is_effect_moment": false,
      "capabilities": [],
      "camera_template_id": null,
      "scarcity_class": 0,
      "reason": "open close and intimate — no treatment yet (N4)"
    },
    {
      "id": "b07",
      "start_s": 41.0,
      "end_s": 48.6,
      "text": "the claim that lands the section",
      "spatial_mode": "overlay",
      "presenter_role": "cutout",
      "is_effect_moment": true,
      "capabilities": ["masking", "on_screen_element", "camera_move", "caption"],
      "camera_template_id": "T2",
      "scarcity_class": 2,
      "reason": "emphasis push on the claim; element enters beside a masked presenter (video-09 register)"
    }
  ]
}
```

*(The block above is an illustrative **fragment** — `b01` and `b07` shown. A real plan lists
every beat in time order, and its `presentation` beats must actually appear for a
`modes_used` that includes `presentation` to pass the mode-mix check.)*

## Field definitions

**`declared_mix`** — the promise the mode-mix check holds the plan to (Option A, the project lead
2026-07-16):

- `intent` *(string, required)* — one human sentence stating the planned balance.
- `modes_used` *(array, required)* — every `spatial_mode` the plan will actually use.
- `dominant` *(enum, required)* — `overlay` \| `presentation` \| `clean`; the most-used mode.
- `single_mode` *(bool, required)* — `true` only if the director **deliberately** wants the
  whole video in one non-clean mode.
- `single_mode_reason` *(string \| null)* — **required non-empty** when `single_mode` is
  `true`; the story reason the video should not mix. `null` otherwise.
- `pace` *(enum, required)* — `fast` \| `medium` \| `slow`. Default is `fast` unless the
  material argues otherwise (the project lead preference, 2026-07-16).

**`beats[]`** — one entry per beat, in time order:

- `id`, `start_s`, `end_s`, `text` — identity and the verbatim words.
- `spatial_mode` *(enum, required)* — the family this beat renders in:
  - `clean` — footage with captions only, no added world; neutral, counts toward neither
    family in the mix test.
  - `overlay` — presenter-world: footage is the base, graphics sit behind/in front of the
    subject via the matte path, elements ride the words, camera travels between them.
  - `presentation` — full-frame designed state: a designed card / cinematic screen space
    where the presenter is demoted to an inset or absent.
- `presenter_role` *(enum)* — `anchor` \| `cutout` \| `framed_insert` \| `absent`.
- `is_effect_moment` *(bool, required)* — `true` if this beat gets any treatment worth a
  proxy preview. The preview/parallel workflow renders these; `clean`/untreated beats are
  not previewed.
- `capabilities` *(array)* — what the beat combines, from: `masking`, `on_screen_element`,
  `camera_move`, `caption`, `texture`, `generated_asset`, `full_frame_card`. Used by the
  "combine capabilities when the topic allows" default — a rich effect moment should not be
  a lone caption.
- `camera_template_id` *(string \| null)* — an **accepted N10 atom** (`T1`–`T4`) or `null`.
  `T5` (step-punch) is rejected and must never appear.
- `scarcity_class` *(int 0–4)* — intensity/scarcity class for the existing scarcity check.
- `reason` *(string, required for every effect moment)* — the semantic **or** rhythmic
  motivation (N7). An effect moment with no reason fails the plan check.
- `design` *(object, required for `render:"type_treatment"`)* — preserves the director's
  editorial intention through rendering:
  - `job` — `identity` \| `transformation` \| `thesis` \| `comparison` \| `evidence` \|
    `quote` \| `annotation` \| `utility` \| `atmosphere`;
  - `type_role` — `attention` \| `identity` \| `editorial` \| `annotation` \| `utility`;
  - `scale` — `support` \| `feature` \| `environmental`;
  - `depth` — `front` \| `rear` \| `mixed` \| `screen`;
  - `readability` — `full` \| `recoverable` \| `decorative`;
  - `edge_policy` — `contain` \| `intentional_crop`.

Identity, evidence, and utility jobs require `readability:"full"`. A semantic job may
never be decorative. `intentional_crop` is reserved for environmental, recoverable
typography and does not waive presenter-occlusion judgment. `depth:"mixed"` requires
explicit rear and front line pieces.

## What reads this file

- `check_mode_mix.py` (skill [`check-mode-mix`](../../skills/check-mode-mix/SKILL.md)) — the
  computable mode-mix gate; run at runbook **Stage 5** (early, before any render) and again
  at **Stage 7** against the final plan.
- The **preview/parallel** workflow — selects `is_effect_moment == true` beats to render as
  cheap proxies and hands each worker its beat spec plus the locked look.
- Existing plan checks (holds, scarcity, overlaps) can read the same structure over time.

Keep the JSON and the prose reasoning consistent; on any conflict the render follows the
JSON, because the JSON is what the checks and workers consume.

## Edit-data preflight

Before proxy rendering, run:

```bash
cd research/presenter-world-kit
node scripts/check-edit-data.mjs <edit>/beat-map.json <edit>/captions.json
```

The preflight fails malformed type-treatment contracts, semantic contradictions,
Devanagari, unsorted/overlapping caption timing, and impossible single-word spans. It
warns—without banning—three nearby beats that repeat the same treatment, type role,
scale, and depth.

## Render extension — designed `content` payloads (for the generic kit)

The fields above are the *plan* the checks read. To actually **render** a beat without an
executor re-deriving wording, each beat also carries a designed **`content`** payload and a
**`render`** renderer choice, consumed by the generic
[`presenter-world-kit`](../../research/presenter-world-kit/README.md)
(schema of record: `src/kit/types.ts`). This is what keeps a delegated executor (Codex, etc.)
from *inventing* the on-screen text — the director specifies it, the executor renders it.

- **`render`** — which generic renderer: `clean` \| `overlay_accent` \|
  `type_treatment` \| `pulse_list` \| `station_compare` \| `card`. `overlay_accent`
  remains valid for legacy plans; new role-aware typography uses `type_treatment`.
- **`content`** — the designed payload for that renderer: `kicker` / `title` / `subtitle`,
  `lines[]` (each `{text, tone: paper|accent|neg|meta, at, role?, layer?}`), `items[]`
  (`{n,text,at}` — N2 pulse), `stations{left,right}` (T4 comparison),
  `inset{fx,fy,k}` (**measured** face for a presentation inset — N3.1, never a blind
  offset), and `placement`. A type treatment also carries
  `treatment: identity_lockup|hero_field|thesis_build|editorial_note|support_overlay`.
- **`plate` / `cutout`** — the per-beat media asset basenames (cutout only for masked beats).
- **look tokens** live in a separate `look.json` **derived per video** via
  [`look-derivation-recipe.md`](look-derivation-recipe.md) — never hardcoded in a beat.

The plan-level `spatial_mode`/`camera_template_id`/`scarcity_class` stay the source of truth
for the gates; `render`/`content` are the presentation of the same decision. Keep them
consistent (e.g. `spatial_mode:"presentation"` ↔ `render:"card"`).
