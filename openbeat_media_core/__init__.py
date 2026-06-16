"""OpenBeat Media Core — shared library (Apache-2.0).

Provides:
  - content.py : the Article model and Markdown front-matter read/write
  - feed.py    : RSS 2.0 / Atom 1.0 feed generation (deterministic)
  - render.py  : article -> static HTML (theme applied; single / multi-language editions)
  - themes/    : Jinja themes
"""
from .content import Article, load_article, dump_article, load_dir, slugify
from .feed import build_rss, build_atom, build_feed
from .render import render_site, render_article_html, build_site

__version__ = "0.1.0"

__all__ = [
    "Article", "load_article", "dump_article", "load_dir", "slugify",
    "build_rss", "build_atom", "build_feed",
    "render_site", "render_article_html", "build_site",
]
