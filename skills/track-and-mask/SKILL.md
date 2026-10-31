---
name: track-and-mask
description: Invoke to isolate and temporally track a human presenter into a transparent alpha master (RVM default) for background replacement, foreground typography, or graphics placed behind the subject. Do NOT approximate a silhouette by hand or crop a fixed box; per-shot suitability and settings are a judgment call on the tool's output.
---

# Track and Mask

## Overview

Create an assistant-editor's tracked presenter matte. Use the accepted local RVM workflow for people; keep masking separate from the downstream graphic design.

## Choose the job

| Footage need | Route |
| --- | --- |
| One visible human presenter | RVM MobileNetV3 on MPS — accepted default |
| Edited footage with hard cuts | Process each accepted shot separately; reset recurrent state at cuts |
| Chosen object or non-human subject | Prompted tracking is a separate capability; EdgeTAM is research evidence, not the presenter default |
| Overlapping people, transparent material, severe blur, broadcast roto | Escalate to supervised roto or a separately approved cloud test |

Do not substitute Apple Vision for RVM or invent optical-flow, dilation, or feathering stages without a new evidence-backed comparison.

## Workflow

1. **Lock the source and output.** If the user already supplied the file and purpose, proceed. Otherwise confirm them. Record `ffprobe`, SHA-256, byte size, and modification time. Never alter or write beside the original.
2. **Create a unique run.** Write under `research/masking/runs/<source>-<run-id>/` with `frames/`, `masks/`, `logs/`, `media/`, and `manifest.json`. Never run `maskbench all` for production footage because benchmark paths are fixed.
3. **Respect cuts.** For one continuous shot, keep RVM recurrent state through every frame. For a multi-shot edit, reuse an accepted shot map or review boundaries and run each shot independently.
4. **Decode exact frames.** Preserve the intended delivery raster and frame rate; use sequential `frame_%06d.png` names. Record the decoded count.
5. **Run the proven adapter** from the project root:

   ```bash
   research/masking/backends/rvm/.venv/bin/python \
     research/masking/backends/rvm/run.py \
     --input-dir "$RUN/frames" --output-dir "$RUN/masks" \
     --metadata "$RUN/backend-metadata.json" \
     --vendor research/masking/backends/rvm/vendor/RobustVideoMatting \
     --checkpoint research/masking/backends/rvm/checkpoints/rvm_mobilenetv3.pth \
     --variant mobilenetv3 --device mps
   ```

6. **Export editable alpha.** Pair each RGB frame with its same-name soft mask and encode ProRes 4444 (`ap4h`, `yuva444p12le`). Map source audio only when timing matches exactly. Also export a matte preview and a neutral checkerboard or solid-color cutout.
7. **Verify before delivery.** Require identical input/mask names and counts; nonuniform 0–255 alpha; matching raster, rate, duration, and frame count; a decodable alpha plane; and an unchanged source fingerprint. Watch normal-speed and frame-step evidence around hair, hands, microphone, motion blur, entrances, and exits.
8. **Deliver evidence.** Return the alpha MOV, mask preview, diagnostic composite, manifest, backend metadata, logs, verification result, and honest limitations.

## Accepted envelope

RVM was accepted on the project lead's talking-head footage after a 600-frame 1080p/30 comparison against Apple Vision and EdgeTAM. A second 180-frame validation produced native 3840×2160 masks and a verified 59.94 fps ProRes 4444 alpha export on the M4 Pro.

## Boundaries

- This skill supplies masks and alpha assets; it does not decide typography, placement, color, animation, or taste.
- The benchmark's cyan `MASK TRACKING` graphic was diagnostic only and was explicitly rejected as a design example.
- Do not claim general support for multiple overlapping people, arbitrary objects, glass, smoke, reflections, or perfect hair under every condition.
- Read `docs/capabilities/subject-masking.md` for the accepted decision and `research/masking/BENCHMARK-RESULTS.md` for evidence.
