# Camera-move template study — five treatments of one excerpt (2026-07-16)

Purpose: document the accepted N10 camera-move vocabulary through contrasting,
watchable treatments of the SAME 11.2s excerpt and preserve the review evidence
(delta HD-B in `docs/rulebook/review notes`).

## Review outcome — these schedules are evidence, not reusable wholes

the project lead's first review established that the complete 11.2s schedules below must never
be copied as single templates. The candidate vocabulary is atomic:

- `reveal-out`: T1 leg 1 only. T1's later push is a separate event.
- `emphasis-push`: T2's push/hold and motivated return (legs 1–2). T2 leg 3 is a
  separate event.
- `right-reveal`: positive refinement candidate; open space, fill it, then release
  when that visual moment closes.
- `lr-phrase`: positive sequence candidate for a genuinely matching parallel-clause
  grammar. Version 2 uses only Version 1 legs 2–4; the opening reveal (leg 1) and
  final push (leg 5) are both excluded.
- `step-punch`: **rejected**. T5 remains only as evidence of the killed direction.

Every independently motivated camera event must receive its own template ID in the
edit plan. Selecting an ID never appends other legs from this review composition.

## Version 2 source of truth and active compositions

The schedules below document the Version 1 review reels. They are intentionally
preserved as historical evidence. The current T1–T4 Remotion components do **not**
copy these tables: they read the corrected schedules from `templates.json`.

| Candidate ID | Active composition | Atomic leg count | Version 2 correction |
|---|---|---:|---|
| `reveal-out` | `N10RevealOut` | 1 | Removed the later payoff push. |
| `emphasis-push` | `N10EmphasisPush` | 2 | Kept push + motivated return; removed the later second push. |
| `right-reveal` | `N10RightReveal` | 2 | Kept reveal + return; no later camera event. |
| `lr-phrase` | `N10LeftRightPhrase` | 3 | Kept left→right→neutral only; removed opening reveal and final push. |
| `step-punch` | none | 0 | Rejected and blocked from active rendering. |

`verify_templates.py` enforces this exact set, the leg counts, readable movement
floor, scale safety, per-leg editorial reasons, registry-only component bindings,
T5 rejection, and the four Version 2 media contracts.

## Version 2 acceptance and future spatial-station direction

the project lead accepted all four corrected T1–T4 camera atoms in moving-video review on
2026-07-16. T5 remains rejected.

The D4 file is intentionally a camera-only mechanics proof. In a finished editorial
use, `lr-phrase` must travel between two meaningful visual stations: the first phrase
gets a relevant text, evidence item, contextual graphic, or sourced/generated/derived
asset on the first side; the second phrase gets a different relevant payload on the
other side. Each payload arrives with its phrase, shares scene space with the stable
presenter anchor, and clears or resolves with the comparison. If two accurate
destinations cannot be authored, do not select `lr-phrase` merely for motion.

## Shared facts (all treatments)

- Excerpt: `composition/remotion/public/excerpt.mp4` — a sample talking-head source excerpt
  270.0–281.2s, 2560×1440, 30fps, 11.200s, audio included. One continuous
  talking-head shot, presenter centered. **Face anchor in 1920×1080 logical
  coords: (985, 400).** Frame center: (960, 540).
- Word timings (comp-relative seconds, from `media/words.json`):
  - `open` 0.44–1.58 — "sample opening phrase"
  - `emph` 2.64–3.88 — "key emphasis words"
  - `clauseA` 4.36–5.94 — "first supporting clause"
  - `clauseB` 5.94–7.74 — "second supporting clause"
  - `payoff` 7.74–8.88 — "payoff line"
  - `turn` 8.98–11.10 — "closing turn phrase"
- Composition: 1920×1080, 30fps, 336 frames (already registered in Root.tsx).
- **Perceptibility floor (the point of this whole exercise): every deliberate
  move changes scale by ≥ 0.10 (prefer ≥ 0.12) or travels cx by ≥ 5% of frame
  width (≥ 96px). No micro-moves.**
- All camera motion goes through `src/camera.tsx` (`CameraViewport` + a
  `CameraLeg[]` schedule). Do NOT write your own transform math. Legs are
  sorted, non-overlapping; the camera holds the last leg's end state between
  legs; the boundary clamp is built in.
- Audio must be present in the render (do not mute the OffthreadVideo).
- Elements (T3 only) are placed INSIDE `CameraViewport` — they are in-scene,
  the camera move affects them.

## Version 1 delivery contract (historical)

1. Edit ONLY your own `src/T<n>.tsx`. Never touch `camera.tsx`, `Root.tsx`,
   other treatment files, `package.json`, or anything outside
   `research/camera-templates/`.
2. Render from `composition/remotion/`:
   `npx remotion render T<n> ../../variants/T<n>-<slug>.mp4 --concurrency=3`
3. Self-verify: extract the checkpoint stills listed in your section with
   ffmpeg (`-ss <t> -frames:v 1`) into `variants/checks/T<n>/`, LOOK at each
   image, and confirm the expected framing. If a checkpoint fails, fix your
   schedule and re-render before reporting.
4. Report back: output path, per-checkpoint PASS/FAIL with one line of what
   you saw, and any deviation from spec with its reason.

---

## T1 `reveal-out` — open tight, breathe out (slug: `reveal-out`)

The video begins already punched in on the face and relaxes to full frame as
the opening phrase completes; one clean push returns on the payoff.

| leg | t0 → t1 | scale | cx | cy | ease |
|---|---|---|---|---|---|
| 1 | 0.00 → 2.60 | 1.25 → 1.00 | 985 → 960 | 400 → 540 | easeOut |
| 2 | 7.74 → 8.88 | 1.00 → 1.12 | 960 → 985 | 540 → 430 | standard |

Checkpoints: 0.0s (tight on face, ~1.25×), 2.8s (full frame), 7.5s (still
full frame), 8.9s (pushed ~1.12× toward face), 11.0s (holds the push).

## T2 `emphasis-push` — push in on the key phrase, release as an event (slug: `emphasis-push`)

| leg | t0 → t1 | scale | cx | cy | ease |
|---|---|---|---|---|---|
| 1 | 2.64 → 3.88 | 1.00 → 1.18 | 960 → 985 | 540 → 420 | standard |
| 2 | 7.74 → 8.14 | 1.18 → 1.00 | 985 → 960 | 420 → 540 | easeOut |
| 3 | 8.98 → 9.60 | 1.00 → 1.12 | 960 → 985 | 540 → 430 | standard |

Checkpoints: 0.5s (full frame), 4.0s (pushed 1.18×), 7.5s (still pushed —
the hold is deliberate), 8.3s (released to full), 10.5s (second push held).

## T3 `right-reveal` — camera opens space, an element fills it (slug: `right-reveal`)

Camera drifts so the presenter sits left-of-frame, opening the right third;
two pills land there on the parallel clauses; everything releases on payoff.

| leg | t0 → t1 | scale | cx | cy | ease |
|---|---|---|---|---|---|
| 1 | 2.40 → 3.60 | 1.00 → 1.14 | 960 → 1075 | 540 → 480 | standard |
| 2 | 7.74 → 8.60 | 1.14 → 1.00 | 1075 → 960 | 480 → 540 | easeOut |

Elements (inside CameraViewport, scene coords):
- Pill 1 "FILMMAKING ✗": enters at 4.36 — slides in from +60px right with
  fade, 0.35s easeOut. Center ≈ (1530, 430), rounded-full, white background
  (#F7F4EE), dark text (#1A1A1A), ~44px system-ui semibold, padding ~18px 36px.
  Keep the pill's right edge ≤ x 1680 (stays inside the drifted window).
- Pill 2 "SCREEN DIRECTING ✗": same style, enters at 5.94, center ≈ (1530, 560).
- Both exit at 7.74: slide +40px right + fade out, 0.30s.

Checkpoints: 1.0s (neutral full frame), 4.0s (presenter left, right third
open, no pill yet at 4.0 — pill 1 lands at 4.36), 5.0s (pill 1 visible), 7.0s
(both pills visible), 8.8s (pills gone, frame back to neutral).

Correction after frame-level verification: the original `cx 845` target moved
the scene in the opposite direction, placing the presenter right-of-frame and
clipping both pills. `cx 1075` produces the intended left-seated presenter and
keeps the right-side elements inside the viewport.

## T4 `lr-phrase` — the choreographed sequence: out → left → right → return (slug: `lr-phrase`)

the project lead's worked example. The two parallel clauses get mirrored framings.

| leg | t0 → t1 | scale | cx | cy | ease |
|---|---|---|---|---|---|
| 1 | 0.00 → 1.00 | 1.15 → 1.00 | 960 → 960 | 540 → 540 | easeOut |
| 2 | 4.36 → 4.90 | 1.00 → 1.15 | 960 → 860 | 540 → 470 | standard |
| 3 | 5.94 → 6.50 | 1.15 → 1.15 | 860 → 1060 | 470 → 470 | standard |
| 4 | 7.74 → 8.50 | 1.15 → 1.00 | 1060 → 960 | 470 → 540 | easeOut |
| 5 | 8.98 → 9.58 | 1.00 → 1.10 | 960 → 985 | 540 → 430 | standard |

Checkpoints: 0.0s (slightly tight), 1.2s (settled full), 5.4s (zoomed,
frame favors LEFT), 7.0s (zoomed, frame favors RIGHT — mirror of 5.4), 8.7s
(neutral), 10.5s (final gentle push held).

## T5 `step-punch` — instant punch ladder on the list rhythm, whip release (slug: `step-punch`)

**Review status: REJECTED — do not add this treatment to N10 or select it in an edit.**

Punches are near-instant (2 frames ≈ 0.067s, ease `snap`). The release is a
fast whip back to the full-frame boundary.

| leg | t0 → t1 | scale | cx | cy | ease |
|---|---|---|---|---|---|
| 1 | 2.640 → 2.707 | 1.00 → 1.12 | 960 → 970 | 540 → 500 | snap |
| 2 | 4.360 → 4.427 | 1.12 → 1.24 | 970 → 980 | 500 → 450 | snap |
| 3 | 5.940 → 6.007 | 1.24 → 1.36 | 980 → 985 | 450 → 410 | snap |
| 4 | 7.740 → 7.940 | 1.36 → 1.00 | 985 → 960 | 410 → 540 | easeOut |
| 5 | 8.980 → 9.047 | 1.00 → 1.15 | 960 → 985 | 540 → 430 | snap |

Correction after frame-level verification: the originally specified 0.985×
undershoot exposed black canvas at 7.94s. A viewport wider than its source cannot
be made boundary-safe by center clamping, so T5 now releases to exactly 1.00× and
the shared engine enforces 1.00× as its minimum scale.

Checkpoints: 2.0s (neutral), 3.0s (step 1 held ~1.12×), 5.0s (step 2 held
~1.24×), 7.0s (step 3 held ~1.36×, tight on face), 8.5s (released neutral),
10.0s (final punch held ~1.15×).
