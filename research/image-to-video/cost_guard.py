"""Hard cost guard for Shelf 2 (paid image-to-video). Pure stdlib.

Nothing spends money unless ALL of these are true:
  1. a real FAL_KEY is present in the environment;
  2. the caller passed --spend;
  3. the caller passed --confirm "<exact token>" matching the printed token;
  4. the estimated cost fits under the remaining session cap.

Default is DRY RUN: everything is assembled and priced, nothing is sent.
Every authorized spend is appended to spend-log.jsonl and counts against the cap.
The token is derived from the request so a stale/blind --confirm can't authorize
a different call than the one the user was shown.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "out" / "spend-log.jsonl"


def estimate_cost(price_per_second: float, duration: int) -> float:
    return round(price_per_second * duration, 4)


def confirm_token(model_key: str, prompt: str, duration: int, est: float) -> str:
    h = hashlib.sha256(f"{model_key}|{prompt}|{duration}|{est}".encode()).hexdigest()
    return f"SPEND-{est:.2f}-{h[:6]}"


def spent_so_far() -> float:
    if not LOG.exists():
        return 0.0
    total = 0.0
    for line in LOG.read_text().splitlines():
        if line.strip():
            total += json.loads(line).get("cost", 0.0)
    return round(total, 4)


def authorize(*, model_key: str, prompt: str, duration: int, est: float,
              spend: bool, confirm: str | None, cap_usd: float) -> tuple[bool, str]:
    """Return (allowed, reason). Refuses on any failed condition."""
    token = confirm_token(model_key, prompt, duration, est)
    if not os.environ.get("FAL_KEY"):
        return False, "FAL_KEY not set — refusing (dry-run only)."
    if not spend:
        return False, "no --spend flag — DRY RUN only."
    if confirm != token:
        return False, f"--confirm missing/mismatched. Required token: {token}"
    remaining = round(cap_usd - spent_so_far(), 4)
    if est > remaining:
        return False, f"est ${est:.2f} exceeds remaining session cap ${remaining:.2f} (cap ${cap_usd:.2f})."
    return True, f"authorized: ${est:.2f} (remaining after: ${remaining - est:.2f})"


def record(*, model_key: str, prompt: str, duration: int, cost: float,
           out_file: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "model": model_key, "prompt": prompt, "duration": duration,
            "cost": cost, "out_file": out_file,
        }) + "\n")
