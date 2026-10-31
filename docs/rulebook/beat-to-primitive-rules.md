---
title: Beat-to-Primitive Rulebook
type: rulebook
status: accepted-v1 + accepted amendments through 2026-07-19
updated: 2026-07-19 (N11 explicit color authority)
primary_taste_source: private 24-video taste study (rules derived from it; study not shipped)
mechanic_sources: private per-video mechanic studies, video-01 through video-24 (not shipped)
delta_source: private full-video review deltas, 2026-07-16 (not shipped)
---

# Beat-to-Primitive Rulebook — accepted v1

## What changed from draft v1

Draft v1 began with effects. This version begins with the audience feeling and
storytelling beat that justify an effect.

The useful mechanics from draft v1 remain, but overlapping rules have been merged,
weak assumptions have been demoted, and every buildable rule now states its purpose,
trigger, move, intensity, restraint, required inputs, executing skill, fallback, and
first-person taste provenance.

Evidence priority is:

1. the project lead's accepted 24-video taste map;
3. verified mechanics in the canonical video documents;
4. accepted capability tests;
5. clearly labelled agent inference.

Provenance markers such as `V07` or `video-07` cite entries in the private
reference study these rules were derived from. That study is personal reference
material and is not shipped; the derived rules in this document are its public
form.

the project lead accepted this rulebook on 2026-07-15. It is the governing creative input
for Phase 3's creative-director instructions and the later beat-map planner.

## Target and boundary

Version 1 receives a supplied rough cut and adds a modern polish pass. It does not
re-cut the underlying edit. It may add captions, graphics, presenter-world treatments,
texture, audio treatment, and supplementary insert sequences, but it must preserve
the source cut unless the project lead later expands that scope.

Capability knowledge is a derivation recipe for unseen footage, not a shelf of copied
reference graphics. A ribbon, crossroads, book icon, red ADHD frame, purple palette,
Einstein portrait, or source creator's layout is a disposable example.

This does not mean storing no assets. Reusable material plates such as paper scans,
fabric, ink, grain, dust, scratches, flicker, and light leaks are available in the
completed `../../assets/foundation-textures-v1/` pack, applied under the judgment
rules in [`texture-language.md`](texture-language.md). Story-specific semantic
visuals are still derived, authored, generated, adapted, or sourced for the current
edit.

Video 08
produces no creative-treatment rule. Its durable contribution is system architecture:
real-footage planning and assembly remain separate from replaceable rendering engines.
That belongs in the future assembly harness rather than being misrepresented as
visual taste. Mechanic provenance: video-08.md.

## Engine and reuse policy

The editing agent is the control layer, not a new rendering engine. Skills describe
the editing job, required inputs, procedure, and acceptance criteria. Existing tools
execute that job wherever they are already strongest.

### Reuse-first routing order

1. **Use the accepted capability's proven execution path first.** Do not port a
   working Remotion or FFmpeg capability merely to satisfy a default preference.
2. **Check existing skills, HyperFrames catalog/registry components, and project
   implementations before authoring anything new.**
3. **Use HyperFrames as the default for new motion-design composition:** typography,
   graphic cards, caption layouts, section canvases, and ordinary designed motion.
4. **Use Remotion as the footage/compositing specialist:** alpha-video layers,
   presenter-world depth, video-heavy timelines, complex per-frame behavior, or an
   already accepted Remotion implementation.
5. **Use FFmpeg for native media operations:** audio processing, deterministic
   filters, simple composites, transcodes, muxing, and final assembly.
6. **Reuse Video Use selectively as orchestration knowledge:** real-footage workflow,
   timeline/assembly patterns, caption logic, explicitly authorized grading logic, and
   rendered-output review. Do not inherit its automatic recutting in v1, and never
   invoke its grading path without `color_authority: explicit`.
7. **Write custom code only when the approved treatment cannot be expressed safely by
   an existing component, skill, or engine path.** Record why reuse was insufficient.

These are defaults, not lock-in. Engine choice must preserve the approved creative
intention, and outputs should use portable contracts—timing JSON, masks/alpha media,
ordinary image/video assets, audio stems, and rendered clips—so a different engine can
replace the first one later.

The creative director normally requests a capability rather than a renderer. A future
beat-map entry should carry:

- capability identifier;
- preferred engine set to auto unless a real constraint exists;
- engine constraints such as alpha, cursor data, or required component;
- required inputs and asset brief;
- fallback capability or reduced treatment.

The Phase 5 assembly harness owns the executable engine router. Individual rules below
continue to name the accepted skill/capability; they do not authorize rebuilding that
capability from scratch.

---

## Part I — Creative constitution

These principles outrank every individual rule.

### C1 — Preserve the feeling, not the example

Different content should receive different visuals. First identify what the audience
must feel at the beat—scope, alarm, pressure, clarity, curiosity, proof, intimacy,
relief, importance, or conclusion—then derive an equivalent treatment for the new
story. This is the central Video 19 principle.

### C2 — Make the presenter and graphics one designed world

When a presenter is visible, type, backgrounds, evidence, camera behavior, and
foreground accents should feel spatially related to that person. Prefer integrated
depth and shared composition over stickers placed on top of footage.

### C3 — Motivate movement through narration

A push, pull, pan, canvas change, typography arrival, or graphic reveal needs a spoken
or emotional reason. Movement should arrive with the relevant word or thought change,
not because the screen has been quiet for an arbitrary number of seconds.

### C4 — Elevate moments, not sentences

Routine explanation can remain clean. Important claims, turns, emotional peaks,
comparisons, difficult ideas, and conclusions deserve treatment. Decorating every
sentence flattens the story because nothing remains special.

### C5 — Build and release intensity

Editing density must rise and fall. A high-energy passage needs a comprehension hold
or clean recovery state. Premium editing is controlled editing, not maximum activity.

### C6 — Keep one grammar per section

A section should share a palette, typography system, texture family, motion character,
caption behavior, and a limited set of recurring moves. Variety should come from
changing hierarchy inside that grammar, not importing a new visual universe for every
line.

### C7 — Scarcity protects impact

Climax captions, full-frame thesis words, dramatic poster treatments, fragmentation,
and aggressive flashes lose power when repeated casually. The director must budget
high-impact moves before rendering.

### C8 — Know when clean footage is stronger

Leaving a good shot alone is a valid creative decision. If a treatment adds no clearer
meaning, emotion, evidence, orientation, or rhythm, do not place it.

### C9 — Derive visuals for the current footage

The director specifies the communicative need and visual relationship. Execution may
author, generate, adapt, download, or reuse an appropriate material, but it should not
select a worked example merely because that example exists in the reference library.

### C10 — Add; do not recut in v1

Beat and shot analysis may guide placement, but the supplied rough cut remains intact.
Downbeats can time new graphic or insert events; they do not authorize changing the
underlying editorial cut.

### C11 — Treat technical terms as intent clues

the project lead's terms such as “dolly zoom” may be approximate. Preserve the perceived
filmmaking intention—camera-like movement toward meaning—rather than enforcing a
narrow technical label.

### C12 — Verify mechanics without overriding taste

Canonical evidence may correct what physically happened, but it cannot overwrite why
the project lead saved the reference. Keep stated taste, verified mechanics, and agent inference
separate.

---

## Part II — Director gate before selecting a rule

Before placing any treatment, answer:

1. What is this beat doing: hook, claim, proof, explanation, pressure, comparison,
   transition, emotional peak, resolution, or conclusion?
2. What should the audience feel?
3. Is this moment important enough to deserve treatment?
4. What visual grammar already governs this section?
5. Which rule communicates the beat with the least unnecessary machinery?
6. Has a similar high-impact move appeared too recently?
7. Are the required footage, matte, timing, evidence, and assets actually available?

If these answers are weak, keep the footage clean or use a lower-intensity fallback.

### Intensity classes

| Class | Meaning | Typical use |
|---|---|---|
| 0 — clean | no added visual treatment | breathing space, good performance, comprehension |
| 1 — support | captions, quiet evidence, mild layout help | routine explanation |
| 2 — emphasis | designed keyword, receipt, gentle camera move | important claim or definition |
| 3 — transformation | world swap, poster state, fragmentation | major turn or emotional peak |
| 4 — scarcity | climax takeover or final thesis frame | normally once per piece |

---

## Part III — Buildable-now rules

“Buildable now” means an accepted project capability can execute the mechanics. Asset
choice and creative approval may still require the director.

### A. Presenter-world and narration-led composition

### R1 — Assign depth by communicative role

- **Purpose / feeling:** Make the presenter and graphics feel physically integrated.
- **Trigger:** A presenter is visible and a narration-relevant graphic is needed.
- **Move:** Put large environmental words or metaphor shapes behind the presenter;
  keep captions, small labels, and applied badges in front. Assign depth per element,
  not through one global stack.
- **Semantic depth contract:** names, evidence, utility text, and any claim the
  audience must read receive `readability: full`. Environmental phrases may receive
  `readability: recoverable` when the presenter hides part of the letterforms but the
  intended phrase remains immediately understandable. Only non-semantic atmosphere may
  be `decorative`.
- **Settings:** Background plate → rear graphics → presenter alpha → front captions
  and accents. A shape may split around the silhouette when the composition needs it.
- **Restraint:** Do not force rear placement when occlusion hides the meaning or when
  the matte edge is unreliable. Presenter occlusion and camera-edge cropping are two
  separate decisions; neither authorizes the other.
- **Inputs / execution:** Presenter footage, RVM matte, timed graphic; track-and-mask
  + composite-alpha, optionally compose-presenter-world.
- **Fallback:** Move the graphic into clean negative space in front, reduce scale, and
  preserve readability.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V01, V07, V09, V19. Mechanics video-01, video-07, video-09, video-19.

### R2 — Promote only meaningful words into designed typography

- **Purpose / feeling:** Give a thesis, definition, or emotional keyword more weight
  than routine captions.
- **Trigger:** A word or short phrase carries the beat's central meaning.
- **Move:** Replace or supplement the normal caption with designed typography that
  arrives on the spoken word. It may occupy negative space, ride a path, or behave as
  an environmental object.
- **Settings:** Word-timestamp arrival; hold for comprehension; use section typography
  roles and palette.
- **Restraint:** Do not promote every noun. Ordinary speech stays in the base caption
  system.
- **Inputs / execution:** Word timestamps, selected phrase, layout and type tokens;
  composite-alpha or compose-presenter-world.
- **Fallback:** Highlight the word within the normal caption without changing the
  whole composition.
- **Status:** ✅ Buildable now through the generic presenter-world kit's `type_treatment`
  renderer; role-aware selection is F14.
- **Provenance:** Taste V01, V09, V19. Mechanics video-01, video-09, video-19.

### R3 — Use scale and world state to express emotional weight

- **Purpose / feeling:** Make scope, alarm, pressure, or trivial interruption felt
  spatially.
- **Trigger:** The beat has a clear emotional category and one dominant word.
- **Move:** Change the relationship between person, word, and field: make the person
  small under a universal claim, use a high-contrast field for alarm, or make a
  trivial distraction comically oversized.
- **Settings:** One dominant word; one clear hierarchy; intensity class 2–3.
- **Typography:** Environmental scale must be genuinely environmental. Do not take an
  ordinary side-label composition, place it behind the presenter, and call the
  resulting missing letters intentional.
- **Restraint:** Do not use giant type merely because a word is short. Avoid repeating
  the same field color and scale trick within the same section.
- **Inputs / execution:** Beat role, keyword, presenter matte or crop, palette;
  compose-presenter-world + composite-alpha.
- **Fallback:** Use a smaller emphasis word beside the presenter without changing the
  entire world.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V19. Mechanics video-19.

### R4 — Move the camera toward meaning

- **Purpose / feeling:** Carry the viewer into the thought rather than apply a generic
  zoom.
- **Trigger:** Narration names or reveals a visual destination already placed in the
  composition.
- **Move:** Start a virtual push, pull, or lateral move early enough that the camera
  arrives at the destination on the payoff word. A reveal-synced pull may begin just
  before the graphic arrives. Quiet diagrams may receive only a slow drift.
- **Settings:** One stable anchor; readable landing hold; motion character consistent
  with the section.
- **Restraint:** Use pronounced moves sparingly. Do not move if there is no semantic
  destination or if movement hides the relationship being explained.
- **Inputs / execution:** Word timestamps, station geometry, target and hold duration;
  compose-presenter-world.
- **Fallback:** Keep the camera locked and animate only the destination's emphasis.
- **Status:** ✅ Buildable now at accepted mild-camera level. **Station travel
  un-parked 2026-07-15:** the project lead's prototype review named the real edit need the
  2026-07-14 deferral was waiting for — see rule N7 and the private camera-travel
  study (not shipped).
  Large travel moves remain gated on the capability proof at
  `../../research/camera-travel/`.
- **Provenance:** Taste V01, V09. Mechanics video-01, video-02, video-09.

### R5 — Change the card world while preserving the human anchor

- **Purpose / feeling:** Create rapid freshness without making the viewer lose the
  presenter.
- **Trigger:** Several consecutive narration beats need distinct graphic cards.
- **Move:** Swap background, headline treatment, and accent family together at each
  beat while keeping the presenter matte treatment stable.
- **Settings:** Changes follow narration beats, not a fixed timer; one palette family
  or section grammar connects the cards.
- **Restraint:** Do not use for a reflective passage that needs continuity or when the
  changing worlds have no clear relationship to the words.
- **Inputs / execution:** Beat map, presenter matte, per-card design tokens;
  track-and-mask + composite-alpha.
- **Fallback:** Keep one background and change only the headline or one supporting
  element.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V07, V20. Mechanics video-07, video-20.

### R6 — Use a full-canvas change only for a structural turn

- **Purpose / feeling:** Make the audience feel a chapter or mode change.
- **Trigger:** A genuine turning point, chapter title, or change in argumentative mode.
- **Move:** Replace the complete canvas quickly; optionally demote live footage into a
  framed inset during the title beat, then restore the established world.
- **Settings:** Fast gear-shift rather than a slow decorative fade; intensity class 2–3.
- **Restraint:** Do not use for routine sentences or as a substitute for clear story
  structure.
- **Inputs / execution:** Section boundary, alternate canvas, optional inset;
  compose-presenter-world or render-geometric-masks.
- **Fallback:** Change the section title, palette accent, or framing without replacing
  the complete background.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V09, V19. Mechanics video-09, video-19.

### R7 — Hold one view stable while a spoken list changes around it

- **Purpose / feeling:** Make pressure, accumulation, or comparison feel persistent
  rather than chaotic.
- **Trigger:** Narration lists related causes, features, pressures, or alternatives.
- **Move:** Hold one presenter framing and section palette while changing exactly one
  main word and one supporting background element per list item.
- **Settings:** Word-synced item changes; stable person and camera; clear reset after
  the list.
- **Restraint:** Do not change camera, palette, type family, and background geometry
  simultaneously for every item.
- **Inputs / execution:** List items with word timestamps, one source view, item
  graphics; compose-presenter-world.
- **Fallback:** Keep the background fixed and replace only the keyword.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V19. Mechanics video-19.

### R8 — Adapt mixed media without breaking the section grid

- **Purpose / feeling:** Make differently shaped footage and evidence feel designed
  rather than awkwardly cropped.
- **Trigger:** An insert has a different aspect ratio, or consecutive beats need
  alternating media and text space.
- **Move:** Place the insert inside a bordered or otherwise designed module; alternate
  media/text balance across the stable grid when it improves the eye path.
- **Settings:** Preserve source proportions; use section border, spacing, and palette.
- **Restraint:** Do not nest footage when full-bleed imagery is emotionally stronger.
  Do not alternate sides mechanically on every beat.
- **Inputs / execution:** Insert media, canvas grid, typography block;
  composite-alpha or compose-presenter-world.
- **Fallback:** Letterbox or place the media full-width with text above/below.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V01. Mechanics video-01.

### R9 — Reserve a caption-system takeover for the emotional climax

- **Purpose / feeling:** Signal that one line carries a different emotional charge.
- **Trigger:** The director identifies the single strongest emotional line.
- **Move:** Suppress the base caption treatment and present the line in a distinct,
  section-compatible typography state.
- **Settings:** Intensity class 4; normally one use per piece; hold long enough to read.
- **Restraint:** Do not use on several “important” lines. Distinct does not mean
  stylistically unrelated.
- **Inputs / execution:** Selected line, word timing, special caption treatment;
  composite-alpha.
- **Fallback:** Emphasize one word inside the base caption system.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V09. Mechanics video-09.

### R10 — Let the final thesis replace the presenter

- **Purpose / feeling:** Make the conclusion feel decisive and linger after speech.
- **Trigger:** The final thesis word or short phrase resolves the piece.
- **Move:** Remove the presenter and let the conclusion occupy the full frame, holding
  after the voice ends.
- **Settings:** Intensity class 4; silent hold of at least about one second when pacing
  permits.
- **Restraint:** Use only when the word genuinely carries the conclusion. Do not copy
  the source's exact word, red field, or layout.
- **Inputs / execution:** Final phrase, end-of-speech time, section typography and
  palette; composite-alpha.
- **Fallback:** Hold the presenter and place a large concluding phrase beside them.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V19. Mechanics video-19.

### B. Proof, comparison, and narrative-state changes

### R11 — Land a visual receipt with the claim

- **Purpose / feeling:** Turn assertion into trust and proof.
- **Trigger:** A material spoken claim has a specific source, example, transformation,
  or result that can substantiate it.
- **Move:** Reveal the most relevant receipt on or immediately after the payoff word;
  hold it long enough for the audience to understand what it proves.
- **Settings:** Do not arrive early; choose legibility over rapid turnover.
- **Restraint:** Generic b-roll is not a receipt. Do not show evidence that only
  decorates the topic without proving the claim.
- **Inputs / execution:** Claim timestamp, evidence asset, proof relationship;
  composite-alpha or compose-presenter-world.
- **Fallback:** Keep the claim clean and add a concise sourced text label if no honest
  visual proof exists.
- **Status:** ✅ Buildable now when the evidence asset is available.
- **Provenance:** Taste V06, V24. Mechanics video-06, video-24.

### R12 — Escalate receipts instead of repeating them

- **Purpose / feeling:** Make an argument accumulate persuasive force.
- **Trigger:** Several related claims build one thesis.
- **Move:** Progress from source or premise to derivation, application, and dynamic
  proof. Use a second instance to demonstrate that a method is a system rather than a
  one-off.
- **Settings:** Each receipt must add a new evidentiary function.
- **Restraint:** Do not repeat near-identical screenshots or reuse the same proof type
  simply to maintain motion.
- **Inputs / execution:** Ordered claims and multiple evidence states; ordinary
  timeline sequencing with composite-alpha.
- **Fallback:** Use fewer, stronger receipts and allow clean narration between them.
- **Status:** ✅ Buildable now when evidence states exist.
- **Provenance:** Taste V06. Mechanics video-06.

### R13 — Let the audience watch the before become the after

- **Purpose / feeling:** Make improvement understandable, not merely asserted.
- **Trigger:** Narration identifies a flaw and names a fix or changed state.
- **Move:** Preserve the identity of the subject while a circular or linear reveal
  transforms before into after on the spoken cue. Optionally restate the same states
  once with explicit Before and After labels.
- **Settings:** Reveal begins close to the verbal change; labels are mandatory in a
  summary card.
- **Restraint:** Do not compare unrelated subjects or use a wipe when a direct cut
  communicates more honestly.
- **Inputs / execution:** Matched before/after assets and cue time;
  render-geometric-masks.
- **Fallback:** Use a static side-by-side or two labelled cards.
- **Status:** ✅ Buildable now. Staged hand-drawn critique marks remain Future F8.
- **Provenance:** Taste V11, V23. Mechanics video-11, video-16, video-23.

### R14 — Transform the world to express a narrative state

- **Purpose / feeling:** Make overwhelm, fragmentation, or relief visible.
- **Trigger:** The story moves into overload, contradiction, distress, or resolution.
- **Move:** For fragmentation, briefly split the presenter into multiple crops against
  negative space, then resolve. For overwhelm-to-relief, build clutter around a stable
  subject and replace it with a clean organized state at resolution.
- **Settings:** Intensity class 3; brief overload; clear return to stability.
- **Restraint:** Do not use fragmentation as a default montage look or clutter a beat
  whose meaning is already difficult to understand.
- **Inputs / execution:** Narrative-state labels, presenter crop/matte, accent assets;
  track-and-mask + composite-alpha.
- **Fallback:** Change one background geometry or reduce/clear supporting elements
  without multiplying the person.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V10, V19. Mechanics video-10, video-19.

### R15 — Build accumulation in steps, then hold the result

- **Purpose / feeling:** Let a growing list, crowd, recap, or burst feel additive.
- **Trigger:** Narration accumulates items or starts a new energetic card.
- **Move:** Add one item at a time at a deliberate cadence. Recap phrases can build in
  negative space; small accent graphics can burst in over roughly 0.5–1.5 seconds;
  hold the completed group before clearing.
- **Settings:** Cadence follows speech or beat structure; one stable anchor remains.
- **Restraint:** Do not add elements faster than they can be distinguished. Avoid
  random sparkles with no accumulation meaning.
- **Inputs / execution:** Ordered items, timestamps, accent assets; composite-alpha.
- **Fallback:** Reveal the complete group once, then highlight items sequentially.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V07, V09, V10. Mechanics video-07, video-09, video-10.

### C. High-impact accents and subject elevation

### R16 — Use Difference shapes as brief punctuation

- **Purpose / feeling:** Add a controlled hit to an emphasis beat or hard cut.
- **Trigger:** A selected impact word, reveal, montage beat, or existing hard cut needs
  extra energy.
- **Move:** Flash one white Difference-blend geometry, stack two or three staggered
  shapes for a stronger hit, or bridge the existing cut with related outgoing and
  incoming shapes. Do not move the source cut.
- **Settings:** the project lead's accepted taste is 4–5 frames. The source tutorial demonstrates
  2–3 frames; duration remains FPS-aware and adjustable. Finish on a clean frame.
- **Restraint:** Not a constant glitch layer. Avoid several stacked events in one
  short passage.
- **Inputs / execution:** Beat/cut time, target region, geometry and intensity;
  render-geometric-masks.
- **Fallback:** Use one short opacity or color-field accent without Difference blend.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V04, plus the project lead's later accepted 4–5-frame capability choice. Mechanics video-04, [geometric-masks capability](../capabilities/geometric-masks.md).

### R17 — Elevate an important person or quote into a live poster

- **Purpose / feeling:** Make the audience recognize that this person or line matters.
- **Trigger:** A genuinely important naming, quote, introduction, or highlight moment.
- **Move:** Isolate the live subject, replace the original environment with a calm
  graphic canvas, reframe into deliberate negative space, add concise typography,
  and optionally apply the accepted inner-luminance accent treatment.
- **Settings:** Outer temporal alpha; optional inner luminance thresholds around
  lo 0.20 / hi 0.55 as adjustable defaults; intensity class 3.
- **Restraint:** Reserve for importance. Do not copy the source's Cillian Murphy
  identity, red/white palette, or exact lockup.
- **Inputs / execution:** Presenter footage, RVM matte, selected line/name, canvas and
  type treatment; track-and-mask + posterize-subject + composite-alpha.
- **Fallback:** Keep the original footage and use a restrained title card or side text
  without posterization.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V17. Mechanics video-17, [inner-luminance capability](../capabilities/inner-luminance-mask.md).

### D. Rhythm and audio

### R18 — Use audio layers to decide eligibility, not creative meaning

- **Purpose / feeling:** Prevent placements that fight speech, music, or silence.
- **Trigger:** A proposed move depends on current audio state.
- **Move:** Use independent speech and music layers: word-synced text belongs in
  speech; music-driven visual accents belong where music is audible; ducking activates
  only during speech; silence may justify breathing room.
- **Settings:** Speech and music may overlap. Audio detection does not decide which
  visual is emotionally correct.
- **Restraint:** Do not turn every detected beat or speech onset into an edit.
- **Inputs / execution:** segment-speech-music output plus editorial beat map.
- **Fallback:** If separation confidence is poor, use transcript timing and manual
  section labels; avoid aggressive audio-conditioned moves.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V03, V13. Mechanics [speech/music capability](../capabilities/speech-music-segmentation.md).

### R19 — Prefer downbeats for added music-led events

- **Purpose / feeling:** Give music-driven additions weight without frantic cutting.
- **Trigger:** A supplementary montage, graphic sequence, or insert treatment follows
  a music bed.
- **Move:** Place major changes on downbeats by default. Use every beat only for an
  intentionally frantic passage; use phrase boundaries for sparse treatment.
- **Settings:** Density is a director dial, not a detector setting.
- **Restraint:** In v1, never use the beat map to recut the supplied rough cut. It may
  time only added elements or inserted sub-compositions already authorized by the
  plan.
- **Inputs / execution:** detect-beats output and approved treatment window.
- **Fallback:** Use phrase starts or manually selected musical accents.
- **Status:** ✅ Buildable now.
- **Provenance:** the project lead's accepted audio-phase listening decision; mechanic
  [beat-detection capability](../capabilities/beat-detection.md).

### R20 — Make room for dialogue while preserving the music's body

- **Purpose / feeling:** Keep speech effortless to understand without making the music
  vanish or pump distractingly.
- **Trigger:** Speech overlaps a music bed.
- **Move:** During speech, carve the music around the vocal range and apply a gentle
  broad duck; return to the untreated music state outside speech.
- **Settings:** Accepted constructed-mix default: general/male center about 1350 Hz,
  width 1.5 octaves, carve −6 dB, plus broad duck −6 dB; female center about 2500 Hz.
  Duck depth remains a mix dial. Source guidance was about 0.5-octave width and −2 dB
  usual gain; both values remain documented rather than silently conflated.
- **Restraint:** Never judge the system on editor-pre-ducked music. Avoid over-wide
  carving that hollows the track.
- **Inputs / execution:** Clean/separated speech and music stems, speech regions;
  duck-music-under-speech.
- **Fallback:** Gentle speech-gated broad duck without EQ if the stems or filter path
  fail.
- **Status:** ✅ Buildable now.
- **Provenance:** Taste V13. Mechanics video-13, [dialogue-aware ducking capability](../capabilities/dialogue-aware-ducking.md).

### E. Screen recordings

### R21 — Direct a screen recording like a cinematic shot

- **Purpose / feeling:** Turn flat evidence into a focused, story-driven visual space.
- **Trigger:** A screen recording is important enough to become b-roll rather than a
  plain full-screen insert.
- **Move:** Choose only the treatment that serves the beat: perspective plane and slow
  drift for cinematic presence; gradient depth-of-field to direct attention; macro
  subpixel treatment for extreme zoom; cursor HUD when pointer movement itself needs
  guidance.
- **Settings:** Start from accepted rig ranges, then frame for the actual screen. Keep
  the focus band on meaningful content and overlays readable.
- **Restraint:** Do not combine every treatment by default. A HUD is not useful when
  the cursor is irrelevant; blur is harmful when the viewer must read the whole page.
- **Inputs / execution:** Screen recording, target region, optional cursor coordinates,
  camera brief; render-geometric-masks.
- **Fallback:** Use a clean framed screen module with a simple push toward the relevant
  area.
- **Status:** ✅ Buildable now at concept level; content-specific design remains for
  the unified design pass.
- **Provenance:** Taste V24. Mechanics video-24, [geometric-masks capability](../capabilities/geometric-masks.md).

---

## Part IV — Future rule families

The director may describe these treatments, but planner v1 must not promise execution
until the capability or asset workflow is accepted.

### F1 — Pacing envelope and recovery controller

Map narrative sections to a density curve: attention spike → comprehension hold →
controlled rebuild → recovery. Count recent cuts, motion, graphics, sound events, and
scarcity moves. This is the executable version of Constitution C4–C7 and the Video 03
lesson. It needs the future beat-map planner's density model.

### F2 — Tactile diorama explanation

For difficult spatial or layered information, derive a miniature, cutaway, exploded
view, or paper-craft diagram and animate only the relationship being explained. The
asset-generation and fact-safe layer-separated diagram pipeline are not yet accepted.
Taste: V02.

### F3 — Illustrated paper-cutout story world

For unfamiliar scenarios or workflows that ordinary footage cannot clarify, build a
coherent illustrative sandbox with clear protagonist/support hierarchy, hybrid vector
or UI inserts, and state changes. The green mat and red/black outlines from Video 10
are examples, not mandatory styling. Taste: V10.

### F4 — Velocity-peak match transition

Give two visual states a shared motion path and place the swap at peak velocity so the
motion hides the transition. Requires a verified match-transition primitive. Source:
video-15.

### F5 — Stepped-time tactile motion

Run selected collage or print-style spatial motion at roughly 10–12 updates per second
to create physical stop-motion character. Treat frame rate as a style dial, not a
global law. Requires a stepped-time renderer. Taste: V14.

### F6 — Material texture and print-imperfection system

Choose halftone, paper, fabric, crumple, grain, dust, scratches, ink misalignment,
chromatic offsets, translucency, or highlight compression because the material
changes how the source feels—not because every premium edit needs dirt.

This family requires both a renderer and **Foundation Texture Pack v1**: a small
licensed set of actual still and moving plates with source, licence, resolution,
frame rate, tiling/looping behavior, blend guidance, and storytelling-use metadata.
Procedural gradients, grids, masks, and tunable halftones should remain code-generated
where practical. The pack is complete at `../../assets/foundation-textures-v1/`.

Taste: V16, V22, V23.

### F7 — Declarative raster stylization recipe

At a selected beat, transform the source into one readable graphic language such as
ASCII, dither, halftone, CRT, or pixel sorting. Store family, controls, seed, and time
behavior as a tunable recipe; never rely on an opaque website preset. Requires a
temporally stable raster-effect renderer. Taste:
V18.

### F8 — Staged critique annotation

Build hand-drawn lines, circles, and cross-outs one spoken critique at a time before
revealing the improved state. Requires an annotation authoring/build primitive.
Taste: V11.

### F9 — Raw-versus-edited synchronized comparison

When the story itself is the difference an edit or treatment makes, show matched raw
and treated states in a synchronized split view. This is a comparison/showcase
grammar, not a default layout for podcast footage. Requires a polished split-screen
family. Taste: V20.

### F10 — Active-word highlighted caption system

Highlight the currently spoken word within a consistent caption design when rapid
speech needs orientation or semantic emphasis. Requires a word-aware caption styling
system; it must still obey section grammar and density limits. Taste:
V20.

**Language register:** captions for Hindi speech enter this system **already
romanized to Hinglish** — the Devanagari ASR transcript is converted upstream by the
[`romanize-hinglish`](../../skills/romanize-hinglish/SKILL.md) skill (rule N9), which
preserves per-word timings so active-word highlighting still lands on the spoken
word. F10 never receives or renders Devanagari.

### F11 — Contextual concept visual resolver — accepted

When a concrete idea deserves a supporting visual, the director should describe the
communicative need and request a contextual concept visual. Execution may author,
generate, adapt, or source the result at run time.

**Accepted decision (the project lead, 2026-07-15):** use this as the replacement for
“keyword → stock icon.” Do not create a permanent noun-to-icon lookup. A book,
brain, runner, or heart from Video 20 is only a worked example. The circular
mask is an optional composition, not the definition of the rule. Icons remain
available when they are genuinely the strongest contextual choice; they are
never the automatic response to a keyword.

**Implementation — the "source" arm (2026-07-21; extended 2026-07-22):** F11's *source*
route now has **two peer sub-routes**, both peers of the *generate* arm:
- **stock** — [`source-footage`](../../skills/source-footage/SKILL.md) (Shelf 1): fetches
  real/stock b-roll from free libraries; best for generic human/emotional situations and
  establishing shots.
- **open-web mining** — [`mine-web-footage`](../../skills/mine-web-footage/SKILL.md)
  (Shelf 3): locates a **real, specific** thing (a named landmark, a real event, a
  recognizable scene) buried inside long web/YouTube videos, as a delegated sub-agent, when
  stock can't hold it and generation can't reproduce it.

All three (stock / open-web / generate) are **peer** choices per beat — real when the beat
must look *true*, open-web when it must be real *and specific*, generate when the concept has
no real referent — never source-first-with-fallback. The pick and the real-vs-generate
decision are human/vision judgment: the CLIP ranking aid must not auto-pick (its score
anti-correlates with dramatic register), and a low score is not a "generate instead" signal.
Two open-web query rules: describe the **LOOK not the ROLE** (a "villain" text query returned
the *hero* on the the prototype worked example test — CLIP has no concept of a character), and use a **web-found
reference image** for a specific person (image→image). Copyrighted subjects get a *metaphorical*
clip; the open-web sub-route finds clips but does not clear rights (the project lead's editorial/legal
call, gated by a go/no-go ask). Runbook stage 5a; capabilities
[`footage-sourcing`](../capabilities/footage-sourcing.md) and
[`web-footage-mining`](../capabilities/web-footage-mining.md). Both mechanics are proven;
in-edit placement/treatment is pending the project lead's taste acceptance.

### F12 — Named-layer reveal in an explainer

As narration names a component or relationship, reveal or emphasize that layer while
keeping unrelated layers quiet. Requires a semantic, layer-separated diagram
pipeline. Mechanics: video-02.

### F13 — Element-to-element morph

Continuously transform one meaningful UI or graphic object into the next instead of
hard-cutting between them. Requires a shape/path morph primitive. Taste:
V09.

### F14 — Typography role selection

Classify text by communicative job, then select its role, scale, depth, readability,
and motion. The executable roles are attention, identity, editorial, annotation,
utility, and caption; one font may fill several roles. Exact source fonts are
candidates, not a fixed library, and the engine never selects a different font merely
to manufacture variety.

- **Status:** ✅ Buildable now for role selection and the generic
  `identity_lockup`, `hero_field`, `thesis_build`, `editorial_note`, and
  `support_overlay` treatment relationships.
- **Restraint:** treatment names describe reusable compositions, never a shelf of
  source-specific phrases or looks.
- **Taste:**
V05.

### F15 — Section-level color and style unification

When mismatched assets must coexist, normalize palette and, when necessary, visual
style so they feel made for one section. Apply selectively, not everywhere. Tinting
may be procedural; deeper style changes may require generation. Taste:
V21.

### F16 — Camera angle as an asset-direction choice

When sourcing or generating an important visual, choose angle according to intended
feeling rather than accepting the safe eye-level default. Low/upward framing is a
source heuristic for power, not a measured universal law. This affects asset
selection/generation, not the underlying rough cut. Taste:
V11.

### F17 — Reference-guided asset adaptation

When a section needs a polished generated or authored asset, the resolver may search
for a strong visual reference and its available prompt or construction language, then
adapt it to the current subject and section grammar. It must not reduce the process to
blind noun replacement, copy a provider-specific prompt library permanently, or treat
the demonstrated gallery as a required dependency. This requires the future asset
resolver plus provenance, licensing, and adaptation safeguards. Taste:
V12.

---

## Part V — Cross-cutting execution rules

- **X1 — Arrive with the word (hardened 2026-07-15).** Important typography,
  receipts, and semantic visuals land **on** the payoff word — never before it.
  Setup scaffolding (frames, rules, kickers) may precede; the meaning-carrying
  element may not. Reveal timing must be authored against word timestamps, not
  scene boundaries: the Masterclass prototype revealed `HERO → ZERO` 6.4s before
  the spoken words because its reveals fired at scene starts (measured in the
  2026-07-15 delta log, MC-A). Verification compares every designed arrival to
  its word onset.
- **X2 — Keep one stable anchor.** During camera travel, card changes, lists, and
  accumulation, preserve one visual reference so the viewer remains oriented.
- **X3 — Hold for comprehension.** A technically correct arrival is still wrong if
  the audience cannot read or understand it before it disappears.
- **X4 — Lock overlays to the correct space.** Texture, pattern, and HUD elements must
  remain screen-locked or object-locked intentionally; do not let them drift with the
  wrong camera layer.
- **X5 — Preserve temporal stability.** Reuse deterministic seeds and clocks so grain,
  dots, and procedural effects do not shimmer or boil accidentally.
- **X6 — Render from recipes.** Persist tunable parameters and source provenance, not
  only a baked output.
- **X7 — Protect scarcity.** Count recent intensity-class 3 and 4 moves and enforce
  recovery time.
- **X8 — Prefer a coherent fallback.** If the ideal asset or capability is missing,
  reduce the move instead of substituting an unrelated flashy effect.
- **X9 — Verify pixels and sound.** Mechanical checks do not prove correct occlusion,
  readable holds, motivated camera, or good mixing.
- **X10 — Verify semantic text through camera motion.** For text with `edge_policy:
  contain`, inspect setup, arrival, each camera-leg midpoint and landing, and release.
  A clean plate boundary does not prove the words stayed readable.

---

## Part VI — Required planner checks

Before approving a beat map, reject or revise it when:

- two treatments compete for the same words or screen region;
- a graphic cannot be read for its intended hold;
- a high-impact move has no narrative or emotional justification;
- intensity-class 3–4 moves appear without recovery;
- a section changes palette, typography, texture, and motion grammar without a
  structural reason;
- a rear graphic is hidden by the presenter at the point that carries meaning;
- an identity, evidence, or utility beat does not declare full readability;
- environmental typography is too small for its meaning to survive the intended
  presenter occlusion;
- necessary text leaves the frame at any sampled camera state;
- three nearby beats repeat the same treatment, type role, scale, and depth without the
  director confirming a developing idea;
- an asset is unavailable, unlicensed, or lacks provenance;
- a future rule is assigned as though it were buildable;
- a beat-driven rule would alter the supplied rough cut;
- the treatment proves renderer capability but does not serve the intended feeling;
- a designed text/graphic exceeds its N1/N2 hold budget without a recorded reason;
- a meaning-carrying element arrives before its payoff word (X1 hardened);
- a text block ignores the active frame's center axes (N3);
- the opening minute carries chrome or a premature aspect shift (N4);
- a continuous scene element crosses the presenter's face (N5);
- a corner chip has no current narrative job (N6).

## Part VII — Amendments from the 2026-07-15 prototype review

Provenance: the project lead's live spoken review of the two autonomous prototypes on
2026-07-15 — the explicit creative decision this accepted rulebook requires for
changes. Every rule below traces to a pixel-verified delta recorded in the private
prototype-review notes (not shipped);
none is agent speculation.

### N1 — Maximum hold: land, be read, leave

- **Purpose / feeling:** Designed text is an event, not furniture. Overstay reads as
  the edit having stopped paying attention.
- **Move:** A designed text/graphic state holds long enough to be read comfortably
  (X3) and then exits. **Default budget 5–7 seconds**; longer holds require an
  explicit narrative reason recorded in the beat map.
- **Restraint inversion:** This is X3's missing other half — the prototypes held
  titles 13–52 seconds (and one sidebar 150 seconds) because only a minimum existed.
- **Speech coverage:** a long talking stretch is carried by the live caption system
  (F10), never by freezing one title over it.
- **Provenance:** the project lead stated 5–7s max (deltas FP-B, FP-E, MC-C-adjacent).

### N2 — Persistent structures pulse with the narration

- **Purpose / feeling:** Each list item's arrival is an event; the clearing between
  items is what makes it one.
- **Move:** Indices, trackers, and accumulating structures appear when their item is
  spoken, clear when the narration moves on, and return (optionally evolved — e.g.
  with an aspect change) for the next item. The accumulated full state may cap the
  sequence briefly, then exits (R15 hold-then-clear still applies).
- **Restraint:** Do not leave a tracker pinned through footage that has moved on —
  the FP gear ladder sat 150 seconds and killed its own design, which the project lead liked
  ("it's not about the design being bad").
- **Provenance:** the project lead described the exact desired rhythm (delta FP-C); strengthens
  R7's "clear reset" from a clause into a default.

### N3 — Compose against the active frame

- **Purpose / feeling:** Text that ignores the frame it shares reads as broken
  layout, however good the typography.
- **Move:** When the composition letterboxes, splits, or nests footage, text blocks
  and graphic clusters align to the **active frame's** optical center/axes — the
  letterboxed region or the adjacent footage module — not to the full canvas's top
  grid line.
- **Verified defect:** Masterclass hung its text columns from the canvas top beside
  a vertically-centered footage window, leaving dead quadrants (deltas MC-C, MC-4).
- **Provenance:** the project lead stated it twice, including the general form ("whatever
  aspect ratio is being chosen, the text should be aligned on the middle").

- **N3.1 — Any crop/inset/aspect-change of the presenter must be subject-measured
  (never blind canvas coordinates).** Whenever a treatment reframes, insets, or
  changes the aspect around the presenter (a presentation-mode inset, a punch-in
  crop, a reframed window), the system must **first measure where the face/subject
  actually is** — mask centroid + head band, or a vision face read — and frame the
  face intentionally (centered, or a deliberate rule-of-thirds offset). A hardcoded
  fixed offset that assumes the subject is centered is forbidden: talking-head
  subjects are routinely off-center. This is the crop-side companion to the main rule
  and to `compose-presenter-world` step 1 ("measure the subject first… author ALL
  geometry relative to these numbers — never blind canvas coordinates"); the gap was
  that *insets and aspect-changes* were not wired to that measurement the way the
  camera moves already are.
  - **Verified defect:** screenwriting-masterclass proxy (2026-07-18) — the
    presentation-card presenter inset used a blind offset and framed the torso, not
    the face. Fixed by measuring the head band from the RVM mask and centering on it.
  - **Enforcement:** add to the editorial gate — every presenter-containing inset/
    crop must record the measured subject center it was framed against; a crop with no
    recorded measurement fails. Computable where a mask exists (assert face-center is
    within the inset's central region).
  - **Provenance:** the project lead stated it as a durable project rule, 2026-07-18 ("you have
    to analyze the frame… always calculate where the face is actually centered so that
    we don't repeat the same mistake again… not just right now but in the future").

### N4 — Cold-open intimacy

- **Purpose / feeling:** The opening minute buys the audience's presence; formality
  and chrome before intimacy pushes them away.
- **Move:** Open close to the audience — full-frame footage, minimal or no system
  furniture. Read the footage's emotional register first (FP's opening is a person
  not at his best, cleaning his room — the treatment, if any, should reflect *that*).
  Presentation-mode/aspect shifts and format chrome arrive only after the audience
  is oriented (~10s earliest, later is fine).
- **Restraint:** "Nothing in the first minute" is a valid and often correct choice
  (C8). Recording labels, border systems, and archive metadata are never an opening
  statement.
- **Provenance:** the project lead stated both halves (deltas FP-A, MC-B).

### N5 — Editorial verification gate (enforcement, not taste)

- **Purpose:** Both prototypes passed technical QC while violating rules the system
  already had. Every editorial rule now has a pre-presentation check; prose intent
  is not evidence.
- **Move:** Before any render is shown, verify at pixel/timestamp level:
  word-sync arrivals (X1: no meaning-carrying element earlier than its word onset),
  hold durations vs N1/N2 budgets, active-frame alignment (N3), presenter-crossing
  elements (no continuous line/edge through a face — FP's front-layer spine rule
  sliced the presenter's face in half), corner-chip justification (N6), scarcity
  counts (X7), and cold-open compliance (N4).
- **Provenance:** deltas FP-D, MC-A; the QC-contract gap is Class 1 throughout.

### N6 — Corner metadata needs a job

- **Purpose / feeling:** Persistent corner chips read as forced decoration unless
  they are doing specific narrative work at that moment.
- **Move:** A HUD/ledger chip may appear when its content is the point (a score that
  the narration is about to pay off, a counter the story tracks). It enters when its
  job starts and leaves when the job is done — chips obey N1/N2 like everything else.
- **Provenance:** the project lead: corner notes "look horrible… except when it is needed for
  something very specific" (delta FP-D).

### N7 — Station travel: re-frame with the narration item

- **Purpose / feeling:** The presenter's world is a space with places in it; the
  camera moving to the next artifact *because the speaker referenced it* is what
  makes the edit feel authored in 3D rather than decorated in 2D.
- **System Capability & Editorial Logic (updated 2026-07-16):**
  This is not a single hardcoded template or movement style. Rather, it is a system-level
  ability to contextually design motivated camera moves:
  1. **Framing Awareness:** The system must identify the shot classification of the source
     media (e.g., wide shot, medium shot, medium close-up, close-up) and adjust camera limits.
     The shot class is **classified by a vision read of the whole frame** (more reliable and
     context-rich than a silhouette outline); the camera *limits* are then bounded by the
     measured subject size from the mask, as a *formula* rather than a fixed number — a wide
     shot can absorb a big push, a close-up almost none. Vision judges; the mask (pulled on
     demand for occlusion/safety) bounds. Execution mechanics: `skills/compose-presenter-world`
     step 4.
     *   *Restraint:* If starting on a medium close-up, avoid zooming into an extreme close-up;
         constrain the zoom scale (e.g., `s = 1.15` to `1.20` instead of `1.45`) to preserve
         presenter framing and resolution.
  2. **Movement Variation:** Alternate and adapt movement sequences according to story beats.
     *   *Examples:* Zoom in first to emphasize an element; or zoom out first to reveal the wider
         layout and then pan/slide toward a specific element.
  3. **No Boundary Leaks:** Camera moves (`cx`, `cy`) must always be mathematically bounded by
     the scale `s` (`cx` in `[960/s, 1920 - 960/s]`, `cy` in `[540/s, 1080 - 540/s]`) to keep the
     framing entirely inside the original video frame. Never reveal background margin gaps,
     borders, grids, or generator canvas backdrops.
- **Move Grammar Options:**
  *   *discrete hops (video-01 style):* anchor (full frame) → travel to station A on its word
      → hold → return to anchor → travel to station B.
  *   *continuous travel (video-09 style):* anchor → diagonal push-in toward element A →
      lateral slide (maintaining zoom) to element B → return to anchor.
- **Choosing the grammar is read from the speech rhythm, not preset (the project lead, 2026-07-16):**
  when two things are named back-to-back with little or no gap, **glide continuously**
  between them — the ideas are connected, so the move is too. When one thing is named,
  then a beat of explanation, then the next thing, **go to the first, return to the
  anchor, then go to the second** — the return mirrors the pause. The system reads the
  gap structure of the narration and picks; it may also combine and vary within a
  section (zoom-in to emphasize vs zoom-out to reveal then slide) as the material
  warrants. This is editorial judgment like an editor who holds every option in mind
  and fits the move to *this* video — never a fixed choreography or a keyword→move
  template.
- **Restraint:** travel needs a semantic destination (R4 unchanged); do not shake a
  canvas with nothing to travel to. One stable anchor always survives (X2).
- **Motivation is semantic OR rhythmic — not keyword-only:** a move must be motivated,
  but the motivation may be *semantic* (the narration references the place/element being
  traveled to) **or** *rhythmic* (the shot has sat still and the energy needs a lift —
  N8). What is never allowed is decoration for no reason. Do not let "matches a spoken
  noun" harden into a keyword→move template; that reintroduces exactly the mechanical
  rigidity this rule exists to prevent.
- **Status:** un-parked 2026-07-15; capability proven in safe-boundary renders at
  `workbench/research/camera-travel/out/`.
- **Provenance:** the project lead's review (delta MC-D / 2026-07-16 feedback): the v01/09 language "looked really
  fucking good and was never used by our edits... system needs the ability to think about these
  movements based on what frame we are on."

### N9 — On-screen language register: Hinglish, never Devanagari

- **Purpose / feeling:** Match how the project lead and his audience actually write: Hindi is
  spoken, but on-screen text is written in Latin script.
- **Move:** All captions, designed typography, and text overlays derived from Hindi
  speech are written in **Hinglish** — romanized Hindi ("main abhi Hindi bol raha
  hoon lekin English mein likh raha hoon"), with English loanwords restored to
  their English spellings (YouTube, vlog, edit, thumbnail, click — never यूट्यूब).
- **Restraint / honesty:** Romanization is a writing act, not a mechanical
  transliteration — ASR mishearings must be resolved by context before they reach
  the screen, and low-confidence wordings flagged rather than displayed wrong.
- **Mechanism (how the rule is actually satisfied):** an LLM converts the Devanagari
  ASR transcript to Hinglish, dispatched to a small-model sub-agent (provider-neutral
  role, not a hardcoded vendor model), per the
  [`romanize-hinglish`](../../skills/romanize-hinglish/SKILL.md) skill and the
  [Hinglish Caption Romanization](../capabilities/hinglish-romanization.md)
  capability. The register (locked spellings — `hoon`/`kyun`/`woh`/`mein`, English
  loanwords in English spelling, no academic long-vowels) lives in the skill as the
  single source of truth. There is **no** transliteration script — the only code is
  the backstop below.
- **Enforcement (the rule is not prose — it is a gate):** every caption/text source
  must contain **zero Devanagari codepoints (U+0900–U+097F)** before any render is
  presented. This is check #9 of the editorial verification gate (a `grep`, run
  automatically, never left to agent discretion). N9 was violated once *because it
  had no enforcement* — `fp-excerpt-corrected.mp4` shipped `लगता` on screen and was
  marked approved (2026-07-16); the gate now catches this class mechanically.
- **Status:** ✅ Effective immediately; enforced via the verification gate; applies to
  the F10 caption system.
- **Provenance:** the project lead stated, 2026-07-15 review session ("we shouldn't be adding
  subtitles in Hindi, it should always be Hinglish"); enforcement + delegation
  architecture directed by the project lead, 2026-07-16 ("LLM doing it… a sub-agent could even
  be a smaller model… don't want to hardcode for one specific provider").

### N8 — Pacing register: change is the default state

- **Purpose / feeling:** "People like things to change… people like to see different
  perspectives. Our style is a little slow right now."
- **Move:** Raise the visual state-change cadence, not the effect count: shorter
  holds (N1), pulsing structures (N2), per-item travel (N7), perspective/framing
  changes at narration turns. The v01 reference runs ~7 world/framing states in 20
  seconds while staying legible because exactly one thing changes at a time and the
  anchor keeps returning.
- **Restraint:** scarcity classes and recovery (C5/C7/X7) are untouched — class 3–4
  moves stay rare. What may not sit still is the ordinary support layer.
- **Calibration:** the excerpt-review loop with the project lead tunes the exact register;
  treat current numbers as starting points, not law.
- **Provenance:** delta G-A (direction the project lead-stated; calibration agent-inferred and
  marked as such).

### N10 — Atomic camera vocabulary: travel between meaningful visual stations

- **Purpose / feeling:** Turn a static presenter shot into a navigable world. Camera
  motion should carry the viewer toward meaning, not merely change the crop.
- **Accepted vocabulary:** `reveal-out`, `emphasis-push`, `right-reveal`, and
  `lr-phrase`. Each is an atomic editorial action with a readable magnitude. A
  return to neutral may close the action; an unrelated later move always requires a
  separate decision and template reference. `step-punch` is rejected and
  non-selectable.
- **Semantic-station rule:** before selecting travel between sides, define the two
  destinations. Station A must contain an accurate visual payload for the first
  phrase; Station B must contain a different accurate payload for the second. A
  payload may be designed text, evidence, a contextual graphic, or a sourced,
  generated, or derived asset. It arrives with its phrase, belongs to the same scene
  space as the presenter, and clears or resolves when its job ends. Camera path and
  payload timing are one directed beat, not separate decoration passes.
- **Stable anchor:** the presenter or another clearly chosen subject remains the
  viewer's orientation point while the surrounding destinations change.
- **Restraint / fallback:** do not select `lr-phrase` merely because two lateral
  moves would look energetic. It requires two genuinely distinct narration ideas
  that benefit from spatial comparison. If the editor cannot author two relevant,
  legible destinations, use one simpler motivated push/reveal or keep the shot
  locked. All generated or sourced payloads still obey accuracy, provenance, depth,
  readability, and section-grammar rules.
- **Execution / enforcement:** the accepted schedules live in
  `../../workbench/research/camera-templates/templates.json`; active compositions
  must consume that registry. Its automatic verifier rejects handwritten schedules,
  extra camera legs, sub-perceptual movement, below-1.0 scale, boundary leaks, and
  rejected IDs. The director's editorial gate rejects left/right beat plans that
  omit either station's phrase and visual payload.
- **Status:** ✅ T1–T4 accepted by the project lead's moving-video review on 2026-07-16; T5
  remains rejected.
- **Provenance:** the project lead's two camera-template reviews, recorded in delta HD-B on
  2026-07-16. In the acceptance review he explicitly described the first side and
  second side receiving different narration-relevant elements so the static shot
  reads as a 3D world.

### N11 — Source color is locked unless specifically requested

- **Purpose / feeling:** Preserve the photographed image and prevent a broad style
  request from silently becoming a grade.
- **Authority rule:** Color authority is independent of cut authority and defaults to
  `unchanged` on every assignment route. Only a user request that specifically asks
  for color correction, grading, relighting, recoloring, a LUT, or a named color
  adjustment may set it to `explicit`.
- **Non-authorizing language:** “Cinematic,” “visual polish,” “complete pass,”
  “cohesive look,” “make it pop,” and similar direction never authorize changing
  source-footage color.
- **Execution:** With `color_authority: unchanged`, every engine omits source-footage
  color transforms. Necessary color-space management is allowed only to preserve the
  source appearance across delivery and must be documented and visually matched.
  Added graphics may use a designed palette without altering the footage beneath.
- **Enforcement:** Editorial verification check #11 inspects the render plan or engine
  graph for color transforms and compares representative full-resolution source/output
  frames. Any unauthorized transform or visible shift fails the conform.
- **Provenance:** the project lead stated, 2026-07-19, after the `I AM BACK` pass inferred a
  restrained grade from a cinematic visual-polish request. The render is evidence of
  the scope error, not a color precedent.

## Honest source-versus-accepted differences

1. **Difference flash:** Video 04 demonstrates about 2–3 frames. the project lead later accepted
   4–5 frames in the geometric-mask capability. Rule R16 uses the accepted taste while
   preserving the source value.
2. **Music carve:** Video 13 speaks about a width setting around 0.5 and a usual gain
   near −2 dB. The accepted constructed-mix implementation uses a 1.5-octave,
   −6 dB carve plus a gentle −6 dB broad duck. Rule R20 preserves both.

## Resolved review decision

F11 is resolved **yes**: replace “keyword → icon” with “idea → contextual
concept visual.” The director describes the communicative need, and execution
authors, generates, adapts, or sources the visual for the current story instead
of using a permanent stock-icon lookup.

## Review status

**Accepted by the project lead on 2026-07-15.** Phase 3 creative-director instructions may
now begin. Changes to this accepted rulebook require a new explicit creative
decision rather than silent drift.

**Amendment 2026-07-15 (evening):** Part VII (N1–N8), the hardened X1, R4's
station-travel un-parking, and the extended planner checks were added from
the project lead's spoken prototype review — that review is the explicit creative decision
authorizing this amendment. N7 remains execution-gated on the camera-travel
capability proof; N8's exact register is calibrated through the corrected-excerpt
review loop.

**Amendment 2026-07-16:** N10 was accepted after moving-video review of four
corrected atomic camera treatments. It adds the locked atomic vocabulary,
perceptibility enforcement, and the requirement that left/right travel connect two
phrase-specific visual stations rather than move through empty space.

**Amendment 2026-07-19:** N11 was added by direct user instruction. Source-footage
color now defaults to locked on every route, and correction or grading requires a
specific color request plus verification check #11.
