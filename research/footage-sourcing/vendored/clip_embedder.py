# SPDX-License-Identifier: MIT OR AGPL-3.0-only
# Original EditorialCut code. A standard wrapper over Hugging Face's public
# CLIP model API; not derived from any third-party source.
"""CLIP embedder — images and text into comparable 512-d vectors.

One job: encode images or strings with ``openai/clip-vit-base-patch32`` and
return L2-normalised ``float32`` rows, so cosine similarity is just a dot
product (``images @ query`` reads as similarity directly).

The model loads once per process (lazily, on first use) and runs on GPU if
one is present, else CPU. Heavy imports (torch, transformers) stay inside the
functions so merely importing this module is cheap. Deciding *what* to embed
and *how* to rank lives in the callers, not here.
"""
from __future__ import annotations

from pathlib import Path
from typing import Sequence, Union

import numpy as np


_MODEL = None
_PROCESSOR = None
_DEVICE: str = "cpu"
_MODEL_ID = "openai/clip-vit-base-patch32"
_DIM = 512


def _load() -> None:
    """Load the CLIP model + processor once, caching them at module scope."""
    global _MODEL, _PROCESSOR, _DEVICE
    if _MODEL is not None:
        return
    import torch  # type: ignore
    from transformers import CLIPModel, CLIPProcessor  # type: ignore

    _DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    _PROCESSOR = CLIPProcessor.from_pretrained(_MODEL_ID)
    _MODEL = CLIPModel.from_pretrained(_MODEL_ID).to(_DEVICE)
    _MODEL.eval()


def _l2_normalise(features):
    """Row-wise L2 normalise, guarding against divide-by-zero."""
    return features / features.norm(dim=-1, keepdim=True).clamp_min(1e-8)


def model_info() -> dict:
    """Provenance metadata for whatever index these embeddings feed."""
    return {"model_id": _MODEL_ID, "device": _DEVICE, "dim": _DIM}


def embed_images(image_paths: Sequence[Union[str, Path]]) -> np.ndarray:
    """Encode image files into an ``(N, 512)`` float32 matrix of unit rows."""
    if not image_paths:
        return np.zeros((0, _DIM), dtype=np.float32)

    import torch  # type: ignore
    from PIL import Image  # type: ignore

    _load()
    assert _MODEL is not None and _PROCESSOR is not None

    images = [Image.open(str(p)).convert("RGB") for p in image_paths]
    try:
        inputs = _PROCESSOR(images=images, return_tensors="pt").to(_DEVICE)
        with torch.no_grad():
            features = _l2_normalise(_MODEL.get_image_features(**inputs))
        return features.cpu().numpy().astype(np.float32, copy=False)
    finally:
        # Release PIL file handles promptly (matters on Windows).
        for img in images:
            img.close()


def embed_texts(texts: Sequence[str]) -> np.ndarray:
    """Encode strings into an ``(N, 512)`` float32 matrix of unit rows."""
    if not texts:
        return np.zeros((0, _DIM), dtype=np.float32)

    import torch  # type: ignore

    _load()
    assert _MODEL is not None and _PROCESSOR is not None

    # A blank string upsets the processor; swap in a filler so row indices
    # still line up with what the caller passed.
    cleaned = [t if (t and t.strip()) else "untitled" for t in texts]
    inputs = _PROCESSOR(
        text=cleaned,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=77,
    ).to(_DEVICE)
    with torch.no_grad():
        features = _l2_normalise(_MODEL.get_text_features(**inputs))
    return features.cpu().numpy().astype(np.float32, copy=False)


def pool_frames(frame_embeddings: np.ndarray) -> np.ndarray:
    """Mean-pool ``(K, 512)`` frame vectors into one unit ``(512,)`` clip vector."""
    if frame_embeddings.size == 0:
        return np.zeros(_DIM, dtype=np.float32)
    mean = frame_embeddings.mean(axis=0)
    norm = float(np.linalg.norm(mean))
    if norm < 1e-8:
        return np.zeros(_DIM, dtype=np.float32)
    return (mean / norm).astype(np.float32, copy=False)
