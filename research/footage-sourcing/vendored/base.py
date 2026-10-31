# SPDX-License-Identifier: MIT OR AGPL-3.0-only
# Original EditorialCut code. Defines a small in-house adapter interface;
# not derived from any third-party source.
"""Shared shape for stock-media source adapters.

A "source" (Pexels today; Archive.org, Wikimedia, etc. later) knows how to
talk to one provider's search API and hand back results in one common
shape. Everything above this layer — ranking, de-duplication, the actual
editorial choice — is done elsewhere against `Candidate` rows, so it never
has to care which provider a clip came from.

The contract is deliberately tiny: a `name`, an availability check, a
`search`, and a `download`. A new provider is just a class that offers
those four things and returns `Candidate` objects.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Protocol, runtime_checkable


@dataclass
class Candidate:
    """One search hit from a source, before anything is downloaded.

    Carries enough to decide whether the clip is worth pulling, plus the
    provenance (creator, license, source URL) worth keeping around. Fields
    that don't apply to a given result stay at their defaults — images have
    `duration == 0.0`, sources without an fps simply omit it from `extra`.
    Adapters fill in what they can and leave the rest.
    """

    source: str                             # adapter name, e.g. "pexels"
    source_id: str                          # unique within that source
    source_url: str                         # landing page (human readable)
    download_url: str                       # direct file URL
    kind: str                               # "video" or "image"
    width: int = 0
    height: int = 0
    duration: float = 0.0                   # seconds (0 for images)
    creator: str = ""                       # attribution name
    license: str = ""                       # licence string or URL
    source_tags: str = ""                   # title + description + tags joined
    thumbnail_url: str = ""                 # for previews and image-fallback embeds
    extra: dict[str, Any] = field(default_factory=dict)  # source-specific junk

    @property
    def clip_id(self) -> str:
        """Stable ``"<source>_<source_id>"`` key for this result."""
        return f"{self.source}_{self.source_id}"


@dataclass
class SearchFilters:
    """What to ask a source for. Adapters ignore fields they can't honour.

    These are set generously by the caller; whatever a given provider can't
    apply server-side is either filtered client-side by the adapter or left
    for the ranking step to sort out.
    """

    kind: str = "video"                     # "video", "image", or "any"
    min_duration: Optional[float] = None    # seconds; None = no floor
    max_duration: Optional[float] = None    # seconds; None = no ceiling
    orientation: Optional[str] = None       # "landscape" | "portrait" | "square"
    min_width: Optional[int] = None         # resolution floor in pixels
    per_page: int = 20
    page: int = 1


@runtime_checkable
class StockSource(Protocol):
    """The four things every source adapter must provide.

    ``name``
        Stable identifier; becomes the ``source`` on each `Candidate`.
    ``is_available``
        Cheap, offline check for "are the keys/deps present?" — callers skip
        sources that answer False.
    ``search``
        Returns a flat list of `Candidate` objects (empty list is fine).
        Network failures should raise; the caller decides how to handle them.
    ``download``
        Writes the candidate's file to ``out_path`` (making parent dirs) and
        returns the path. Blocking; no caching of its own.
    """

    name: str

    def is_available(self) -> bool: ...

    def search(self, query: str, filters: SearchFilters) -> list[Candidate]: ...

    def download(self, candidate: Candidate, out_path: Path) -> Path: ...
