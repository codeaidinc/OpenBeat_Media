"""RSS 2.0 / Atom 1.0 feed generation (deterministic, no dependencies).

Sources are kept in each item's summary. The sources label is localizable
(``sources_label``) so each edition's feed matches its language.
"""
from __future__ import annotations

from datetime import datetime, timezone
from email.utils import format_datetime
from typing import List
from xml.sax.saxutils import escape

from .content import Article


def _parse_dt(s: str) -> datetime:
    try:
        dt = datetime.fromisoformat((s or "").replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


def _summary(a: Article, sources_label: str = "Sources") -> str:
    base = a.teaser
    if a.sources:
        base += f" | {sources_label}: " + " ".join(a.sources)
    return base


def build_rss(articles: List[Article], *, title: str, site_url: str = "",
              sources_label: str = "Sources") -> str:
    items = []
    for a in articles:
        dt = _parse_dt(a.published_at)
        link = f"{site_url.rstrip('/')}/article/{a.slug}.html" if site_url else ""
        items.append(
            "<item>"
            f"<title>{escape(a.title)}</title>"
            + (f"<link>{escape(link)}</link>" if link else "")
            + f"<guid isPermaLink=\"false\">{escape(a.slug)}</guid>"
            f"<pubDate>{format_datetime(dt)}</pubDate>"
            f"<description>{escape(_summary(a, sources_label))}</description>"
            "</item>"
        )
    chan_link = f"<link>{escape(site_url)}</link>" if site_url else ""
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<rss version="2.0"><channel>'
            f"<title>{escape(title)}</title>{chan_link}"
            f"<description>{escape(title)}</description>"
            + "".join(items) + "</channel></rss>")


def build_atom(articles: List[Article], *, title: str, site_url: str = "",
               sources_label: str = "Sources") -> str:
    updated = max((_parse_dt(a.published_at) for a in articles),
                  default=datetime(1970, 1, 1, tzinfo=timezone.utc))
    entries = []
    for a in articles:
        dt = _parse_dt(a.published_at)
        link = f"{site_url.rstrip('/')}/article/{a.slug}.html" if site_url else ""
        entries.append(
            "<entry>"
            f"<title>{escape(a.title)}</title>"
            f"<id>{escape(a.slug)}</id>"
            + (f'<link href="{escape(link)}"/>' if link else "")
            + f"<updated>{dt.isoformat()}</updated>"
            f"<summary>{escape(_summary(a, sources_label))}</summary>"
            "</entry>"
        )
    sl = f'<link rel="self" href="{escape(site_url.rstrip("/") + "/feed.xml")}"/>' if site_url else ""
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<feed xmlns="http://www.w3.org/2005/Atom">'
            f"<title>{escape(title)}</title><id>urn:openbeat:media</id>{sl}"
            f"<updated>{updated.isoformat()}</updated>"
            + "".join(entries) + "</feed>")


def build_feed(articles: List[Article], kind: str = "rss", **kw) -> str:
    return build_atom(articles, **kw) if kind == "atom" else build_rss(articles, **kw)
