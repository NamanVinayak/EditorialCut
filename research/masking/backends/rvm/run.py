from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image


def frame_paths(directory: Path) -> list[Path]:
    return sorted(directory.glob("frame_*.png"))


def alpha_to_uint8(alpha: np.ndarray) -> np.ndarray:
    return np.rint(np.clip(alpha, 0.0, 1.0) * 255.0).astype(np.uint8)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RVM frame-sequence adapter")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--vendor", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--variant", choices=("mobilenetv3", "resnet50"), default="mobilenetv3")
    parser.add_argument("--device", choices=("auto", "mps", "cpu"), default="auto")
    parser.add_argument("--downsample-ratio", type=float)
    return parser.parse_args()


def choose_device(requested: str, torch_module) -> str:
    if requested == "auto":
        return "mps" if torch_module.backends.mps.is_available() else "cpu"
    if requested == "mps" and not torch_module.backends.mps.is_available():
        raise RuntimeError("MPS was requested but is not available")
    return requested


def run_inference(args: argparse.Namespace) -> dict[str, object]:
    import torch
    from torchvision.transforms.functional import pil_to_tensor

    vendor = args.vendor.resolve()
    sys.path.insert(0, str(vendor))
    from model import MattingNetwork

    frames = frame_paths(args.input_dir)
    if not frames:
        raise RuntimeError("input directory contains no frame_*.png files")
    if not args.checkpoint.is_file():
        raise RuntimeError(f"checkpoint not found: {args.checkpoint}")
    device = choose_device(args.device, torch)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for old in args.output_dir.glob("frame_*.png"):
        old.unlink()

    model = MattingNetwork(args.variant).eval().to(device)
    state = torch.load(args.checkpoint, map_location=device, weights_only=True)
    model.load_state_dict(state)
    recurrent = [None] * 4
    started = time.perf_counter()
    native_size: list[int] | None = None

    with torch.inference_mode():
        for index, frame in enumerate(frames, start=1):
            with Image.open(frame) as image:
                rgb = image.convert("RGB")
                tensor = pil_to_tensor(rgb).float().div_(255).unsqueeze(0).unsqueeze(0)
            tensor = tensor.to(device)
            ratio = args.downsample_ratio
            if ratio is None:
                ratio = min(512 / max(tensor.shape[-2:]), 1.0)
            _, alpha, *recurrent = model(tensor, *recurrent, ratio)
            array = alpha[0, 0, 0].float().cpu().numpy()
            native_size = [int(array.shape[1]), int(array.shape[0])]
            Image.fromarray(alpha_to_uint8(array), mode="L").save(
                args.output_dir / frame.name
            )
            if index % 30 == 0:
                print(f"processed {index}/{len(frames)}", flush=True)

    if device == "mps":
        torch.mps.synchronize()
    return {
        "backend": "rvm",
        "variant": args.variant,
        "device_requested": args.device,
        "device_used": device,
        "processed_frames": len(frames),
        "native_size": native_size,
        "downsample_ratio": args.downsample_ratio,
        "wall_seconds_internal": time.perf_counter() - started,
        "torch_version": torch.__version__,
    }


def main() -> int:
    args = parse_args()
    metadata = run_inference(args)
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(json.dumps(metadata, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
