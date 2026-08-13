#!/usr/bin/env python3
"""Extract public Xiaoyuzhou episode metadata from an episode page."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class PayloadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.current: str | None = None
        self.buffer: list[str] = []
        self.json_ld: list[str] = []
        self.next_data: list[str] = []
        self.meta: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "meta":
            key = values.get("property") or values.get("name")
            if key and values.get("content"):
                self.meta[key] = values["content"] or ""
        if tag != "script":
            return
        script_type = (values.get("type") or "").lower()
        script_id = values.get("id") or ""
        if script_type == "application/ld+json":
            self.current = "json_ld"
            self.buffer = []
        elif script_id == "__NEXT_DATA__":
            self.current = "next_data"
            self.buffer = []

    def handle_data(self, data: str) -> None:
        if self.current:
            self.buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "script" or not self.current:
            return
        payload = "".join(self.buffer).strip()
        if payload:
            getattr(self, self.current).append(payload)
        self.current = None
        self.buffer = []


def parse_duration(value: Any) -> int | None:
    if isinstance(value, (int, float)):
        return int(value)
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value)
    if not match:
        return None
    hours, minutes, seconds = (int(part or 0) for part in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def clean_text(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = re.sub(r"<[^>]+>", " ", html.unescape(value))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n\n", text)).strip()


def first(*values: Any) -> Any:
    return next((value for value in values if value not in (None, "", [])), None)


def load_json(raw_values: list[str]) -> list[Any]:
    parsed: list[Any] = []
    for raw in raw_values:
        try:
            parsed.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return parsed


def find_episode_ld(payloads: list[Any]) -> dict[str, Any]:
    queue = list(payloads)
    while queue:
        item = queue.pop(0)
        if isinstance(item, list):
            queue.extend(item)
        elif isinstance(item, dict):
            if item.get("@type") == "PodcastEpisode":
                return item
            graph = item.get("@graph")
            if isinstance(graph, list):
                queue.extend(graph)
    return {}


def get_nested(data: Any, *keys: str) -> Any:
    for key in keys:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


def normalize_url(value: str) -> tuple[str, str]:
    raw = value.strip()
    if re.fullmatch(r"[0-9a-fA-F]{24}", raw):
        episode_id = raw.lower()
        return f"https://www.xiaoyuzhoufm.com/episode/{episode_id}", episode_id
    parsed = urlparse(raw)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
        "xiaoyuzhoufm.com",
        "www.xiaoyuzhoufm.com",
    }:
        raise ValueError("Expected a public xiaoyuzhoufm.com episode URL or 24-character episode ID")
    match = re.search(r"/(?:episode|episodes)/([0-9a-fA-F]{24})(?:/|$)", parsed.path)
    if not match:
        raise ValueError("Could not find a 24-character Xiaoyuzhou episode ID in the URL")
    episode_id = match.group(1).lower()
    return f"https://www.xiaoyuzhoufm.com/episode/{episode_id}", episode_id


def fetch(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; media-archive-notebooklm/1.0)",
            "Referer": "https://www.xiaoyuzhoufm.com/",
        },
    )
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def extract(page: str, canonical_url: str, episode_id: str) -> dict[str, Any]:
    parser = PayloadParser()
    parser.feed(page)
    ld = find_episode_ld(load_json(parser.json_ld))
    next_payloads = load_json(parser.next_data)
    next_root = next_payloads[0] if next_payloads else {}
    episode = get_nested(next_root, "props", "pageProps", "episode") or {}
    podcast = episode.get("podcast") if isinstance(episode, dict) else {}
    podcast = podcast if isinstance(podcast, dict) else {}
    ld_media = ld.get("associatedMedia") if isinstance(ld.get("associatedMedia"), dict) else {}
    ld_series = ld.get("partOfSeries") if isinstance(ld.get("partOfSeries"), dict) else {}
    enclosure = episode.get("enclosure") if isinstance(episode.get("enclosure"), dict) else {}
    episode_image = episode.get("image") if isinstance(episode.get("image"), dict) else {}
    podcast_image = podcast.get("image") if isinstance(podcast.get("image"), dict) else {}

    if not ld and not episode and not parser.meta.get("og:audio"):
        raise ValueError("No Xiaoyuzhou episode payload found; the page may be private or its structure changed")

    pid = podcast.get("pid")
    result = {
        "episode_id": episode_id,
        "canonical_url": canonical_url,
        "title": first(ld.get("name"), episode.get("title"), parser.meta.get("og:title")),
        "podcast": first(ld_series.get("name"), podcast.get("title")),
        "podcast_url": first(
            ld_series.get("url"),
            f"https://www.xiaoyuzhoufm.com/podcast/{pid}" if pid else None,
        ),
        "author": podcast.get("author"),
        "published_at": first(ld.get("datePublished"), episode.get("pubDate")),
        "duration_seconds": first(parse_duration(episode.get("duration")), parse_duration(ld.get("timeRequired"))),
        "description": first(clean_text(ld.get("description")), clean_text(episode.get("shownotes"))),
        "audio_url": first(ld_media.get("contentUrl"), enclosure.get("url"), parser.meta.get("og:audio")),
        "cover_image": first(episode_image.get("picUrl"), podcast_image.get("picUrl"), parser.meta.get("og:image")),
        "play_count": episode.get("playCount"),
        "comment_count": episode.get("commentCount"),
        "favorite_count": episode.get("favoriteCount"),
        "subscriber_count": podcast.get("subscriptionCount"),
        "episode_count": podcast.get("episodeCount"),
    }
    return result


def markdown_card(data: dict[str, Any]) -> str:
    def display(value: Any) -> str:
        return "—" if value in (None, "") else str(value)

    rows = [
        ("标题", data.get("title")),
        ("播客", data.get("podcast")),
        ("主播/作者", data.get("author")),
        ("发布时间", data.get("published_at")),
        ("时长（秒）", data.get("duration_seconds")),
        ("播放", data.get("play_count")),
        ("订阅", data.get("subscriber_count")),
        ("节目链接", data.get("canonical_url")),
        ("音频链接", data.get("audio_url")),
    ]
    lines = ["| 字段 | 值 |", "|---|---|"]
    lines.extend(f"| {label} | {display(value)} |" for label, value in rows)
    return "\n".join(lines)


def main() -> int:
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument("episode", help="Xiaoyuzhou episode URL or 24-character ID")
    arg_parser.add_argument("--html", type=Path, help="Read saved HTML instead of fetching the page")
    arg_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = arg_parser.parse_args()
    try:
        canonical_url, episode_id = normalize_url(args.episode)
        page = args.html.read_text(encoding="utf-8") if args.html else fetch(canonical_url)
        data = extract(page, canonical_url, episode_id)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    if args.format == "markdown":
        print(markdown_card(data))
    else:
        print(json.dumps({"ok": True, "data": data}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
