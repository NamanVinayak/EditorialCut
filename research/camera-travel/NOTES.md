# Camera-travel capability proof (rulebook N7) — 2026-07-15

**Watch:** `out/camera-travel.mp4` (20s, 1920×1080/30, with source speech audio).

Proves the station-travel grammar from the video-01 study on the accepted benchmark
window (Masterclass 270–290s), reusing the accepted RVM alpha master + plate from the
presenter-world slice (hard-linked, byte-identical — see inputs below).

## What it does (all camera moves are edit-side, on one rigid 2.5D world)

| Time | Spoken (Hindi) | Move |
|---|---|---|
| 0–2.6s | — | anchor: presenter full-frame, clean |
| 2.64s "एवरेज ऑडियंस" | travel LEFT + land close on **Station A** — a dot-crowd "AVERAGE AUDIENCE"; dots build staggered as camera arrives; label lands on the word (f95) |
| 8.44s "पसंद आएगा" | the crowd **pulses** (they like it) |
| 8.9s | return to anchor for "मेरे को फैमिली में इसलिए पसंद आएगा" |
| 12.14s "फिल्मेकर के लेंचे" | travel RIGHT to **Station B** — viewfinder lens ring draws in; label on the word (f385) |
| 15.56s "नॉर्मल ऑडियंस" | travel DOWN (the vertical move) to **Station C** — seats facing a screen; label on the word (f484) |
| 17.64s "शो अच्छा लगता" | return to anchor; rear "GOOD SHOW." chip lands beside his head on the word, exits ~1.9s later |

Hold budgets (N1/N2): A ≈ 6.2s, B ≈ 2.6s, C ≈ 1.4s, chip ≈ 1.9s — all within the
5–7s budget. First 2.6s clean (N4 spirit). Nothing crosses the face (N5).

## Mechanics (extends compose-presenter-world)

- One world root carries a translate+scale camera (`transformOrigin: 0 0`;
  `tx = 960 − cx·s`). Plate and cutout sit at world (0,0)–(1920,1080) with **no
  independent transforms** — the anti-doubling law holds by construction.
- Stations live on a paper-grid canvas surrounding the plate; at each station a
  ~70–90px sliver of the plate stays in view as the spatial connection.
- Travels are 20–26 frames, bezier(0.45,0.05,0.2,1); camera lands slightly closer
  (s 1.08–1.12) than anchor — the "land close" of the grammar.

## Verification (pixel-checked)

- 600/600 frames, 1920×1080, 30 fps exact.
- Contact sheet (2 fps) — full grammar readable.
- Mid-travel still — single presenter silhouette, no doubling.
- Arrival-sync still — dots mid-build, label just starting on its word onset.
- Late still — chip beside head, nothing crossing the face.
- Inputs byte-identical (hard links to the presenter-world/alpha-compositing assets).
- The reviewed verification stills contained source footage, so they are not
  shipped with the repo. Re-render and re-extract frames to reproduce them.

## Status

Mechanics proven for **video-01's grammar** (discrete station hops: anchor → travel
to station → return); awaiting the project lead's eye on the render. Styling is diagnostic
(concept-first rule) — the design pass owns taste. If accepted, N7's execution gate
lifts and the skill note goes into `skills/compose-presenter-world/SKILL.md`'s
accepted envelope.

**Video-09's grammar** (continuous diagonal push-in + lateral slide, with elements
behind the presenter) is a separate proof — see `v09-grammar/` when it exists.
The previous understanding ("morph-and-accumulate with static camera") was
corrected on 2026-07-16; both videos use camera travel, just different patterns.
