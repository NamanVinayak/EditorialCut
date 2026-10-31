# Shelf 2 — image → image-to-video (built, cost-guarded, UNFIRED)

**Date:** 2026-07-21 · **Status:** ~95% built; **no real render run yet (no spend).**

The peer of Shelf 1 (real footage). Shelf 2 turns an **approved still** (from Shelf-1 sourcing,
image-gen, or a chosen frame) into a short motion clip via a paid image-to-video API — the cheap
path the project lead wanted: pay only to *animate a still you already approved*, not to gamble on a blind
text-to-video prompt.

## The flow

1. A still exists and is **approved by a human** (approval happens upstream, not here).
2. `animate.py` builds the exact i2v request for that still + a motion prompt.
3. **DRY RUN by default** — prints the request + estimated cost, sends nothing.
4. A real paid call requires ALL of: `FAL_KEY` set **and** `--spend` **and** a matching
   `--confirm <token>` **and** the estimate under the session cap **and** `--approved`.

```bash
# dry run (no key, no spend) — proves the request + cost, spends nothing:
python3 animate.py --image still.jpg --prompt "slow push in, subtle handheld" --duration 5
# real generation (only when you choose to spend):
FAL_KEY=<your-key> python3 animate.py --image still.jpg --prompt "..." --duration 5 \
    --approved --spend --confirm SPEND-0.50-d0922f
```

## What is verified (against fal.ai live docs, 2026-07-21)

- **Gateway pattern:** `POST https://queue.fal.run/fal-ai/{model}`, header `Authorization: Key
  <FAL_KEY>`, body `{prompt, image_url, duration}`; poll `status_url` → `response_url`; video URL
  at `result["video"]["url"]`. Verified against fal's live docs — **not stale.**
- **Model `kling-std`** (`fal-ai/kling-video/v1/standard/image-to-video`): required `prompt` +
  `image_url`, optional `duration` (5/10). Schema doc-verified.
- **Image input:** fal accepts a base64 **data URI** (used here for local stills) or a
  `fal.storage.upload` URL (recommended for large/production).
- **Pricing (fal, 2026):** Hailuo 02 ~$0.045/s (cheapest), Kling std cheap, LTX cheapest/fastest,
  up to Sora/Seedance ~$0.30/s. A 5 s test clip is well under $1.

## What is NOT done (the last 5% — needs a real spend)

- **No real render has run.** Motion quality, artifacts, and exact output shape are unproven until
  one clip is generated. Everything above the paid call is proven; the paid call is unfired.
- `hailuo-02` and `ltx` schemas are **price-verified only** (`schema_verified:false`) — verify
  their exact model path + input schema on fal before enabling.
- **One gateway built (fal).** Replicate and Runway-direct are known alternative patterns
  (each provider documents its own submit/poll API) but are **not** wired or verified here —
  do that only if fal proves insufficient.
- Not wired into the director's decision docs yet — that waits until a real clip proves the
  capability (unlike Shelf 1, which is proven and already wired to F11's "source" arm).

## Files (pure stdlib — no deps, no venv)

- `models.json` — verified model registry (paths, schemas, price estimates, sources/dates).
- `providers/fal_i2v.py` — fal gateway client; `build_request()` is pure/offline, `submit_and_wait()`
  is the only network method.
- `cost_guard.py` — hard spend gate (key + `--spend` + request-derived token + session cap +
  append-only `out/spend-log.jsonl`).
- `animate.py` — the still → approve → animate orchestrator (dry-run default).

## First real test when the project lead is ready

Set `FAL_KEY`, pick a beat Shelf 1 couldn't serve (e.g. the "on the run" fugitive), generate/approve
a still, then run one 5 s `kling-std` clip (~$0.50 est) with `--spend --confirm <token> --approved`.
Review the motion; if good, wire Shelf 2 into runbook stage 5a/6 and the F11 "generate-motion" arm.
