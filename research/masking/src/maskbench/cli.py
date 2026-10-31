from __future__ import annotations

import argparse
import json
from pathlib import Path

from .composite import render_method_views
from .config import load_config
from .media import prepare_proxy
from .methods import run_apple_vision, run_edgetam, run_rvm
from .report import build_review
from .verify import verify_project


METHODS = ("apple-vision", "rvm", "edgetam")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="maskbench")
    parser.add_argument("--config", type=Path, default=Path("benchmark.json"))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("prepare")
    run = sub.add_parser("run")
    run.add_argument("--method", choices=METHODS, required=True)
    render = sub.add_parser("render")
    render.add_argument("--method", choices=(*METHODS, "all"), default="all")
    sub.add_parser("report")
    sub.add_parser("verify")
    sub.add_parser("all")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config = load_config(args.config)
    project = config.project_root
    frames = project / "results/prepared/frames"

    def require_prepared() -> None:
        count = len(list(frames.glob("frame_*.png"))) if frames.is_dir() else 0
        if count != config.expected_frames:
            parser.error(
                f"prepared frame sequence is missing or incomplete: "
                f"expected {config.expected_frames}, found {count}; run prepare first"
            )

    def run_method(method: str) -> dict:
        require_prepared()
        if method == "apple-vision":
            return run_apple_vision(project, frames, config.expected_frames)
        if method == "rvm":
            return run_rvm(project, frames, config.expected_frames)
        return run_edgetam(project, frames, config.expected_frames, config.prompt_box)

    if args.command == "prepare":
        result = prepare_proxy(config, config.results_root)
        print(json.dumps({"proxy": str(result.proxy), "frames": result.frame_count}, indent=2))
    elif args.command == "run":
        print(json.dumps(run_method(args.method), indent=2))
    elif args.command == "render":
        require_prepared()
        method_ids = METHODS if args.method == "all" else (args.method,)
        print(json.dumps([render_method_views(project, config, item) for item in method_ids], indent=2))
    elif args.command == "report":
        result = build_review(project)
        print(json.dumps({key: str(value) for key, value in result.items()}, indent=2))
    elif args.command == "verify":
        result = verify_project(project)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "passed" else 1
    elif args.command == "all":
        prepare_proxy(config, config.results_root)
        for method in METHODS:
            run_method(method)
            render_method_views(project, config, method)
        build_review(project)
        result = verify_project(project)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "passed" else 1
    return 0
