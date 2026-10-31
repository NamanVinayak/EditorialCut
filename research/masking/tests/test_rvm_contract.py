import importlib.util
from pathlib import Path

import numpy as np


PROJECT = Path(__file__).resolve().parents[1]
BACKEND = PROJECT / "backends/rvm/run.py"


def load_backend():
    spec = importlib.util.spec_from_file_location("rvm_backend", BACKEND)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_alpha_to_uint8_preserves_soft_values() -> None:
    backend = load_backend()
    alpha = np.array([[0.0, 0.25], [0.75, 1.0]], dtype=np.float32)

    converted = backend.alpha_to_uint8(alpha)

    assert converted.dtype == np.uint8
    assert converted.tolist() == [[0, 64], [191, 255]]


def test_frame_paths_are_sorted_and_filtered(tmp_path: Path) -> None:
    backend = load_backend()
    for name in ["frame_000003.png", "notes.txt", "frame_000001.png"]:
        (tmp_path / name).touch()

    assert [path.name for path in backend.frame_paths(tmp_path)] == [
        "frame_000001.png",
        "frame_000003.png",
    ]
