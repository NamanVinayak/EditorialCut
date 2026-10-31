---
title: Texture Language
type: rulebook
status: accepted-v1
updated: 2026-07-23
---

# Texture Language — when material tells the story

Texture is material storytelling, not generic dirt. The physical world is full of
imperfection, and eyes trust imperfection: a flat digital graphic reads as generic,
while the same graphic under a restrained material treatment reads as crafted,
premium, and emotionally present. This document is the judgment layer for the
raw materials shipped in [`assets/foundation-textures-v1/`](../../assets/foundation-textures-v1/README.md)
— that README covers blend-mode mechanics; this file covers when and why.

These rules were derived from the same private 24-video reference study as the
Beat-to-Primitive Rulebook. The study itself is not shipped; the rules are.

## The three laws

1. **Scarcity.** Texture earns its emotional impact through strategic rarity.
   A texture treatment is a scoped move on beats that justify it — never a
   global filter across the whole edit. If every scene is textured, no scene is.
2. **Stationary in screen space.** Overlay textures (halftone, grain, paper
   fiber, dust) stay fixed to the screen, not to the content. A texture that
   rotates or translates with a camera move breaks the print illusion and reads
   as a sticker. Reject any composite where the texture travels.
3. **Motion textures must live.** Grain, dust, and scratches must animate or
   re-randomize at frame rate. A static grain still held over moving footage
   reads instantly as fake. (The motion files in the foundation pack exist for
   exactly this reason — loop them, never freeze-frame them.)

## When to reach for texture

| Story context | Treatment | Why it works |
| --- | --- | --- |
| Archival, historical, or documentary assets (maps, old photos, collage) | Halftone or print grain at 5–6% opacity, optionally with stepped motion (see below) | Simulates vintage print reproduction; binds mixed-source assets into one tactile space |
| Documents, articles, screenshots, "paper" UI | The four-layer paper stack (below) | Turns a sterile white box into a physical sheet |
| Footage or montage that wants film memory | Grain / dust-scratches / flicker from the motion pack, briefly, on the beats that carry the feeling | Vintage as an accent, not a costume |
| Flat vector / comic / poster graphics that feel weightless | Paper or canvas noise at low opacity; optional chromatic aberration at high-contrast edges | Restores material weight; playful print misregistration |
| A transformation or reveal beat | Ink/stain/scratch reveal mattes as wipes or masks | The material itself performs the story event |

If a beat does not fit one of these contexts, the default is **no texture**.
Clean is a valid material language.

## The taxonomy

Sixteen texture families recur across the reference study: halftone, grain,
noise, grunge, paper, crumpled, dust, scratches, concrete, canvas, ink, paint,
smoke, marble, wood, fabric. The foundation pack ships starter plates for
paper, crumpled, fabric, ink, grain, dust/scratches, flicker, and light leaks.
The remaining families are derived or sourced per-edit under the Visual Design
Contract — they are contexts to recognize, not files to hoard.

## Application mechanics

- **Blend direction:** dark-on-light textures (halftone, ink, stains) composite
  in Multiply; light-on-dark textures (dust, scratches, leaks) composite in
  Screen or Add. The pack README's table carries the per-family bands.
- **Opacity bands:** pulp-fiber and subtle print grain live at roughly 5–6%;
  deliberate print overlays may reach 40%. Above ~40% the texture overpowers
  the underlying color and the treatment fails review.
- **Halftone scales with luminance.** Dot size must respond to the underlying
  image brightness, not sit as a uniform grid. A static uniform dot grid is the
  most common tell of a lazy halftone.
- **The four-layer paper stack:** (1) compress highlights so nothing sits at
  pure white — maximum brightness around 230/255 kills the digital glow;
  (2) map a warm eggshell tint into the paper tone; (3) overlay high-frequency
  fiber noise at 5–6%; (4) hold the paper layer at ~95% opacity so background
  elements bleed faintly through, the way real paper is slightly translucent.
- **Stepped motion pairing:** when texture is simulating stop-motion print
  collage, step the treated elements to roughly 8–12 fps. Above ~15 fps the
  stop-motion feel dissolves; below ~6 fps the motion becomes unwatchable.
  The step applies to the treated elements as a group — one shared puppet
  rhythm, not per-element rates.
- **Chromatic aberration:** 2–4 px of channel offset at high-contrast edges
  reads as print misregistration; beyond ~10 px it reads as damage and hurts
  legibility. Never run aberration through body text.
- **Sound completes the material.** Paper that slides, flips, or curls wants a
  paper foley cue on the same frame. Silent material motion breaks the illusion
  the texture just built.

## Review proof

The standard review artifact for any texture treatment is a **before/after
split** — a wipe or slider that divides the untreated and treated states of the
same frame. Verify at 100% zoom. Reject when:

- the texture moves with the camera instead of the screen;
- a motion texture is frozen;
- opacity exceeds its band, or texture crosses a face at full strength;
- halftone dots ignore luminance;
- text legibility drops (aberration, grid, or crease across type);
- the same texture treatment has already appeared on nearby beats without a
  story reason — the scarcity law outranks the mechanics.

## Relationship to the locked look

Texture treatments are **treatment moves on treated beats** under the
[locked-look contract](locked-look-contract.md): they never alter the color of
untreated source footage, and they require the same treated-versus-clean
authority as any other effect. The foundation pack's existence is capability,
not permission.
