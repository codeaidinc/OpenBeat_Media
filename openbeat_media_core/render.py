"""Article -> static HTML (theme applied; Jinja2).

- render_site(articles, out_dir, ...) writes a single edition (one site).
- build_site(articles, out_dir, ...) writes one edition per language (domestic /
  international). Articles are split by their `lang`; each language is written to
  out_dir/<lang>/, with a root page that redirects to the primary language.
  Translated articles (matched by translation_key, or the language suffix of the
  slug) are cross-linked by a language switcher. A single language writes at the root.

The site chrome is localized per edition (English chrome for /en/, Japanese for /ja/)
via openbeat_media_core.i18n.SITE. `site` settings (title, logo, accent, font, hero =
slots for brand assets) are passed through to the theme.
"""
from __future__ import annotations

import os
import re
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .content import Article
from .feed import build_feed
from .i18n import site_ui

THEMES_ROOT = os.path.join(os.path.dirname(__file__), "themes")

LANG_LABELS = {
    "ja": "日本語", "en": "English", "fr": "Français", "de": "Deutsch",
    "es": "Español", "pt": "Português", "ko": "한국어", "zh": "中文",
    "vi": "Tiếng Việt", "th": "ไทย", "id": "Bahasa",
}
_LANG_SUFFIX = re.compile(r"-(en|ja|jp|fr|de|es|pt|ko|zh|vi|th|id)$", re.I)

DEFAULT_SITE = {
    "title": "OpenBeat Media",
    "tagline": "A publication of your own, with sources",
    "logo": "",            # logo image path / URL (empty = text nameplate)
    "hero": "",            # hero/banner image at the top of the front page
    "accent": "#b4532a",   # accent color (nameplate, rules, section headings, links)
    "font": 'system-ui, -apple-system, "Hiragino Sans", "Noto Sans JP", sans-serif',
    "base_url": "",        # e.g. https://media.example (for absolute feed URLs)
    "lang": "en",          # default language when an article has no `lang`
    "primary_lang": "",    # root redirect target for multi-edition builds (default: most articles)
    "beat_labels": {},     # optional: {"science-tech": "Science & Tech", ...}
    "lang_labels": {},     # optional: language code -> display name override
}


def _env(theme: str) -> Environment:
    theme_dir = os.path.join(THEMES_ROOT, theme)
    if not os.path.isdir(theme_dir):
        raise ValueError(f"theme not found: {theme}")
    return Environment(loader=FileSystemLoader(theme_dir),
                       autoescape=select_autoescape(["html"]))


def _related(article: Article, articles: List[Article], limit: int = 4) -> List[Article]:
    """Other articles in the same beat (newest first), up to `limit`."""
    if not article.beat:
        return []
    out = [x for x in articles if x.beat == article.beat and x.slug != article.slug]
    out.sort(key=lambda a: a.published_at, reverse=True)
    return out[:limit]


def _tkey(a: Article) -> str:
    """Key used to group translations: translation_key first, else the slug with its
    language suffix removed."""
    tk = (getattr(a, "translation_key", "") or "").strip()
    if tk:
        return tk
    return _LANG_SUFFIX.sub("", a.slug) or a.slug


def _index_switch(editions, current_lang):
    return [{"label": e["label"], "url": e["base"] + "/",
             "current": e["lang"] == current_lang} for e in editions]


def _article_switch(article, editions, current_lang, pairs):
    key = _tkey(article)
    out = []
    for e in editions:
        slug = (pairs.get(key) or {}).get(e["lang"])
        url = (e["base"] + f"/article/{slug}.html") if slug else (e["base"] + "/")
        out.append({"label": e["label"], "url": url,
                    "current": e["lang"] == current_lang})
    return out


def render_article_html(article: Article, *, site: Optional[dict] = None,
                        theme: str = "default", related: Optional[List[Article]] = None,
                        base: str = "", lang_switch=None, lang=None) -> str:
    s = {**DEFAULT_SITE, **(site or {})}
    ui = site_ui(lang or s["lang"])
    return _env(theme).get_template("article.html").render(
        a=article, site=s, related=related or [], base=base,
        lang_switch=lang_switch, ui=ui)


def render_index_html(articles: List[Article], *, site: Optional[dict] = None,
                      theme: str = "default", base: str = "", lang_switch=None,
                      lang=None) -> str:
    s = {**DEFAULT_SITE, **(site or {})}
    ui = site_ui(lang or s["lang"])
    beats = sorted({a.beat for a in articles if a.beat})
    return _env(theme).get_template("index.html").render(
        articles=articles, site=s, beats=beats, base=base,
        lang_switch=lang_switch, ui=ui)


def render_site(articles: List[Article], out_dir: str, *, site: Optional[dict] = None,
                theme: str = "default", base: str = "",
                editions=None, current_lang=None, pairs=None) -> dict:
    """Write a single edition to out_dir. If `editions` is given, render the language
    switcher and localize the chrome to `current_lang`."""
    s = {**DEFAULT_SITE, **(site or {})}
    ui_lang = current_lang or s["lang"]
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "article"), exist_ok=True)

    idx_switch = _index_switch(editions, current_lang) if editions else None
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index_html(articles, site=s, theme=theme, base=base,
                                  lang_switch=idx_switch, lang=ui_lang))

    for a in articles:
        art_switch = (_article_switch(a, editions, current_lang, pairs)
                      if editions else None)
        with open(os.path.join(out_dir, "article", f"{a.slug}.html"), "w",
                  encoding="utf-8") as f:
            f.write(render_article_html(a, site=s, theme=theme,
                                        related=_related(a, articles), base=base,
                                        lang_switch=art_switch, lang=ui_lang))

    feed_url = s["base_url"]
    if base and s["base_url"]:
        feed_url = s["base_url"].rstrip("/") + base
    with open(os.path.join(out_dir, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(build_feed(articles, kind="rss", title=s["title"], site_url=feed_url,
                           sources_label=site_ui(ui_lang)["sources_h"]))

    return {"articles": len(articles), "out_dir": os.path.abspath(out_dir)}


_REDIRECT = """<!DOCTYPE html>
<html lang="{plang}"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={primary}">
<title>{title}</title></head>
<body><h1>{title}</h1><p>Choose a language / 言語を選んでください</p><p>{links}</p>
<script>location.replace("{primary}")</script></body></html>"""


def _write_root_redirect(out_dir, primary_path, s, editions):
    links = " ".join(f'<a href="{e["base"]}/">{e["label"]}</a>' for e in editions)
    html = _REDIRECT.format(plang=s.get("primary_lang") or s.get("lang", "en"),
                            primary=primary_path, title=s["title"], links=links)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_site(articles: List[Article], out_dir: str, *, site: Optional[dict] = None,
               theme: str = "default") -> dict:
    """Write one edition per language (domestic / international). A single language
    writes at the root, unchanged."""
    s = {**DEFAULT_SITE, **(site or {})}
    deflang = s.get("lang", "en")
    by = {}
    for a in articles:
        by.setdefault(a.lang or deflang, []).append(a)
    langs = sorted(by)

    if len(langs) <= 1:
        info = render_site(articles, out_dir, site=s, theme=theme)
        info["editions"] = langs
        return info

    labels = {**LANG_LABELS, **(s.get("lang_labels") or {})}
    editions = [{"lang": L, "label": labels.get(L, L.upper()), "base": f"/{L}"}
                for L in langs]
    primary = s.get("primary_lang") or max(langs, key=lambda L: len(by[L]))
    pairs = {}
    for a in articles:
        pairs.setdefault(_tkey(a), {})[a.lang or deflang] = a.slug

    total = 0
    for L in langs:
        render_site(by[L], os.path.join(out_dir, L), site=s, theme=theme,
                    base=f"/{L}", editions=editions, current_lang=L, pairs=pairs)
        total += len(by[L])
    os.makedirs(out_dir, exist_ok=True)
    _write_root_redirect(out_dir, f"/{primary}/", s, editions)
    return {"articles": total, "editions": langs, "primary": primary,
            "out_dir": os.path.abspath(out_dir)}
