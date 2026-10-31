# Presenter-world edit kit — the reusable render engine

One generic Remotion project that renders **any** presenter/talking-head edit from
**data only**. You never edit the kit's TSX per video — you supply three JSON files and
per-beat media assets, and render the single `FullVideo` composition. This is what makes
the look portable across topics/genres and across executors (Claude Code, Codex, etc.).

It is the runnable home of the [`compose-presenter-world`](../../skills/compose-presenter-world/SKILL.md)
skill's "author the whole video from a beat map" step. The stylistic *choices* are not
baked in — they arrive as **derived look tokens** (see
[`look-derivation-recipe.md`](../../docs/rulebook/look-derivation-recipe.md)).

## The data contract (what an executor fills — never the code)

```
public/edit/
  look.json        # LookTokens — DERIVED per video (accent + role-based type palette)
  beat-map.json    # EditPlan — beats + `design` intent + designed `content` payloads
  captions.json    # {words:[{t,e,w}]} word-synced, comp-relative to 0, Hinglish, ZERO Devanagari
  plates/<id>.mp4  # per-beat 1920x1080 plate segment (starts at 0), one per beat
  cutouts/<id>.mov # per-beat ProRes-4444 alpha cutout — ONLY for masked beats (presenter_role=cutout)
```

Types are the source of truth: [`src/kit/types.ts`](src/kit/types.ts).

### Generic renderers (pick per beat via `render`)
- `clean` — plate + captions only (cold open, reflective recovery, explanatory stretches).
- `overlay_accent` — masked/anchor presenter + a stacked text element (kicker/title/lines,
  each `tone` = paper|accent|neg, each with an arrival `at`). Optional
  `camera_template_id`. Retained for legacy beat maps.
- `type_treatment` — role-aware typography selected from a beat's communicative job:
  `identity_lockup`, `hero_field`, `thesis_build`, `editorial_note`, or
  `support_overlay`. The beat declares type role, scale, depth, readability, and edge
  policy; the look supplies the coherent per-video font palette.
- `pulse_list` — N2 accumulating numbered list beside a masked presenter (`items[].at` = onset).
- `station_compare` — T4 lr-phrase two-station comparison (`content.stations.left/right`).
- `card` — full-frame presentation state (term/quote/rules/closing); optional **measured**
  presenter `inset:{fx,fy,k}` (N3.1 — fx,fy are the measured face center, never a guess).

### Camera
Only the accepted N10 atoms `T1..T4` (from the canonical registry
`research/camera-templates/templates.json`, mirrored in `src/kit/templates.json`).
T5 is rejected. Executors set `camera_template_id`; they never hand-author leg schedules.
For contained typography, the kit intersects the visible world at setup, camera-leg
starts/midpoints/landings, and release, then lays necessary text inside that shared region.
This is separate from the plate boundary clamp.

### Typography intent

New type-treatment beats carry:

```json
{
  "design": {
    "job": "transformation",
    "type_role": "attention",
    "scale": "environmental",
    "depth": "rear",
    "readability": "recoverable",
    "edge_policy": "contain"
  },
  "render": "type_treatment",
  "content": {
    "treatment": "hero_field",
    "lines": [{"text": "HERO → ZERO", "at": 0.8}]
  }
}
```

The example demonstrates the data shape, not a reusable screenwriting template.
Identity/evidence/utility text must be fully readable. Mixed depth requires explicit
`layer:"rear"` and `layer:"front"` line pieces.

## Producing the per-beat assets (deterministic — from the source + analysis cache)
1. **Plate segments:** `ffmpeg -ss <start> -i <SOURCE> -t <len> -vf "fps=<fps>,scale=1920:1080:flags=lanczos" -an -c:v libx264 -crf 16 plates/<id>.mp4`. **Render/decode from the highest-res source (4K) so camera pushes stay lossless** — this is why the moves finally read as perceptible.
2. **Masks (masked beats only):** decode the window to `frame_%06d.png`, run the accepted RVM adapter (`skills/track-and-mask`), then `ffmpeg [plate][mask]alphamerge -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le cutouts/<id>.mov`.
3. **Face measurement for any inset (N3.1):** from the RVM mask head band, `fx = mean x of the top ~28% of mask rows`, `fy = mean y of that band`; put those in `content.inset`.
4. **Captions:** the Hinglish transcript (`romanize-hinglish`), absolute word times → `{t,e,w}`.

## Preflight

```bash
npm test
node scripts/check-edit-data.mjs public/edit/beat-map.json public/edit/captions.json
```

The edit-data preflight validates type-treatment intent, caption chronology and duration,
zero Devanagari, and local treatment repetition. Repetition is a warning for director
review; semantic contradictions and impossible timing are failures. The caption renderer
respects word end times and clears during silence.

## Render
```bash
# proxy (cheap preview of the effect windows): scale down, keep watermark
./node_modules/.bin/remotion render FullVideo out/proxy.mp4 --frames=<a-b> --scale=0.3333 --muted
# conform (whole video, full res): set proxy_watermark=false in beat-map.json first
./node_modules/.bin/remotion render FullVideo out/conform_noaudio.mp4 --muted --color-space=bt709
ffmpeg -y -i out/conform_noaudio.mp4 -i <SOURCE_AUDIO> -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 out/final.mp4
```
Use `./node_modules/.bin/remotion` directly (not `npx`, which can mis-resolve here).

## Rules this kit already enforces / expects
- **Mode-mix (gate #10):** the plan must mix `overlay`+`presentation` (run `check_mode_mix.py` on the source-schema beat map).
- **N9:** `captions.json` must have zero Devanagari (U+0900–U+097F).
- **N3.1:** every `inset` carries a measured `fx,fy` — never a blind offset.
- **N1/N2/N8:** holds 5–7s, lists pulse and clear, one thing changes at a time.
- **N7/N10:** camera only via T1–T4 registry atoms, motivated (semantic/rhythmic).
- **F14:** typography role and treatment follow the beat's communicative job.
- **Semantic text:** full/recoverable/decorative intent and contain/intentional-crop
  intent are explicit and independently verified.

## Validated
2026-07-18 on `representative long-form test`: all five renderers reproduce the
director-approved proxy look from data alone (see `out/_val_*.png`). Approved stylistic
direction by the project lead on the proxy review the same day.
