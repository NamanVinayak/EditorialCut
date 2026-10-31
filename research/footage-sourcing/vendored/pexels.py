# SPDX-License-Identifier: MIT OR AGPL-3.0-only
# Original EditorialCut code. Implements the public Pexels REST API
# (https://www.pexels.com/api/documentation/); not derived from any
# third-party source.
"""Pexels source adapter.

Talks to Pexels' two documented search endpoints — ``/videos/search`` and
``/v1/search`` — and folds both into the common `Candidate` shape so callers
never branch on video-vs-image. Pexels is a good default: big free catalogue,
no attribution required, direct file URLs that cache well.

Auth is the raw ``PEXELS_API_KEY`` in the ``Authorization`` header, exactly as
Pexels documents it (no ``Bearer`` prefix).
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

from .base import Candidate, SearchFilters


_VIDEO_SEARCH_URL = "https://api.pexels.com/videos/search"
_IMAGE_SEARCH_URL = "https://api.pexels.com/v1/search"
_PEXELS_LICENSE = "Pexels License (free, no attribution required)"
_MAX_PER_PAGE = 80          # Pexels hard cap
_VIDEO_WIDTH_CAP = 1920     # don't bother downloading >1080p renditions


class PexelsSource:
    """Pexels adapter for both videos and images.

    Stateless: every call reads the API key from the environment, so a fresh
    instance per run is fine.
    """

    name = "pexels"
    display_name = "Pexels"
    provider = "pexels"
    priority = 10
    install_instructions = (
        "Set PEXELS_API_KEY in .env to enable Pexels stock search "
        "(free key at https://www.pexels.com/api/)."
    )
    supports = {"video": True, "image": True}

    # -- protocol ------------------------------------------------------------

    def is_available(self) -> bool:
        return bool(os.environ.get("PEXELS_API_KEY"))

    def search(self, query: str, filters: SearchFilters) -> list[Candidate]:
        """Query Pexels for `query`, dispatching on ``filters.kind``.

        ``"video"`` and ``"image"`` hit one endpoint each; ``"any"`` hits both
        and returns videos followed by images. No re-ranking happens here.
        """
        kind = (filters.kind or "video").lower()
        results: list[Candidate] = []
        if kind in ("video", "any"):
            results += self._search_videos(query, filters)
        if kind in ("image", "any"):
            results += self._search_images(query, filters)
        return results

    def download(self, candidate: Candidate, out_path: Path) -> Path:
        """Stream ``candidate.download_url`` to ``out_path`` in chunks."""
        import requests  # lazy: keep import cost off module load

        if not candidate.download_url:
            raise ValueError(f"Candidate {candidate.clip_id} has no download_url")

        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with requests.get(candidate.download_url, stream=True, timeout=120) as resp:
            resp.raise_for_status()
            with open(out_path, "wb") as fh:
                for chunk in resp.iter_content(chunk_size=1 << 16):
                    if chunk:
                        fh.write(chunk)
        return out_path

    # -- internals -----------------------------------------------------------

    def _headers(self) -> dict[str, str]:
        key = os.environ.get("PEXELS_API_KEY")
        if not key:
            raise RuntimeError(
                "PEXELS_API_KEY not set. Get a free key at "
                "https://www.pexels.com/api/ and add it to .env."
            )
        return {"Authorization": key}

    def _base_params(self, query: str, filters: SearchFilters) -> dict[str, Any]:
        params: dict[str, Any] = {
            "query": query,
            "per_page": min(max(filters.per_page, 1), _MAX_PER_PAGE),
            "page": max(filters.page, 1),
        }
        if filters.orientation:
            params["orientation"] = filters.orientation
        return params

    def _search_videos(self, query: str, filters: SearchFilters) -> list[Candidate]:
        import requests  # lazy

        resp = requests.get(
            _VIDEO_SEARCH_URL,
            headers=self._headers(),
            params=self._base_params(query, filters),
            timeout=30,
        )
        resp.raise_for_status()
        videos = resp.json().get("videos") or []

        out: list[Candidate] = []
        for v in videos:
            duration = float(v.get("duration") or 0)
            # Pexels can't filter duration server-side, so do it here.
            if filters.min_duration is not None and duration < filters.min_duration:
                continue
            if filters.max_duration is not None and duration > filters.max_duration:
                continue

            rendition = _pick_video_rendition(
                v.get("video_files") or [],
                min_width=filters.min_width or 0,
                max_width=_VIDEO_WIDTH_CAP,
            )
            if rendition is None:
                continue

            user = v.get("user") or {}
            out.append(
                Candidate(
                    source=self.name,
                    source_id=str(v.get("id")),
                    source_url=v.get("url") or "",
                    download_url=rendition.get("link") or "",
                    kind="video",
                    width=int(rendition.get("width") or v.get("width") or 0),
                    height=int(rendition.get("height") or v.get("height") or 0),
                    duration=duration,
                    creator=user.get("name") or "",
                    license=_PEXELS_LICENSE,
                    source_tags=_slug_tags_from_url(v.get("url") or ""),
                    thumbnail_url=v.get("image") or "",
                    extra={
                        "fps": rendition.get("fps"),
                        "rendition_quality": rendition.get("quality"),
                        "user_url": user.get("url"),
                    },
                )
            )
        return out

    def _search_images(self, query: str, filters: SearchFilters) -> list[Candidate]:
        import requests  # lazy

        resp = requests.get(
            _IMAGE_SEARCH_URL,
            headers=self._headers(),
            params=self._base_params(query, filters),
            timeout=30,
        )
        resp.raise_for_status()
        photos = resp.json().get("photos") or []

        out: list[Candidate] = []
        for p in photos:
            width = int(p.get("width") or 0)
            height = int(p.get("height") or 0)
            if filters.min_width is not None and width < filters.min_width:
                continue

            src = p.get("src") or {}
            # large2x is the detail/size sweet spot for montage stills;
            # fall back to the full original if the CDN omits it.
            download_url = src.get("large2x") or src.get("original") or ""
            if not download_url:
                continue

            out.append(
                Candidate(
                    source=self.name,
                    source_id=str(p.get("id")),
                    source_url=p.get("url") or "",
                    download_url=download_url,
                    kind="image",
                    width=width,
                    height=height,
                    duration=0.0,
                    creator=p.get("photographer") or "",
                    license=_PEXELS_LICENSE,
                    source_tags=(p.get("alt") or "").strip(),
                    thumbnail_url=src.get("medium") or "",
                    extra={
                        "photographer_url": p.get("photographer_url"),
                        "avg_color": p.get("avg_color"),
                    },
                )
            )
        return out


# -- module helpers (kept importable for tests) --------------------------------


def _pick_video_rendition(
    video_files: list[dict],
    min_width: int = 0,
    max_width: int = _VIDEO_WIDTH_CAP,
) -> Optional[dict]:
    """Largest playable rendition whose width fits ``[min_width, max_width]``.

    Pexels returns several renditions (SD/HD/UHD, plus HLS). Take the widest
    real video file within the cap — width as a quality proxy, cap so we don't
    pull 4K we'll only downscale anyway. Returns None if nothing qualifies.
    """
    usable = [
        f
        for f in video_files
        if (f.get("file_type") or "").startswith("video/")
        and f.get("link")
        and min_width <= int(f.get("width") or 0) <= max_width
    ]
    if not usable:
        return None
    return max(usable, key=lambda f: int(f.get("width") or 0))


def _slug_tags_from_url(url: str) -> str:
    """Turn a Pexels landing URL into a rough keyword string.

    Pexels video JSON has no reliable tags, but the landing URL is a slug like
    ``/video/aerial-view-of-city-at-night-3571264/`` — the uploader's own words.
    Drop the trailing numeric id and swap hyphens for spaces so CLIP's text
    encoder has something to chew on. Empty string if the URL won't parse.
    """
    if not url:
        return ""
    parts = url.rstrip("/").rsplit("/", 1)
    if len(parts) != 2:
        return ""
    slug = parts[1]
    head, _, tail = slug.rpartition("-")
    if head and tail.isdigit():
        slug = head
    return slug.replace("-", " ").strip()
