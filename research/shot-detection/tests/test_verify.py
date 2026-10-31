from pathlib import Path

from shotbench.verify import verify_results


def test_verify_results_reports_empty_media(tmp_path: Path) -> None:
    (tmp_path / "empty.mp4").touch()

    report = verify_results(tmp_path)

    assert report.failures
    assert "empty.mp4" in report.failures[0]


def test_verify_results_reports_missing_html_link(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text('<video src="missing.mp4"></video>')

    report = verify_results(tmp_path)

    assert any("missing.mp4" in failure for failure in report.failures)


def test_verify_results_accepts_valid_json(tmp_path: Path) -> None:
    (tmp_path / "result.json").write_text('{"ok": true}')

    report = verify_results(tmp_path)

    assert report.checked == 1
    assert report.failures == ()

