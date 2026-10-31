import json
import sys
from pathlib import Path

from maskbench.execute import run_measured


def test_run_measured_preserves_logs_and_metrics(tmp_path: Path) -> None:
    stdout = tmp_path / "stdout.log"
    stderr = tmp_path / "stderr.log"
    metrics = tmp_path / "metrics.json"

    result = run_measured(
        [
            sys.executable,
            "-c",
            "import sys; print('hello'); print('warning', file=sys.stderr)",
        ],
        cwd=tmp_path,
        stdout_path=stdout,
        stderr_path=stderr,
        metrics_path=metrics,
    )

    assert result.returncode == 0
    assert result.wall_seconds >= 0
    assert result.peak_rss_bytes is None or result.peak_rss_bytes > 0
    assert stdout.read_text().strip() == "hello"
    assert stderr.read_text().strip() == "warning"
    stored = json.loads(metrics.read_text())
    assert stored["argv"][0] == sys.executable
    assert stored["returncode"] == 0


def test_run_measured_records_failure_without_raising(tmp_path: Path) -> None:
    result = run_measured(
        [sys.executable, "-c", "raise SystemExit(7)"],
        cwd=tmp_path,
        stdout_path=tmp_path / "stdout.log",
        stderr_path=tmp_path / "stderr.log",
        metrics_path=tmp_path / "metrics.json",
    )

    assert result.returncode == 7
