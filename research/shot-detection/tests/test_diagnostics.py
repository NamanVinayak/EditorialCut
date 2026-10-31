from shotbench.diagnostics import parse_scdet_log


def test_parse_scdet_log_extracts_score_and_time() -> None:
    log = """
[Parsed_scdet_0 @ 0x123] lavfi.scd.score: 10.499, lavfi.scd.time: 0.166834
[Parsed_scdet_0 @ 0x123] lavfi.scd.score: 28.676, lavfi.scd.time: 8.049716
"""

    events = parse_scdet_log(log, fps=24.0)

    assert len(events) == 2
    assert events[0].score == 10.499
    assert events[0].seconds == 0.166834
    assert events[0].frame == 4
    assert events[1].frame == 193


def test_parse_scdet_log_ignores_unrelated_ffmpeg_lines() -> None:
    events = parse_scdet_log("frame=  100 fps=0.0 q=-0.0", fps=30.0)

    assert events == ()

