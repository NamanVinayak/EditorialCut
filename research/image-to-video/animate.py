"""Shelf 2 orchestrator: approved still -> image-to-video, cost-guarded.

The FLOW (peer of sourcing real footage, Shelf 1):
  1. A still exists and is APPROVED by a human (from Shelf-1 sourcing, image-gen,
     or a chosen frame). Approval happens BEFORE this script.
  2. This script builds the exact i2v request for that still + a motion prompt.
  3. DRY RUN by default: prints the request + estimated cost, sends nothing.
  4. Only with FAL_KEY set + --spend + a matching --confirm token, under the
     session cap, does it actually submit / poll / download.

Examples:
  # dry run (no key, no spend) — prove the request + cost:
  python animate.py --image still.jpg --prompt "slow push in, subtle handheld" --duration 5
  # real generation (only when you choose to spend):
  FAL_KEY=<your-key> python animate.py --image still.jpg --prompt "..." --spend --confirm SPEND-0.50-abc123
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from providers.fal_i2v import FalI2V  # noqa: E402
import cost_guard  # noqa: E402

REGISTRY = json.loads((ROOT / "models.json").read_text())


def main() -> None:
    ap = argparse.ArgumentParser(description="Animate an approved still (Shelf 2, cost-guarded).")
    ap.add_argument("--image", required=True, help="approved still: local path or http(s) URL")
    ap.add_argument("--prompt", required=True, help="motion prompt (what should MOVE)")
    ap.add_argument("--model", default=REGISTRY["default_model"], choices=list(REGISTRY["models"]))
    ap.add_argument("--duration", type=int, default=5)
    ap.add_argument("--out", default=str(ROOT / "out" / "clip.mp4"))
    ap.add_argument("--cap", type=float, default=2.0, help="hard session spend cap (USD)")
    ap.add_argument("--approved", action="store_true", help="assert the still is human-approved")
    ap.add_argument("--spend", action="store_true", help="opt in to a real paid call")
    ap.add_argument("--confirm", default=None, help="exact SPEND token printed by the dry run")
    args = ap.parse_args()

    entry = REGISTRY["models"][args.model]
    key = os.environ.get("FAL_KEY")
    client = FalI2V(entry, api_key=key)
    request = client.build_request(args.image, args.prompt, duration=args.duration)
    est = cost_guard.estimate_cost(entry["usd_per_second_estimate"], args.duration)
    token = cost_guard.confirm_token(args.model, args.prompt, args.duration, est)

    print("=" * 68)
    print(f"Shelf 2 · image-to-video · model={args.model} ({entry['path']})")
    print(f"  schema_verified: {entry['schema_verified']}   source: {entry.get('source')}")
    if not entry["schema_verified"]:
        print("  !! schema NOT doc-verified — verify before a real spend")
    print(f"  still (approved={args.approved}): {request['printable_payload']['image_url']}")
    print(f"  motion prompt: {args.prompt!r}   duration: {args.duration}s")
    print(f"  submit_url: {request['submit_url']}")
    print(f"  payload: {json.dumps(request['printable_payload'])[:300]}")
    print(f"  ESTIMATED COST: ${est:.2f}  (est ${entry['usd_per_second_estimate']}/s ×"
          f" {args.duration}s; confirm exact price on fal before spending)")
    print(f"  session spent so far: ${cost_guard.spent_so_far():.2f} / cap ${args.cap:.2f}")
    print("-" * 68)

    ok, reason = cost_guard.authorize(model_key=args.model, prompt=args.prompt,
                                      duration=args.duration, est=est, spend=args.spend,
                                      confirm=args.confirm, cap_usd=args.cap)
    if not ok:
        print(f"NOT SPENDING — {reason}")
        if not args.spend:
            print(f"To actually generate: set FAL_KEY, add  --spend --confirm {token}")
        print("=" * 68)
        return

    if not args.approved:
        print("REFUSING: still not marked --approved. Approve the frame first.")
        return

    print(f"AUTHORIZED — {reason}\nsubmitting to fal (this spends money)...")
    result = client.submit_and_wait(request)
    out = client.download(result, Path(args.out))
    cost_guard.record(model_key=args.model, prompt=args.prompt, duration=args.duration,
                      cost=est, out_file=str(out))
    print(f"DONE -> {out}  (recorded ${est:.2f})")
    print("=" * 68)


if __name__ == "__main__":
    main()
