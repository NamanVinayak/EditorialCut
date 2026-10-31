from dataclasses import dataclass
from html import escape
import json
from pathlib import Path
from statistics import median
from typing import Iterable


@dataclass(frozen=True)
class CandidateVote:
    detector: str
    frame: int
    score: float | None = None


@dataclass(frozen=True)
class CandidateGroup:
    frame: int
    votes: tuple[CandidateVote, ...]


def cluster_votes(
    votes: Iterable[CandidateVote],
    tolerance_frames: int = 1,
) -> tuple[CandidateGroup, ...]:
    if tolerance_frames < 0:
        raise ValueError("tolerance_frames cannot be negative")
    working: list[list[CandidateVote]] = []
    for vote in sorted(votes, key=lambda item: (item.frame, item.detector)):
        if working:
            current = working[-1]
            current_detectors = {item.detector for item in current}
            representative = round(median(item.frame for item in current))
            if (
                abs(vote.frame - representative) <= tolerance_frames
                and vote.detector not in current_detectors
            ):
                current.append(vote)
                continue
        working.append([vote])
    return tuple(
        CandidateGroup(
            frame=round(median(vote.frame for vote in group)),
            votes=tuple(group),
        )
        for group in working
    )


def _candidate_card(video_id: str, candidate: dict[str, object]) -> str:
    key = f"{video_id}:{candidate['index']}"
    votes = ", ".join(str(vote) for vote in candidate["votes"])
    choices = "".join(
        f'<label><input type="radio" name="{escape(key)}" value="{value}"> {label}</label>'
        for value, label in (
            ("hard_cut", "Real cut"),
            ("transition", "Transition"),
            ("false_detection", "False detection"),
            ("unsure", "Unsure"),
        )
    )
    return f"""
    <article class="candidate" data-key="{escape(key)}">
      <div class="candidate-heading">
        <h4>Boundary {int(candidate['index']):03d} — {float(candidate['seconds']):.3f}s</h4>
        <span>Frame {int(candidate['frame'])} · Votes: {escape(votes)}</span>
      </div>
      <video controls preload="metadata" src="{escape(str(candidate['clip']))}"></video>
      <div class="stills">
        <figure><img loading="lazy" src="{escape(str(candidate['before']))}"><figcaption>Frame before</figcaption></figure>
        <figure><img loading="lazy" src="{escape(str(candidate['after']))}"><figcaption>Frame after</figcaption></figure>
      </div>
      <div class="choices">{choices}</div>
      <input class="note" type="text" placeholder="Optional note, e.g. flash begins here">
    </article>
    """


def render_review_page(videos: list[dict[str, object]], output_path: Path) -> str:
    sections = []
    for video in videos:
        video_id = str(video["video_id"])
        cards = "".join(
            _candidate_card(video_id, candidate)
            for candidate in video["candidates"]
        )
        scene_links = "".join(
            f'<li><a href="{escape(str(scene))}">{escape(Path(str(scene)).name)}</a></li>'
            for scene in video["scenes"]
        )
        sections.append(
            f"""
            <section class="video-section" id="{escape(video_id)}">
              <h2>{escape(video_id)}</h2>
              <p class="use-case">{escape(str(video['use_case']))}</p>
              <details><summary>Play the complete original</summary>
                <video controls preload="metadata" src="{escape(str(video['source']))}"></video>
              </details>
              <details><summary>Open the primary isolated scenes ({len(video['scenes'])})</summary>
                <ol class="scene-list">{scene_links}</ol>
              </details>
              <p><strong>Possible missed cuts:</strong> add timecodes here if every detector missed something.</p>
              <textarea class="missed" data-video="{escape(video_id)}" placeholder="Example: 00:12.450 — real cut was missed"></textarea>
              <h3>Candidate boundaries ({len(video['candidates'])})</h3>
              {cards}
            </section>
            """
        )

    page_data = json.dumps(
        {
            "schema_version": 1,
            "review_page": output_path.name,
            "video_ids": [str(video["video_id"]) for video in videos],
        }
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Shot Detection Review</title>
  <style>
    :root {{ color-scheme: dark; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    body {{ max-width: 1100px; margin: 0 auto; padding: 28px; background: #111; color: #f4f4f4; }}
    header {{ position: sticky; top: 0; z-index: 4; background: rgba(17,17,17,.96); padding: 10px 0 16px; border-bottom: 1px solid #444; }}
    nav a {{ color: #9ac8ff; margin-right: 14px; }}
    button {{ background: #f4f4f4; color: #111; border: 0; border-radius: 7px; padding: 10px 14px; font-weight: 700; cursor: pointer; }}
    .video-section {{ margin: 52px 0; }}
    .use-case {{ font-size: 1.08rem; color: #d0d0d0; }}
    video {{ display: block; width: 100%; max-height: 620px; background: #000; margin: 12px 0; }}
    .candidate {{ border: 1px solid #3d3d3d; border-radius: 12px; padding: 18px; margin: 24px 0; background: #1a1a1a; }}
    .candidate-heading {{ display: flex; gap: 14px; justify-content: space-between; align-items: baseline; flex-wrap: wrap; }}
    .candidate-heading h4 {{ margin: 0; }}
    .candidate-heading span {{ color: #bbb; }}
    .stills {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
    figure {{ margin: 0; }} img {{ width: 100%; height: auto; }} figcaption {{ color: #bbb; }}
    .choices {{ display: flex; flex-wrap: wrap; gap: 18px; margin: 14px 0; }}
    .note, textarea {{ width: 100%; box-sizing: border-box; background: #262626; color: #fff; border: 1px solid #555; border-radius: 6px; padding: 9px; }}
    textarea {{ min-height: 70px; }}
    .scene-list {{ columns: 2; }} .scene-list a {{ color: #9ac8ff; }}
    .saved {{ color: #8ee39d; margin-left: 12px; }}
    @media (max-width: 700px) {{ .stills {{ grid-template-columns: 1fr; }} .scene-list {{ columns: 1; }} }}
  </style>
</head>
<body>
  <header>
    <h1>Shot Detection Review</h1>
    <p>Judge the edit, not the software. For every proposed boundary, play the short clip and choose what actually happened.</p>
    <button id="download">Download review JSON</button><span class="saved" id="saved"></span>
    <nav>{''.join(f'<a href="#{escape(str(video["video_id"]))}">{escape(str(video["video_id"]))}</a>' for video in videos)}</nav>
  </header>
  {''.join(sections)}
  <script>
    const PAGE = {page_data};
    const STORAGE_KEY = 'EditorialCut-shotbench-review-v1';
    let state = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{"decisions":{{}},"missed":{{}}}}');
    function save() {{
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      document.getElementById('saved').textContent = 'Saved in this browser';
    }}
    document.querySelectorAll('.candidate').forEach(card => {{
      const key = card.dataset.key;
      const prior = state.decisions[key];
      if (prior) {{
        const radio = card.querySelector(`input[value="${{prior.decision}}"]`);
        if (radio) radio.checked = true;
        card.querySelector('.note').value = prior.note || '';
      }}
      card.querySelectorAll('input[type="radio"]').forEach(input => input.addEventListener('change', () => {{
        state.decisions[key] = {{ decision: input.value, note: card.querySelector('.note').value }};
        save();
      }}));
      card.querySelector('.note').addEventListener('input', event => {{
        state.decisions[key] = state.decisions[key] || {{ decision: 'unsure' }};
        state.decisions[key].note = event.target.value;
        save();
      }});
    }});
    document.querySelectorAll('.missed').forEach(area => {{
      area.value = state.missed[area.dataset.video] || '';
      area.addEventListener('input', event => {{ state.missed[area.dataset.video] = event.target.value; save(); }});
    }});
    document.getElementById('download').addEventListener('click', () => {{
      const payload = {{ ...PAGE, exported_at: new Date().toISOString(), ...state }};
      const blob = new Blob([JSON.stringify(payload, null, 2)], {{ type: 'application/json' }});
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'shot-detection-review.json';
      link.click();
      URL.revokeObjectURL(link.href);
    }});
  </script>
</body>
</html>
"""


def write_review_page(videos: list[dict[str, object]], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_review_page(videos, output_path))
    return output_path
