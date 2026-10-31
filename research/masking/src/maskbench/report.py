from __future__ import annotations

import html
import json
import os
from pathlib import Path
from typing import Any


METHOD_LABELS = {
    "apple-vision": "Apple Vision",
    "rvm": "Robust Video Matting",
    "edgetam": "EdgeTAM",
}

VIEW_LABELS = {
    "graphic_behind": "Graphic behind subject",
    "checkerboard_cutout": "Cutout on checkerboard",
    "mask": "Matte only",
    "edge_diagnostics": "Edge diagnostics",
    "comparison": "Original / result split",
}


def _review_relative(path: Path, review_root: Path) -> str:
    return Path(os.path.relpath(path.resolve(), review_root.resolve())).as_posix()


def _load_method(project: Path, run_path: Path, review_root: Path) -> dict[str, Any]:
    run = json.loads(run_path.read_text())
    method_id = str(run["method"])
    media_manifest_path = project / f"results/media/{method_id}/artifacts.json"
    media: dict[str, str] = {}
    kind = "unknown"
    if media_manifest_path.is_file():
        manifest = json.loads(media_manifest_path.read_text())
        kind = str(manifest.get("kind", "unknown"))
        for view, value in manifest.get("media", {}).items():
            candidate = Path(value)
            if not candidate.is_absolute():
                candidate = project / candidate
            media[str(view)] = _review_relative(candidate, review_root)
    return {
        "id": method_id,
        "label": METHOD_LABELS.get(method_id, method_id),
        "status": run.get("status", "unknown"),
        "job": run.get("required_input", "not recorded"),
        "kind": kind,
        "wall_seconds": run.get("wall_seconds"),
        "peak_rss_bytes": run.get("peak_rss_bytes"),
        "warnings": run.get("warnings", []),
        "error": run.get("exact_error"),
        "media": media,
    }


def _method_cards(methods: list[dict[str, Any]]) -> str:
    cards: list[str] = []
    for method in methods:
        method_id = html.escape(method["id"])
        label = html.escape(method["label"])
        if method["status"] == "success":
            video = (
                f'<video id="video-{method_id}" class="method-video" muted playsinline '
                f'preload="metadata" data-method="{method_id}"></video>'
            )
            state = '<span class="status success">Tracked all 600 frames</span>'
        else:
            error = html.escape(str(method.get("error") or "No exact error recorded"))
            video = f'<div class="failed"><strong>Method failed</strong><p>{error}</p></div>'
            state = '<span class="status failed-status">Failed</span>'
        seconds = method.get("wall_seconds")
        runtime = f"{float(seconds):.1f}s" if seconds is not None else "—"
        memory_value = method.get("peak_rss_bytes")
        memory = f"{float(memory_value) / 1_000_000_000:.2f} GB" if memory_value else "—"
        job = html.escape(str(method.get("job", "not recorded")))
        kind = "Soft alpha" if method.get("kind") == "alpha" else "Hard binary mask"
        warnings = method.get("warnings") or []
        warning_html = "".join(f"<li>{html.escape(str(item))}</li>" for item in warnings)
        cards.append(
            f"""
            <article class="method-card" data-method-card="{method_id}">
              <div class="method-heading">
                <div><p class="eyebrow">{html.escape(kind)}</p><h2>{label}</h2></div>
                {state}
              </div>
              <div class="video-shell">{video}</div>
              <dl class="facts">
                <div><dt>Job</dt><dd>{job}</dd></div>
                <div><dt>20-second run</dt><dd>{runtime}</dd></div>
                <div><dt>Peak memory</dt><dd>{memory}</dd></div>
              </dl>
              {f'<details><summary>Known technical caveats</summary><ul>{warning_html}</ul></details>' if warnings else ''}
            </article>
            """
        )
    return "\n".join(cards)


def _ratings(methods: list[dict[str, Any]]) -> str:
    criteria = (
        ("overall", "Overall usefulness"),
        ("hair", "Hair and fine edges"),
        ("hands", "Hands and fast movement"),
        ("shoulders_mic", "Shoulders and microphone"),
        ("flicker", "Temporal steadiness"),
        ("tracking", "Graphic stays behind subject"),
    )
    sections: list[str] = []
    for method in methods:
        method_id = html.escape(method["id"])
        label = html.escape(method["label"])
        if method["status"] != "success":
            continue
        rows = []
        for key, title in criteria:
            options = '<option value="">Not rated</option>' + "".join(
                f'<option value="{value}">{value} — {text}</option>'
                for value, text in (
                    (1, "Unusable"),
                    (2, "Major fixes"),
                    (3, "Usable with cleanup"),
                    (4, "Good"),
                    (5, "Excellent"),
                )
            )
            rows.append(
                f'<label class="rating-row"><span>{html.escape(title)}</span>'
                f'<select data-rating data-method="{method_id}" data-criterion="{key}">{options}</select></label>'
            )
        sections.append(
            f"""
            <section class="rating-card">
              <h3>{label}</h3>
              {''.join(rows)}
              <label class="notes-label">What did you notice?
                <textarea data-notes data-method="{method_id}" rows="4" placeholder="Example: hair looks good, but the right hand disappears at 00:12..."></textarea>
              </label>
            </section>
            """
        )
    return "\n".join(sections)


def _html_document(data: dict[str, Any]) -> str:
    encoded = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    cards = _method_cards(data["methods"])
    ratings = _ratings(data["methods"])
    view_buttons = "".join(
        f'<button class="view-button{" active" if key == "graphic_behind" else ""}" '
        f'data-view="{key}">{html.escape(label)}</button>'
        for key, label in VIEW_LABELS.items()
    )
    errors = " ".join(
        html.escape(str(method.get("error") or ""))
        for method in data["methods"]
        if method["status"] != "success"
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mask Tracking Review</title>
  <style>
    :root {{ color-scheme: dark; --ink:#f5f3ee; --muted:#aaa9a4; --panel:#181a1d; --line:#30343a; --cyan:#14dbe4; --pink:#ff42c8; --green:#72df91; --red:#ff766d; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:#0b0c0e; color:var(--ink); font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    button,select,textarea,input {{ font:inherit; }}
    .page {{ width:min(1760px,calc(100% - 40px)); margin:0 auto; padding:48px 0 100px; }}
    .hero {{ display:grid; grid-template-columns:minmax(0,1.5fr) minmax(280px,.7fr); gap:32px; align-items:end; margin-bottom:34px; }}
    .eyebrow {{ margin:0 0 8px; color:var(--cyan); font-size:12px; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }}
    h1 {{ margin:0; font-size:clamp(38px,6vw,78px); line-height:.95; letter-spacing:-.055em; }}
    .lede {{ margin:20px 0 0; color:#d2d0ca; font-size:18px; line-height:1.55; max-width:880px; }}
    .callout {{ border:1px solid #315459; background:#10272a; padding:20px; border-radius:16px; color:#d9ffff; line-height:1.5; }}
    .controls {{ position:sticky; z-index:5; top:0; background:rgba(11,12,14,.93); backdrop-filter:blur(16px); border:1px solid var(--line); border-radius:18px; padding:14px; margin-bottom:22px; }}
    .view-buttons,.transport {{ display:flex; flex-wrap:wrap; gap:9px; align-items:center; }}
    .transport {{ margin-top:12px; }}
    button {{ border:1px solid var(--line); border-radius:999px; padding:10px 15px; color:var(--ink); background:#202329; cursor:pointer; }}
    button:hover,button.active {{ border-color:var(--cyan); background:#123a3d; }}
    #timeline {{ flex:1; min-width:240px; accent-color:var(--cyan); }}
    #timecode {{ min-width:92px; color:var(--muted); font-variant-numeric:tabular-nums; }}
    .methods {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px; }}
    .method-card,.rating-card,.decision {{ border:1px solid var(--line); background:var(--panel); border-radius:18px; padding:16px; min-width:0; }}
    .method-heading {{ min-height:76px; display:flex; justify-content:space-between; gap:12px; align-items:flex-start; }}
    h2 {{ margin:0; font-size:24px; letter-spacing:-.03em; }}
    .status {{ white-space:nowrap; border-radius:999px; padding:7px 10px; font-size:11px; font-weight:800; }}
    .success {{ color:#baffca; background:#173e25; }} .failed-status {{ color:#ffd1cd; background:#51201c; }}
    .video-shell {{ aspect-ratio:16/9; overflow:hidden; background:#050505; border-radius:12px; display:grid; place-items:center; }}
    video {{ width:100%; height:100%; object-fit:contain; }}
    .failed {{ padding:24px; color:#ffd1cd; }}
    .facts {{ display:grid; gap:9px; margin:15px 0 0; }}
    .facts div {{ display:grid; grid-template-columns:105px 1fr; gap:10px; border-top:1px solid #292c31; padding-top:9px; }}
    dt {{ color:var(--muted); }} dd {{ margin:0; line-height:1.35; }}
    details {{ margin-top:14px; color:var(--muted); }} details li {{ margin:6px 0; }}
    .guide {{ margin:54px 0 20px; display:flex; gap:20px; justify-content:space-between; align-items:end; }}
    .guide h2 {{ font-size:34px; }} .guide p {{ color:var(--muted); max-width:760px; margin:0; line-height:1.5; }}
    .rubric {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px; }}
    .rating-card h3 {{ font-size:22px; margin:0 0 14px; }}
    .rating-row {{ display:grid; grid-template-columns:1fr 175px; gap:12px; align-items:center; padding:10px 0; border-top:1px solid #2a2d32; }}
    select,textarea {{ width:100%; color:var(--ink); background:#0f1114; border:1px solid #3a3f46; border-radius:9px; padding:9px; }}
    .notes-label {{ display:block; color:var(--muted); margin-top:14px; }} textarea {{ display:block; margin-top:8px; resize:vertical; }}
    .decision {{ margin-top:18px; display:grid; grid-template-columns:1fr 1fr 2fr auto; gap:14px; align-items:end; }}
    .decision label {{ color:var(--muted); }} .decision select,.decision textarea {{ margin-top:7px; }}
    #save-state {{ color:var(--green); margin-left:10px; }}
    .footer-note {{ color:var(--muted); margin-top:20px; line-height:1.5; }}
    @media(max-width:1100px) {{ .methods,.rubric {{ grid-template-columns:1fr; }} .hero {{ grid-template-columns:1fr; }} .decision {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
<main class="page">
  <section class="hero">
    <div>
      <p class="eyebrow">20 seconds · 600 frames · fully local on M4 Pro</p>
      <h1>Mask Tracking Review</h1>
      <p class="lede">These are not single-frame masks. Each method followed the presenter through the entire shot. Judge the edit: hair, hands, microphone, edge flicker, and whether the cyan title convincingly travels behind the moving presenter.</p>
    </div>
    <aside class="callout"><strong>How to review</strong><br>Play all three together. Change the view without losing your place. Use edge diagnostics for close inspection, then score what you would actually accept in an edit.</aside>
  </section>

  <section class="controls" aria-label="Synchronized playback controls">
    <div class="view-buttons">{view_buttons}</div>
    <div class="transport">
      <button id="play">Play all</button><button id="back">−1 frame</button><button id="forward">+1 frame</button>
      <input id="timeline" type="range" min="0" max="20" step="0.033333" value="0">
      <span id="timecode">00:00.00</span>
    </div>
  </section>

  <section class="methods">{cards}</section>

  <section class="guide">
    <div><p class="eyebrow">Your editorial judgment</p><h2>Rate what survives real playback</h2></div>
    <p>A still can hide bad tracking. Scrub through hand movement and watch the silhouette during motion. “5” should mean you would use it without a manual roto pass.</p>
  </section>
  <section class="rubric">{ratings}</section>
  <section class="decision">
    <label>Best automatic presenter matte<select id="best-auto"><option value="">Choose after viewing</option><option value="apple-vision">Apple Vision</option><option value="rvm">Robust Video Matting</option><option value="none">Neither</option></select></label>
    <label>Best prompted tracked selection<select id="best-prompted"><option value="">Choose after viewing</option><option value="edgetam">EdgeTAM</option><option value="none">Not acceptable</option></select></label>
    <label>Overall decision<textarea id="overall-notes" rows="3" placeholder="What should we keep, reject, or retest?"></textarea></label>
    <div><button id="download">Download review JSON</button><span id="save-state">Saved in this browser</span></div>
  </section>
  <p class="footer-note">The methods perform different filmmaking jobs: Apple Vision and RVM automatically isolate a person; EdgeTAM begins from one box and tracks that selected subject. The test media is silent so all players stay synchronized. {errors}</p>
</main>
<script id="review-data" type="application/json">{encoded}</script>
<script>
const DATA = JSON.parse(document.getElementById('review-data').textContent);
const STORAGE_KEY = 'EditorialCut-mask-review-v1';
const videos = [...document.querySelectorAll('.method-video')];
const timeline = document.getElementById('timeline');
const play = document.getElementById('play');
let activeView = 'graphic_behind';
let syncing = false;

function sourceFor(video) {{
  const method = DATA.methods.find(item => item.id === video.dataset.method);
  return method && method.media[activeView];
}}
function setView(view) {{
  const time = Number(timeline.value || 0);
  const wasPlaying = videos.some(video => !video.paused);
  activeView = view;
  document.querySelectorAll('.view-button').forEach(button => button.classList.toggle('active', button.dataset.view === view));
  videos.forEach(video => {{ const src=sourceFor(video); if(src){{ video.src=src; video.load(); video.addEventListener('loadedmetadata',()=>{{video.currentTime=Math.min(time,video.duration||20); if(wasPlaying) video.play();}},{{once:true}}); }} }});
}}
function setTime(value) {{
  const target = Math.max(0,Math.min(20,Number(value)));
  syncing = true; timeline.value=target;
  videos.forEach(video => {{ if(video.readyState && Math.abs(video.currentTime-target)>.025) video.currentTime=target; }});
  const minutes=Math.floor(target/60).toString().padStart(2,'0'); const seconds=(target%60).toFixed(2).padStart(5,'0');
  document.getElementById('timecode').textContent=`${{minutes}}:${{seconds}}`;
  syncing = false;
}}
play.addEventListener('click', async () => {{
  if(videos.some(video=>!video.paused)) {{ videos.forEach(video=>video.pause()); play.textContent='Play all'; }}
  else {{ const t=Number(timeline.value); videos.forEach(video=>video.currentTime=t); await Promise.allSettled(videos.map(video=>video.play())); play.textContent='Pause all'; }}
}});
document.getElementById('back').addEventListener('click',()=>setTime(Number(timeline.value)-1/30));
document.getElementById('forward').addEventListener('click',()=>setTime(Number(timeline.value)+1/30));
timeline.addEventListener('input',()=>setTime(timeline.value));
document.querySelectorAll('.view-button').forEach(button=>button.addEventListener('click',()=>setView(button.dataset.view)));
if(videos[0]) videos[0].addEventListener('timeupdate',()=>{{ if(!syncing&&!videos[0].paused) setTime(videos[0].currentTime); }});
videos.forEach(video=>video.addEventListener('ended',()=>{{videos.forEach(item=>item.pause());play.textContent='Play all';}}));

function collect() {{
  const review={{schema_version:1,reviewed_at:new Date().toISOString(),active_view:activeView,ratings:{{}},notes:{{}},best_auto:document.getElementById('best-auto').value,best_prompted:document.getElementById('best-prompted').value,overall_notes:document.getElementById('overall-notes').value}};
  document.querySelectorAll('[data-rating]').forEach(el=>{{review.ratings[el.dataset.method]??={{}};review.ratings[el.dataset.method][el.dataset.criterion]=el.value?Number(el.value):null;}});
  document.querySelectorAll('[data-notes]').forEach(el=>review.notes[el.dataset.method]=el.value);
  return review;
}}
function save() {{ localStorage.setItem(STORAGE_KEY,JSON.stringify(collect())); document.getElementById('save-state').textContent='Saved in this browser'; }}
function restore() {{ const raw=localStorage.getItem(STORAGE_KEY); if(!raw)return; try{{const review=JSON.parse(raw);document.querySelectorAll('[data-rating]').forEach(el=>el.value=review.ratings?.[el.dataset.method]?.[el.dataset.criterion]??'');document.querySelectorAll('[data-notes]').forEach(el=>el.value=review.notes?.[el.dataset.method]??'');document.getElementById('best-auto').value=review.best_auto??'';document.getElementById('best-prompted').value=review.best_prompted??'';document.getElementById('overall-notes').value=review.overall_notes??'';}}catch(error){{console.warn(error);}} }}
document.querySelectorAll('select,textarea').forEach(el=>el.addEventListener('input',save));
document.getElementById('download').addEventListener('click',()=>{{const blob=new Blob([JSON.stringify(collect(),null,2)],{{type:'application/json'}});const url=URL.createObjectURL(blob);const anchor=document.createElement('a');anchor.href=url;anchor.download='masking-review.json';anchor.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}});
restore(); setView(activeView); setTime(0);
</script>
</body>
</html>
"""


def build_review(project: Path) -> dict[str, Path]:
    project = project.resolve()
    review_root = project / "results/review"
    review_root.mkdir(parents=True, exist_ok=True)
    methods = [
        _load_method(project, path, review_root)
        for path in sorted((project / "results/methods").glob("*/run.json"))
    ]
    methods.sort(key=lambda method: tuple(METHOD_LABELS).index(method["id"]) if method["id"] in METHOD_LABELS else 99)
    data = {
        "schema_version": 1,
        "title": "Mask Tracking Review",
        "duration_seconds": 20.0,
        "fps": 30,
        "expected_frames": 600,
        "source_proxy": _review_relative(project / "results/prepared/source-proxy.mp4", review_root),
        "methods": methods,
        "view_labels": VIEW_LABELS,
    }
    data_path = review_root / "review-data.json"
    html_path = review_root / "index.html"
    data_path.write_text(json.dumps(data, indent=2) + "\n")
    html_path.write_text(_html_document(data))
    launcher = review_root / "open-review.command"
    launcher.write_text(
        "#!/bin/zsh\n"
        "cd \"${0:A:h}\"\n"
        "python3 -m http.server 8765 >/tmp/editorialcut-mask-review.log 2>&1 &\n"
        "open http://127.0.0.1:8765/index.html\n"
    )
    launcher.chmod(0o755)
    return {"html": html_path, "data": data_path, "launcher": launcher}
