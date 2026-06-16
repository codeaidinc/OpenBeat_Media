"""Tests for the shared core render.py / feed.py."""
import os

from openbeat_media_core import Article, build_feed, render_site
from openbeat_media_core.render import render_article_html, render_index_html


def _arts():
    return [
        Article(slug="a1", title="半導体の記事", body_md="本文A", beat="science-tech",
                sources=["https://example.org/a"], published_at="2026-06-14T09:00:00Z"),
        Article(slug="a2", title="気候の記事", body_md="本文B", beat="climate-energy",
                sources=["https://example.org/b"], published_at="2026-06-12T09:00:00Z"),
    ]


def test_render_article_includes_sources():
    html = render_article_html(_arts()[0])
    assert "半導体の記事" in html
    assert "example.org/a" in html  # sources are always shown


def test_render_index_lists_and_beats():
    html = render_index_html(_arts())
    assert "半導体の記事" in html and "気候の記事" in html


def test_render_site_writes_files(tmp_path):
    out = str(tmp_path / "out")
    info = render_site(_arts(), out)
    assert info["articles"] == 2
    assert os.path.isfile(os.path.join(out, "index.html"))
    assert os.path.isfile(os.path.join(out, "article", "a1.html"))
    assert os.path.isfile(os.path.join(out, "feed.xml"))
    with open(os.path.join(out, "article", "a1.html"), encoding="utf-8") as f:
        assert "本文A" in f.read()


def test_render_site_applies_site_config(tmp_path):
    out = str(tmp_path / "out")
    render_site(_arts(), out, site={"title": "私のメディア", "accent": "#c0392b",
                                    "logo": "https://cdn/logo.png"})
    with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
        body = f.read()
    assert "私のメディア" in body
    assert "#c0392b" in body          # accent color
    assert "https://cdn/logo.png" in body  # logo slot


def test_feed_rss_and_atom():
    rss = build_feed(_arts(), kind="rss", title="My Feed", site_url="https://m.example")
    assert "<rss" in rss and "半導体の記事" in rss and "example.org/a" in rss
    atom = build_feed(_arts(), kind="atom", title="My Feed", site_url="https://m.example")
    assert "<feed" in atom and "気候の記事" in atom
