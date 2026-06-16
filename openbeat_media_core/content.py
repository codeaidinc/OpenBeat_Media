"""Public article model and Markdown front-matter read/write (no dependencies).

File format (content/<slug>.md):

    ---
    title: Export controls on semiconductor materials
    beat: science-tech
    author: Editorial
    tags: semiconductors, export controls
    sources: https://www.meti.go.jp/example
    published_at: 2026-06-14T09:00:00Z
    lang: en
    translation_key: semiconductor-export   # optional: groups translations (else derived from slug)
    ---
    Body (Markdown)...

Sources are required (source traceability). The body is Markdown. If the `markdown`
package is available it is used; otherwise a minimal fallback (paragraphs, headings,
links, lists) is used.
"""
from __future__ import annotations

import html
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

_LIST_KEYS = {"tags", "sources"}


def slugify(s: str, fallback: str = "article") -> str:
    # Keep ASCII alphanumerics and CJK/kana so non-Latin titles still produce a usable slug.
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9぀-ヿ一-鿿ぁ-んァ-ヶ]+", "-", s).strip("-")
    return s or fallback


@dataclass
class Article:
    slug: str
    title: str
    body_md: str = ""
    summary: str = ""
    beat: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)
    author: str = ""
    sources: List[str] = field(default_factory=list)
    published_at: str = ""
    lang: str = "en"
    translation_key: str = ""    # optional: groups translations across editions
    body_is_html: bool = False   # True = treat body_md as ready HTML (integration use)

    def __post_init__(self):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.published_at:
            self.published_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    @property
    def body_html(self) -> str:
        return self.body_md if self.body_is_html else md_to_html(self.body_md)

    @property
    def teaser(self) -> str:
        if self.summary:
            return self.summary
        text = re.sub(r"<[^>]+>", "", self.body_html)
        return (text[:160] + "…") if len(text) > 160 else text


# --- front-matter parse / serialize -------------------------------------
def load_article(path: str) -> Article:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    meta, body = _split_front_matter(raw)
    slug = meta.get("slug") or slugify(meta.get("title", ""),
                                       os.path.splitext(os.path.basename(path))[0])
    return Article(
        slug=slug, title=meta.get("title", ""), body_md=body,
        summary=meta.get("summary", ""), beat=meta.get("beat", ""),
        category=meta.get("category", ""), tags=_as_list(meta.get("tags")),
        author=meta.get("author", ""), sources=_as_list(meta.get("sources")),
        published_at=meta.get("published_at", ""), lang=meta.get("lang", "en"),
        translation_key=meta.get("translation_key", ""),
    )


def dump_article(a: Article) -> str:
    lines = ["---"]
    lines.append(f"title: {a.title}")
    if a.summary:
        lines.append(f"summary: {a.summary}")
    if a.beat:
        lines.append(f"beat: {a.beat}")
    if a.category:
        lines.append(f"category: {a.category}")
    if a.author:
        lines.append(f"author: {a.author}")
    if a.tags:
        lines.append("tags: " + ", ".join(a.tags))
    lines.append("sources: " + ", ".join(a.sources))
    lines.append(f"published_at: {a.published_at}")
    lines.append(f"slug: {a.slug}")
    lines.append(f"lang: {a.lang}")
    if a.translation_key:
        lines.append(f"translation_key: {a.translation_key}")
    lines.append("---")
    lines.append("")
    lines.append(a.body_md.rstrip() + "\n")
    return "\n".join(lines)


def load_dir(content_dir: str) -> List[Article]:
    arts = []
    if not os.path.isdir(content_dir):
        return arts
    for name in sorted(os.listdir(content_dir)):
        if name.endswith(".md"):
            arts.append(load_article(os.path.join(content_dir, name)))
    arts.sort(key=lambda a: a.published_at, reverse=True)
    return arts


def _split_front_matter(raw: str):
    raw = raw.lstrip("﻿")  # strip BOM
    if raw.startswith("---"):
        parts = raw.split("\n", 1)[1] if "\n" in raw else ""
        end = parts.find("\n---")
        if end != -1:
            block = parts[:end]
            body = parts[end + 4:].lstrip("\n")
            return _parse_kv(block), body
    return {}, raw


def _parse_kv(block: str) -> dict:
    meta = {}
    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def _as_list(v) -> List[str]:
    if not v:
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return [p.strip() for p in str(v).split(",") if p.strip()]


# --- Markdown -> HTML ---------------------------------------------------
def md_to_html(md: str) -> str:
    """Use the `markdown` package if available, else a minimal fallback."""
    try:  # pragma: no cover - environment dependent
        import markdown as _md
        return _md.markdown(md or "", extensions=["extra"])
    except Exception:
        return _fallback_md(md or "")


def _fallback_md(md: str) -> str:
    """Dependency-free minimal Markdown (headings / paragraphs / links / lists)."""
    out = []
    for block in re.split(r"\n\s*\n", md.strip()):
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            level = len(block) - len(block.lstrip("#"))
            text = _inline(block.lstrip("#").strip())
            out.append(f"<h{min(level,6)}>{text}</h{min(level,6)}>")
            continue
        if all(l.lstrip().startswith(("-", "*")) for l in block.splitlines()):
            items = "".join(f"<li>{_inline(l.lstrip()[1:].strip())}</li>"
                            for l in block.splitlines())
            out.append(f"<ul>{items}</ul>")
            continue
        out.append(f"<p>{_inline(block)}</p>")
    return "".join(out)


def _inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
                  r'<a href="\2" rel="noopener">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text
