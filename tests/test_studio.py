"""Studio (local editing UI) E2E. Studio is English by default."""
import os

import pytest

from studio import create_app


@pytest.fixture
def app(tmp_path):
    a = create_app(content_dir=str(tmp_path / "content"),
                   output_dir=str(tmp_path / "output"))
    a.testing = True
    return a


@pytest.fixture
def client(app):
    return app.test_client()


def test_index_empty(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "OpenBeat Media Studio" in r.get_data(as_text=True)


def test_new_form(client):
    assert client.get("/new").status_code == 200


def test_save_requires_title(client):
    r = client.post("/save", data={"title": "", "sources": "https://x"},
                    follow_redirects=True)
    assert "Title is required" in r.get_data(as_text=True)


def test_save_requires_sources(client):
    r = client.post("/save", data={"title": "記事", "sources": ""},
                    follow_redirects=True)
    assert "A source is required" in r.get_data(as_text=True)


def test_save_creates_file(app):
    c = app.test_client()
    c.post("/save", data={"title": "テスト記事", "sources": "https://example.org/a",
                          "body_md": "本文", "beat": "science-tech"})
    files = os.listdir(app.config["CONTENT_DIR"])
    assert any(f.endswith(".md") for f in files)
    body = c.get("/").get_data(as_text=True)
    assert "テスト記事" in body


def test_edit_existing(app):
    c = app.test_client()
    c.post("/save", data={"title": "編集対象", "sources": "https://x", "slug": "e1"})
    r = c.get("/edit/e1")
    assert r.status_code == 200 and "編集対象" in r.get_data(as_text=True)


def test_build_then_preview(app):
    c = app.test_client()
    c.post("/save", data={"title": "公開記事", "sources": "https://example.org/a",
                          "body_md": "本文ここ", "slug": "p1"})
    r = c.post("/build", follow_redirects=True)
    assert "Build complete" in r.get_data(as_text=True)
    assert os.path.isfile(os.path.join(app.config["OUTPUT_DIR"], "article", "p1.html"))
    prev = c.get("/preview/article/p1.html")
    assert prev.status_code == 200 and "本文ここ" in prev.get_data(as_text=True)


def test_delete(app):
    c = app.test_client()
    c.post("/save", data={"title": "消す", "sources": "https://x", "slug": "d1"})
    c.post("/delete/d1")
    assert not os.path.isfile(os.path.join(app.config["CONTENT_DIR"], "d1.md"))
