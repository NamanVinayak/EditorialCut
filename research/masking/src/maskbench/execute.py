from __future__ import annotations

import json
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import psutil


@dataclass(frozen=True)
class CompletedRun:
    argv: tuple[str, ...]
    returncode: int
    wall_seconds: float
    peak_rss_bytes: int | None


def _rss_tree(process: psutil.Process) -> int | None:
    total = 0
    found = False
    for item in (process, *process.children(recursive=True)):
        try:
            total += item.memory_info().rss
            found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return total if found else None


def run_measured(
    argv: Sequence[str | Path],
    *,
    cwd: Path,
    stdout_path: Path,
    stderr_path: Path,
    metrics_path: Path,
) -> CompletedRun:
    normalized = tuple(str(item) for item in argv)
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    peak: int | None = None
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        process = subprocess.Popen(normalized, cwd=cwd, stdout=stdout, stderr=stderr)
        tracked = psutil.Process(process.pid)
        while process.poll() is None:
            sample = _rss_tree(tracked)
            if sample is not None:
                peak = sample if peak is None else max(peak, sample)
            time.sleep(0.02)
        returncode = process.returncode
    wall = time.perf_counter() - started
    result = CompletedRun(
        argv=normalized,
        returncode=returncode,
        wall_seconds=wall,
        peak_rss_bytes=peak,
    )
    metrics_path.write_text(json.dumps(asdict(result), indent=2) + "\n")
    return result
