# SPDX-License-Identifier: MIT OR AGPL-3.0-only
# Original EditorialCut code. Implements fal.ai's public queue API
# (https://docs.fal.ai/); not derived from any third-party source.
"""fal.ai image-to-video client — pure stdlib, no third-party deps.

Implements fal's documented queue protocol: POST the job to
``queue.fal.run/fal-ai/{path}`` with an ``Authorization: Key <FAL_KEY>``
header and a JSON body of ``{prompt, image_url, duration}``; poll the returned
``status_url`` until ``COMPLETED``; then GET the ``response_url`` and read the
output video URL out of the result.

One gateway path selects the model (Kling, Hailuo, LTX, Veo, ...).

Money safety is structural: ``build_request()`` is pure and offline, so a
dry run never touches the network. Only ``submit_and_wait()`` makes calls, and
the cost guard must authorise before it is reached.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import time
import urllib.request
from pathlib import Path
from typing import Any, Optional

SUBMIT_URL = "https://queue.fal.run/fal-ai/{path}"


def image_to_input(image: str) -> tuple[str, str]:
    """Resolve an image argument into ``(value_for_api, printable_summary)``.

    An http(s) URL passes straight through. A local path is read and encoded
    as a base64 ``data:`` URI (fal accepts those). The second return value is
    a short human summary so dry-run logs don't dump a megabyte of base64.
    """
    if image.startswith(("http://", "https://")):
        return image, image
    p = Path(image)
    if not p.exists():
        raise FileNotFoundError(f"image not found: {image}")
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}", f"<data-uri {mime} {len(b64) // 1024} KB from {p.name}>"


class FalI2V:
    """Image-to-video calls against one fal model entry from the registry."""

    def __init__(self, model_entry: dict, api_key: Optional[str] = None):
        self.entry = model_entry
        self.path = model_entry["path"]
        self.api_key = api_key

    def build_request(
        self, image: str, prompt: str, duration: int = 5, **opts: Any
    ) -> dict:
        """Assemble (but do not send) the exact request. Pure and offline."""
        image_url, image_summary = image_to_input(image)
        payload: dict[str, Any] = {
            "prompt": prompt,
            "image_url": image_url,
            "duration": str(duration),
        }
        payload.update({k: v for k, v in opts.items() if v is not None})
        return {
            "submit_url": SUBMIT_URL.format(path=self.path),
            "auth_header_present": bool(self.api_key),
            "payload": payload,
            "printable_payload": dict(payload, image_url=image_summary),
        }

    # -- network (reached only after the cost guard authorises) --------------

    def _req(self, url: str, method: str = "GET", body: Optional[bytes] = None) -> dict:
        req = urllib.request.Request(
            url,
            data=body,
            method=method,
            headers={
                "Authorization": f"Key {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())

    def submit_and_wait(
        self, request: dict, poll_interval: float = 5.0, timeout: float = 600.0
    ) -> dict:
        """Submit the job, poll until done, return the final result JSON."""
        if not self.api_key:
            raise RuntimeError("no api key — refusing to submit")
        body = json.dumps(request["payload"]).encode()
        queued = self._req(request["submit_url"], "POST", body)
        status_url = queued["status_url"]
        response_url = queued["response_url"]

        deadline = time.time() + timeout
        while time.time() < deadline:
            status = self._req(status_url).get("status", "UNKNOWN")
            if status == "COMPLETED":
                return self._req(response_url)
            if status in ("FAILED", "CANCELLED", "ERROR"):
                raise RuntimeError(f"generation {status}")
            time.sleep(poll_interval)
        raise TimeoutError("i2v generation timed out")

    def download(self, result: dict, out_path: Path) -> Path:
        """Follow the entry's ``output_video_field`` and save the file."""
        node: Any = result
        for key in self.entry.get("output_video_field", "video.url").split("."):
            node = node[key]
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(node, timeout=180) as resp, open(out_path, "wb") as fh:
            fh.write(resp.read())
        return out_path
