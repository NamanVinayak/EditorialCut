# Camera-move template study — review package (2026-07-16)

Five treatments of the SAME 11.2s the prototype worked example excerpt (source 270.0–281.2s), built as
review compositions for the accepted N10 vocabulary. They are evidence reels, **not five
complete templates to replay verbatim**. Delta HD-B
(`docs/rulebook/review notes`) is the reason this
exists: the shipped full-video edit had two moves of scale 1.08 in five minutes —
imperceptible. Every move here clears the N10 perceptibility floor (≥0.10 scale
delta / ≥96px travel).

## Version 2 — corrected atomic review package

The corrected videos keep the same 11.2s excerpt but allow only the named camera
idea. The frame remains still after that idea closes:

| File | Atomic behavior |
|---|---|
| `variants/v2/T1-reveal-out-atomic.mp4` | One tight→wide reveal, then neutral through the end. |
| `variants/v2/T2-emphasis-push-atomic.mp4` | One push/hold/return, then neutral through the end. |
| `variants/v2/T3-right-reveal-atomic.mp4` | Open the right third, show the two labels, return, then neutral. |
| `variants/v2/T4-lr-phrase-atomic.mp4` | Neutral lead-in, left→right parallel phrase, return, then neutral. |

`templates.json` is the single schedule source. The four Remotion compositions read
their legs from it through `src/templateRegistry.ts`; handwritten duplicate schedules
fail verification. `step-punch` is recorded there as rejected, has no composition ID
or active legs, and is absent from `Root.tsx`.

Run the complete automatic gate with:

```bash
python3 research/camera-templates/verify_templates.py
```

Current evidence: 9/9 contract tests pass; the registry/active-composition check
passes; all four Version 2 files are 1920×1080, 30fps, 336 frames / 11.200s with
48kHz stereo audio. Fresh checkpoints under `variants/checks/v2/` were inspected:
all four remain neutral after their named action, T3's labels clear, and T4 has no
Version 1 opening reveal or final push.

**Status:** accepted by the project lead's moving-video review on 2026-07-16. T1–T4 are the
active N10 camera atoms; T5 remains rejected and non-selectable.

## Version 1 — the project lead's first-review disposition

| File | Verdict | What survives the review |
|---|---|---|
| `T1-reveal-out.mp4` | Keep core; refine | `reveal-out` is only the opening tight→wide action. The later push-in was useful review context but is **not** part of this template. |
| `T2-emphasis-push.mp4` | Keep core; refine | The motivated push-in works, and returning after the moment can close it. The later second push is a separate camera event, never an automatic tail. |
| `T3-right-reveal.mp4` | Positive candidate | the project lead likes the right-reveal direction: open the right third, place the contextual elements, release when that visual moment ends. |
| `T4-lr-phrase.mp4` | Positive candidate | the project lead likes the left/right phrase direction. Its linked left→right grammar is selected only for genuinely parallel clauses; the later final push is separate. |
| `T5-step-punch.mp4` | **Rejected** | the project lead hates step-punch. Keep the file only as review evidence; the move is non-selectable and must not enter N10. |

## N10 granularity learned from this review

- A named move is one atomic editorial action, not every camera leg shown later in
  its demonstration clip.
- A return to neutral may close the same action when the semantic moment ends.
- Any later push/reveal needs a separate template ID and separate semantic or rhythmic
  motivation; selecting one move never imports the rest of its review reel.
- Multi-leg sequence templates are allowed only for a matching discourse structure
  (for example, two parallel clauses for left→right), with unrelated lead-in/tail
  moves kept separate.
- A finished `lr-phrase` treatment defines two semantic stations, not just two camera
  coordinates: the first phrase gets its own relevant visual payload on one side,
  and the second phrase gets a different relevant payload on the other. The camera
  path and payload arrivals are planned together so the presenter inhabits a
  navigable world. If two meaningful destinations cannot be authored, use a simpler
  move or keep the shot locked.
- Rejected treatments remain evidence but are not available to the director.

All five share: `media/excerpt-270.0-281.2.mp4` (2560×1440 proxy cut from the
protected source — source untouched), word timings in `media/words.json`, the
head-session camera engine `composition/remotion/src/camera.tsx` (declarative
`CameraLeg[]` schedules, built-in boundary clamp — no move can expose canvas), and
locked numeric specs in `SPECS.md`.

Correction from head-session pixel verification: T5's original 0.985× whip
undershoot exposed black canvas at 7.94s because a below-1.0 viewport is larger
than the source. T5 now releases to 1.00×, and a render-level regression check at
`test_t5_no_edge_leak.py` protects the boundary.

The same review caught T3's original horizontal camera target moving in the
opposite direction: it seated the presenter right-of-frame and clipped both
pills. The corrected target seats him left and keeps the elements fully visible;
`test_t3_pills_fit.py` protects the right edge.

Process: specs + engine authored by the head session; five Sonnet sub-agents each
implemented one schedule (`composition/remotion/src/T1–T5.tsx`). T1, T2, and T5
rendered before Claude's safety-classifier outage; T3 and T4 were rendered during
session continuation. Self-check stills are in `variants/checks/`, with final
pixel verification performed by the head session.

The first review established atomicity and rejected T5. The second moving-video
review accepted all four corrected T1–T4 camera atoms. the project lead also clarified that a
future finished D4 use should add a different narration-relevant visual at each side;
the existing D4 remains a valid camera-only mechanics proof and was not rerendered.

## Version 1 technical verification

- Camera-source lint and TypeScript compile: PASS. The two unrelated copied scaffold
  compositions were removed; the full local `npm run lint` now checks only this study.
- Every final render: H.264, 1920×1080, 30fps, 336 video frames / 11.200s, AAC stereo
  48kHz audio. Full video+audio decode: PASS for all five.
- T3 right-edge regression: PASS (`test_t3_pills_fit.py`; near-white edge ratio
  `0.000` after correction, originally `0.128`).
- T5 boundary regression: PASS (`test_t5_no_edge_leak.py`; near-black top-edge ratio
  `0.021` after correction, originally `1.000`).
- Protected source SHA-256 remains the previously recorded
  `f1b4468ff8ea69fdefa29dd7b035625ffac78bc19942569e2128832ebd3f022c`.
- Pixel checkpoints were regenerated from the final renders and inspected for all
  five treatments. This verifies delivery correctness, not creative acceptance;
  N10 is accepted for T1–T4; T5 remains rejected.
