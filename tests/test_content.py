"""Tests for the shared core content.py."""
import os

from openbeat_media_core import Article, dump_article, load_article, load_dir, slugify
from openbeat_media_core.content import md_to_html, _fallback_md


def test_slugify_ascii_and_japanese():
    assert slugify("Hello World") == "hello-world"
    assert slugify("半導体の記事")  # non-empty for Japanese too


def test_article_defaults():
    a = Article(slug="", title="タイトル")
    assert a.slug  # generated from the title
    assert a.published_at  # auto-filled


def test_dump_load_roundtrip(tmp_path):
    a = Article(slug="x1", title="記事タイトル", body_md="## 見出し\n本文",
                beat="science-tech", tags=["半導体", "規制"],
                author="編集部", sources=["https://example.org/a"],
                published_at="2026-06-14T09:00:00Z")
    path = tmp_path / "x1.md"
    path.write_text(dump_article(a), encoding="utf-8")
    b = load_article(str(path))
    assert b.title == "記事タイトル"
    assert b.tags == ["半導体", "規制"]
    assert b.sources == ["https://example.org/a"]
    assert b.beat == "science-tech"
    assert "見出し" in b.body_md


def test_load_dir_sorted(tmp_path):
    for slug, dt in [("a", "2026-06-10T00:00:00Z"), ("b", "2026-06-14T00:00:00Z")]:
        Article(slug=slug, title=slug, sources=["https://x"], published_at=dt)
        p = tmp_path / f"{slug}.md"
        p.write_text(dump_article(Article(slug=slug, title=slug.upper(),
                     sources=["https://x"], published_at=dt)), encoding="utf-8")
    arts = load_dir(str(tmp_path))
    assert [a.slug for a in arts] == ["b", "a"]  # newest first


def test_fallback_markdown():
    html = _fallback_md("## 見出し\n\n本文の段落\n\n- 項目1\n- 項目2")
    assert "<h2>見出し</h2>" in html
    assert "<p>本文の段落</p>" in html
    assert "<ul><li>項目1</li><li>項目2</li></ul>" in html


def test_fallback_inline_link():
    html = _fallback_md("[リンク](https://example.org) と **強調**")
    assert '<a href="https://example.org"' in html
    assert "<strong>強調</strong>" in html


def test_body_html_property():
    a = Article(slug="x", title="t", body_md="## H\n段落", sources=["https://x"])
    assert "<h2>" in a.body_html


def test_teaser_from_summary():
    a = Article(slug="x", title="t", summary="要約だけ", body_md="本文",
                sources=["https://x"])
    assert a.teaser == "要約だけ"
