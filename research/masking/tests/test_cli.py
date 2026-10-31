from pathlib import Path
from types import SimpleNamespace

import pytest

import maskbench.cli as cli
from maskbench.cli import build_parser


def test_cli_requires_a_subcommand() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_run_requires_a_known_method() -> None:
    parser = build_parser()
    args = parser.parse_args(["run", "--method", "apple-vision"])
    assert args.command == "run"
    assert args.method == "apple-vision"


def test_run_rejects_unknown_method() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["run", "--method", "made-up"])


def test_main_dispatches_report_command(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    called: list[Path] = []
    monkeypatch.setattr(cli, "load_config", lambda path: SimpleNamespace(project_root=tmp_path))
    monkeypatch.setattr(cli, "build_review", lambda project: called.append(project) or {})
    monkeypatch.setattr("sys.argv", ["maskbench", "--config", "benchmark.json", "report"])

    assert cli.main() == 0
    assert called == [tmp_path]
