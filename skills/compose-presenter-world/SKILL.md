---
name: compose-presenter-world
description: ALWAYS invoke when placing text or graphics inside a presenter's scene — behind/in front of the subject, riding spoken words, or under camera motion. Do NOT hand-roll cv2/PIL/ffmpeg text compositing or blind fixed coordinates; elements are derived per footage from an alpha matte and a word-timestamped transcript with the face/mask measured first (rule N5), never picked from an asset library or placed on guessed pixels.
---

# Compose Presenter World

## Overview

Derive and render in-scene graphic elements for a talking-head clip: shapes that pass behind the subject's head and in front of their torso, text riding those shapes timed to spoken words, a camera pull with parallax, and designed-canvas page swaps. Builds on `skills/composite-alpha/SKILL.md` (layer stack) and `skills/track-and-mask/SKILL.md` (alpha master). This skill owns the *derivation method and motion mechanics*; what elements should exist and how they look are upstream (director/beat plan) and downstream (design pass) decisions.

## Inputs

- Presenter alpha master + background plate (the proven alpha-compositing contract: same raster/fps/frame count)
- Word-timestamped transcript JSON for the same time window (mlx_whisper; `frame = round(word.start × fps)`)
- A beat plan: which elements, bound to which words/windows, at which depth
- For designed typography: communicative job, type role, scale, depth, readability
  (`full|recoverable|decorative`), edge policy (`contain|intentional_crop`), and the
  reusable treatment relationship

## Workflow

1. **Measure the subject first (for precision, not for classification).** `ffmpeg -i cutout.mov -vf "select='eq(n\,N)',alphaextract" mask.png` at representative frames; read off head span, face center, shoulder line. This mask-measurement exists for the pixel-exact jobs vision can't do reliably — placement, occlusion, anti-doubling, and bounding the zoom to the real subject size. It is **not** how the shot is classified (a whole-frame vision read does that — see step 4). Author ALL geometry relative to these numbers — never blind canvas coordinates. Re-measure per clip; framing changes everything.
   - **This includes every inset, reframe, and aspect-change (N3.1).** A presentation-mode presenter inset, a punch-in crop, or any reframed window must be centered on the **measured** face (head-band centroid), never a fixed offset that assumes the subject is centered — talking heads are routinely off-center. Framing an inset on a blind offset is the same defect as authoring a rear element on blind coordinates. (Verified defect: representative long-form test 2026-07-18 inset framed the torso; fixed by measuring the head band.)
   - **Cheap for keep-out, matte only for occlusion (cost rule).** Placing text so it never crosses the face/head needs only the subject's *position*, not a silhouette — a lightweight face/head detector (e.g. an OpenCV face box) sampled a few frames per shot (shots come from `detect-shots`) or **unioned across the text's on-screen window** for a moving subject. That is milliseconds and needs **no** subject matting. Reserve the full alpha matte (`track-and-mask`/RVM — minutes, per-frame) for when text is placed **behind** the subject and the silhouette must actually occlude it. Never run matting merely to position a label or caption. This face keep-out is required for **all** on-screen text — plain captions and corner labels included, not only presenter-world elements — and text is never placed on blind fixed coordinates. If detection fails on a beat, fall back to a conservative center keep-out band rather than placing blind.
2. **Build the locked scene.** Plate and cutout are one physical scene: identical transforms every frame, each wrapped in its own `AbsoluteFill` (unwrapped `<Video>` collapses/renders empty in chromium-headless). Layer order: plate → rear graphics → cutout → front graphics; every layer absolutely positioned.
3. **Derive elements from the recipes** (combine freely; these compose):
   - *Depth-split curve:* one visual curve = two SVG paths split where it crosses the silhouette; upper path in the rear layer (head occludes it), lower in the front layer (crosses the torso).
   - *Text-on-path:* SVG `textPath`; author paths left→right or text flips; `pathLength={1000}` + `strokeDasharray={1000}` for exact draw-in/retract; word appears at its transcript frame.
   - *Rear field elements* (rows, grids, metaphor shapes): rear layer, spread wide enough to stay visible beside the subject; center region will be occluded. When the element carries words, decide whether they need a **full read** or may be **recoverable** through controlled occlusion. Ordinary side-label type hidden behind the presenter is not automatically an environmental composition; environmental type must be scaled and placed so the intended phrase survives the silhouette.
   - *Canvas page:* designed background in the background slot, swiped/cut in under the persistent cutout.
4. **Camera motion without breaking the scene or leaking boundaries.** 
   - *Parallax:* Root scale (center origin) on everything together. Parallax = extra scale on graphics layers only (`1 + (scale−1)×1.5`). NEVER transform plate or cutout independently — that renders a doubled subject.
   - *Station Travel:* Target positions (`cx`, `cy`) at scale `s` must be mathematically bounded to stay strictly within the original 1920x1080 bounds so the plate covers 100% of the screen.
     *   `cx` must satisfy: `960 / s <= cx <= 1920 - 960 / s`
     *   `cy` must satisfy: `540 / s <= cy <= 1080 - 540 / s`
   - *Framing Awareness — classify with vision, bound with the mask:* Two different jobs, two different tools.
     - **Classify (judgment) → a vision read of the whole frame.** The shot class (wide / medium / medium close-up / close-up) and composition — where the empty space is, what the vibe is — are best judged by a vision-capable model looking at the *whole frame*, not inferred from a silhouette bounding box (the full frame carries the context a silhouette discards). This decides *which* move and *how far* it may go.
     - **Bound (precision) → the measured subject size from the mask (step 1).** Vision is unreliable at exact, frame-stable pixel coordinates; the mask supplies them. The zoom ceiling is a **formula of the measured subject size, not a fixed number** — tighter shot → lower ceiling (a close-up softens almost immediately; a wide shot absorbs a big push). Placement room scales the same way: a wide shot leaves space beside the subject for rear elements; a close-up may force graphics smaller or to one side. Reference points, not a template: `s ≤ ~1.15–1.20` for a medium close-up, more for wider, near-zero for a close-up. Re-derive every limit from *this* clip — same formula, different output per frame.
     - **Efficiency:** the per-frame matte is needed anyway for occlusion and anti-doubling, so pull it **on demand** — when the chosen move crosses the subject or risks a leak/double. A move whose graphics stay fully beside the subject may not need it; vision plus the bounds math suffices.
   - *Semantic-text safe region:* Plate coverage and text coverage are different jobs.
     For `edge_policy:contain`, intersect the visible world rectangles at setup, every
     camera-leg start/midpoint/end, and release; place necessary text inside that shared
     region. `intentional_crop` requires an explicit environmental/recoverable contract
     and still receives a director-reviewed recovery frame.
5. **Render** per-beat windows plus the assembled timeline (`--muted --color-space=bt709`, hard-linked assets in `public/`); mux the source audio into the assembled cut.
6. **Verify on the deliverables, not the preview:**
   - frame counts/raster/fps exact; input SHA-256 unchanged;
   - boundary crops at silhouette contacts: rear elements occluded by hair/torso, front elements intact;
   - **single-silhouette check during camera motion** (the doubling check);
   - words inside their spoken windows; text upright;
   - **no edge leaks:** verify that the background plate completely covers the screen at all times during movement.
   - **semantic readability:** identity, evidence, and utility text remain fully readable;
     recoverable rear text still communicates the complete intended phrase;
   - **camera-state text containment:** inspect setup, arrival, every leg midpoint and
     landing, and release—not one representative still;
   - **caption release:** a caption clears after its last word ends instead of persisting
     through silence until the next onset. Run the generic kit's edit-data preflight to
     catch impossible ASR spans before render.

## Whole-video authoring — the generic kit

For authoring a *whole edit* (not just a one-off proof), this skill's runnable home is the
generic **[`presenter-world-kit`](../../research/presenter-world-kit/README.md)**: one
Remotion project that renders any presenter edit **from data** — `look.json` (derived per video
via [`look-derivation-recipe.md`](../../docs/rulebook/look-derivation-recipe.md)), a
`beat-map.json` with designed `content` payloads ([`beat-map-schema.md`](../../docs/rulebook/beat-map-schema.md)),
`captions.json`, and per-beat plate/cutout assets. Renderers: `clean` / `overlay_accent` /
`type_treatment` / `pulse_list` / `station_compare` / `card`.
`type_treatment` offers the generic relationships `identity_lockup`, `hero_field`,
`thesis_build`, `editorial_note`, and `support_overlay`; these are compositions, not
source-specific templates. Before rendering, run
`node scripts/check-edit-data.mjs <beat-map.json> <captions.json>` from the kit.
**Author videos by filling that data, not by writing per-video TSX** — the kit is generic
and stays generic; only the data changes. Validated 2026-07-18. The recipes below remain
the derivation method the kit's components implement.

## Accepted envelope

Proven 2026-07-16 on the accepted benchmark clip: 
*   **Discrete station hops** (20s proof in `CameraTravel.tsx` / `camera-travel.mp4`) — panning and scaling between three internal station layouts layered behind the presenter cutout.
*   **Continuous diagonal + lateral travel** (10s proof in `V09Grammar.tsx` / `v09-camera-travel.mp4`) — continuous diagonal push-in to Element A and lateral slide to Element B while zoomed, keeping all margins clean.

## Boundaries

- Elements are derived per footage from a beat plan — this skill must never ossify into a library of pre-built waveforms/ribbons (the project lead, 2026-07-14).
- Styling here is diagnostic; the design pass owns taste.
- Composition/motion code stays in the head session; delegate only scaffold/renders/batch verification (two delegated rounds failed on geometry & depth reasoning).
- Evidence and reference implementation: `research/presenter-world/`.
