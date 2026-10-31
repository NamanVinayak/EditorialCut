from dataclasses import dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlparse


@dataclass(frozen=True)
class VerificationReport:
    checked: int
    failures: tuple[str, ...]


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"src", "href"} and value:
                self.links.append(value)


def _verify_media(path: Path) -> str | None:
    if path.stat().st_size == 0:
        return f"Empty media file: {path}"
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return f"Undecodable media file: {path}: {completed.stderr.strip()}"
    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return f"Invalid ffprobe response for {path}: {exc}"
    if not any(stream.get("codec_type") == "video" for stream in data.get("streams", [])):
        return f"No video stream found: {path}"
    return None


def _verify_html_links(path: Path) -> list[str]:
    parser = _LinkParser()
    parser.feed(path.read_text())
    failures = []
    for link in parser.links:
        parsed = urlparse(link)
        if parsed.scheme in {"http", "https", "data", "javascript"} or link.startswith("#"):
            continue
        target = (path.parent / unquote(parsed.path)).resolve()
        if not target.exists():
            failures.append(f"Missing HTML link from {path}: {link}")
    return failures


def verify_results(root: Path) -> VerificationReport:
    root = root.resolve()
    failures: list[str] = []
    checked = 0
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        suffix = path.suffix.lower()
        if suffix in {".mp4", ".jpg", ".jpeg", ".png"}:
            checked += 1
            failure = _verify_media(path)
            if failure:
                failures.append(failure)
        elif suffix == ".json":
            checked += 1
            try:
                json.loads(path.read_text())
            except (OSError, json.JSONDecodeError) as exc:
                failures.append(f"Invalid JSON file {path}: {exc}")
        elif suffix == ".html":
            checked += 1
            failures.extend(_verify_html_links(path))
    return VerificationReport(checked=checked, failures=tuple(failures))
