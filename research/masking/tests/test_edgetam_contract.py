import importlib.util
from pathlib import Path

import numpy as np
import pytest


PROJECT = Path(__file__).resolve().parents[1]
BACKEND = PROJECT / "backends/edgetam/run.py"


def load_backend():
    spec = importlib.util.spec_from_file_location("edgetam_backend", BACKEND)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validate_box_accepts_ordered_normalized_box() -> None:
    backend = load_backend()
    assert backend.validate_box([0.30, 0.01, 0.70, 0.99]) == (0.30, 0.01, 0.70, 0.99)


def test_validate_box_rejects_out_of_range_values() -> None:
    backend = load_backend()
    with pytest.raises(ValueError, match="normalized"):
        backend.validate_box([0.30, 0.01, 1.20, 0.99])


def test_binary_mask_contains_only_zero_and_255() -> None:
    backend = load_backend()
    logits = np.array([[-1.0, 0.0], [0.1, 5.0]], dtype=np.float32)
    mask = backend.logits_to_mask(logits)
    assert mask.dtype == np.uint8
    assert set(np.unique(mask)) == {0, 255}
