---
title: Subject Masking
aliases:
  - Presenter Matting
  - Track and Mask
  - Graphics Behind Presenter
type: capability
status: accepted-v1
updated: 2026-07-13
---

# Subject Masking

## Decision

**Accepted for v1: use Robust Video Matting (RVM) as the local default for a visible human presenter.** the project lead reviewed the synchronized Apple Vision, RVM, and EdgeTAM comparison and found the broad graphic-behind results similar. RVM was the only method he considered consistently strong in the raw matte and checkerboard views, and it was also the fastest and lightest measured option.

This acceptance is for the masking job. the project lead explicitly rejected the benchmark's cyan `MASK TRACKING` graphic as a design example. Typography and motion-design quality remain separate downstream decisions.

## Editorial purpose

Produce a temporally continuous soft alpha matte so an editor can:

- place typography or graphics behind a presenter;
- replace or stylize the background;
- reuse the isolated presenter in another composition;
- inspect hair, hands, clothing, and microphone edges throughout motion.

This is more than making a mask on one frame. The matte must follow the subject across every frame without obvious drift, missing body parts, background inclusions, or distracting flicker.

## Proven local implementation

- Model: Robust Video Matting MobileNetV3
- Official repository commit: `53d74c6826735f01f4406b5ca9075eee27bec094`
- Checkpoint SHA-256: `3c7c1d92033f7c38d6577c481d13a195d7d80a159b960f4f3119ac7b534cf4f8`
- Runtime: PyTorch 2.13.0 on Apple MPS
- Machine: M4 Pro with 24 GB unified memory
- Prompt/correction burden: none for a single visible person
- Temporal behavior: recurrent state is preserved through each continuous shot
- Reusable procedure: [`skills/track-and-mask/SKILL.md`](../../skills/track-and-mask/SKILL.md)
- Private benchmark evidence is not distributed; reproduce it with the shipped runner and your own footage.

## Comparative benchmark

All methods processed the same 20-second, 1920×1080, 30 fps sequence of 600 frames.

| Method | Editorial job | Time | Peak memory | Human/visual decision |
| --- | --- | ---: | ---: | --- |
| RVM | Automatic recurrent human matte | **34.90 s** | **0.57 GB** | Accepted default; strongest matte/checkerboard result |
| Apple Vision Accurate | Automatic person segmentation | 64.78 s | 2.81 GB | Broad composite looked usable, but raw mask repeatedly included a large background/chair region |
| EdgeTAM | Box-prompted selected-subject tracking | 104.42 s | 4.77 GB | Broad composite looked usable; hard mask lost fine hair and showed shirt/hand holes |

the project lead found the methods difficult to distinguish in the broad `graphic behind subject` and edge-diagnostic views. The raw matte and checkerboard views were the decisive evidence. No numeric alpha-accuracy score is claimed because no hand-authored ground truth exists.

## 4K/~60 fps validation

After acceptance, RVM processed a second continuous passage at 3840×2160 and `60000/1001` fps:

- Duration: 3.003 seconds
- Frames: 180 input and 180 same-name masks
- Native mask size: 3840×2160
- Wall time: 32.83 seconds
- Peak measured memory: 0.87 GB
- Alpha export: 3840×2160 ProRes 4444, `ap4h`, `yuva444p12le`, 180 frames
- Foreground fraction: mean 0.2872, standard deviation 0.0023
- Alpha range: 0–255
- Source SHA-256, size, and modification time remained unchanged

This establishes local high-resolution feasibility for short passages. It does not promise real-time 4K60 processing or small files: the three-second alpha master is approximately 698 MB.

## Routing rules

| Condition | Decision |
| --- | --- |
| One presenter in a continuous talking-head shot | Use RVM directly |
| Hard cut or changed camera setup | Reset recurrent state and process the new shot separately |
| Several overlapping people or chosen non-human object | Use a separate prompted/supervised tracking workflow |
| Glass, smoke, reflections, mesh, severe blur, or VFX-grade hair | Treat RVM as a draft and escalate to supervised roto or separately approved research |
| Local result visibly fails | Discuss a cloud-quality comparison; obtain upload/cost approval first |

EdgeTAM remains useful evidence for a future prompted `select and track this thing` capability. It should not be silently substituted for the accepted fine presenter matte.

## Output contract

- Immutable-source fingerprint and media probe
- Exact frame sequence and shot scope
- Same-name soft alpha masks for every input frame
- ProRes 4444 alpha master
- Matte-only and neutral-background diagnostic previews
- Model commit, checkpoint hash, device, settings, timing, memory, and logs
- Frame-count/timing/alpha/source-integrity verification
- Human-readable known limitations

## Design boundary

The matte is an editorial asset, not a finished visual treatment. A downstream creative skill decides whether text belongs behind the subject, what it says, where it sits, how it moves, and whether the composition matches the project lead's taste. Diagnostic graphics must remain visually neutral and must never be promoted as a style template.

## Project continuation

Presenter matting is closed. the project lead has chosen to finish the other masking-like jobs before audio: alpha-compositing integration, an inner luminance treatment, renderer-native geometric masks, prompted non-human object propagation, point/surface tracking, and depth/occlusion. The exact order and resume action live in the project review log. Do not treat this as permission to compare more presenter-matting models.
