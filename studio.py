"""OpenBeat Media Studio — the local static-publishing app (OSS, free).

For non-developers (journalists): edit articles in the browser, "Build" the static
site, then upload the output folder to Cloudflare Pages (no git, no GitHub).
Packageable into a single Win/Mac executable with PyInstaller.

Articles are content/<slug>.md (Markdown + front-matter), via openbeat_media_core.
The UI is English by default; set OPENBEAT_LANG=ja for Japanese.
"""
from __future__ import annotations

import os
import sys

from flask import (Flask, redirect, render_template, request, send_from_directory,
                   url_for, flash)

# Make the package importable when run from this directory.
for _p in (os.path.dirname(os.path.abspath(__file__)),):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from openbeat_media_core import (Article, dump_article, load_article, load_dir,
                                 build_site, slugify)
from openbeat_media_core.i18n import studio_ui

CONTENT_DIR = os.environ.get("OPENBEAT_CONTENT_DIR", "content")
OUTPUT_DIR = os.environ.get("OPENBEAT_OUTPUT_DIR", "output")


def site_config() -> dict:
    """Read site.json if present (else defaults). Set brand assets and accent color here."""
    import json
    path = os.environ.get("OPENBEAT_SITE_JSON", "site.json")
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def create_app(content_dir: str = None, output_dir: str = None) -> Flask:
    app = Flask(__name__)
    # Studio is a local-only tool (binds to 127.0.0.1). secret_key is used only to sign
    # flash messages; Studio handles no authentication or personal data. When running on a
    # public network, set OPENBEAT_STUDIO_SECRET. If unset, fall back to a localhost-only
    # development default (not for public use).
    secret = os.environ.get("OPENBEAT_STUDIO_SECRET")
    if not secret:
        if os.environ.get("OPENBEAT_STUDIO_PRODUCTION"):
            raise RuntimeError(
                "OPENBEAT_STUDIO_SECRET is not set. When OPENBEAT_STUDIO_PRODUCTION is "
                "enabled you must provide secret_key via an environment variable."
            )
        secret = "openbeat-studio-dev"  # localhost-only development fallback
    app.secret_key = secret
    app.config["CONTENT_DIR"] = content_dir or CONTENT_DIR
    app.config["OUTPUT_DIR"] = output_dir or OUTPUT_DIR

    def cdir():
        d = app.config["CONTENT_DIR"]
        os.makedirs(d, exist_ok=True)
        return d

    @app.route("/")
    def index():
        arts = load_dir(cdir())
        return render_template("studio_index.html", articles=arts, t=studio_ui(),
                               output_dir=os.path.abspath(app.config["OUTPUT_DIR"]))

    @app.route("/new")
    def new():
        return render_template("studio_edit.html", a=None, t=studio_ui())

    @app.route("/edit/<slug>")
    def edit(slug):
        path = os.path.join(cdir(), f"{slug}.md")
        if not os.path.isfile(path):
            return redirect(url_for("index"))
        return render_template("studio_edit.html", a=load_article(path), t=studio_ui())

    @app.route("/save", methods=["POST"])
    def save():
        t = studio_ui()
        f = request.form
        title = f.get("title", "").strip()
        if not title:
            flash(t["msg_title_required"])
            return redirect(url_for("new"))
        sources = [s.strip() for s in f.get("sources", "").replace("\n", ",").split(",") if s.strip()]
        if not sources:
            flash(t["msg_sources_required"])
            return redirect(url_for("new"))
        slug = f.get("slug", "").strip() or slugify(title)
        a = Article(
            slug=slug, title=title, body_md=f.get("body_md", ""),
            summary=f.get("summary", "").strip(), beat=f.get("beat", "").strip(),
            tags=[t2.strip() for t2 in f.get("tags", "").split(",") if t2.strip()],
            author=f.get("author", "").strip(), sources=sources,
            published_at=f.get("published_at", "").strip(), lang=f.get("lang", "en"),
        )
        with open(os.path.join(cdir(), f"{a.slug}.md"), "w", encoding="utf-8") as fp:
            fp.write(dump_article(a))
        flash(t["msg_saved"].format(slug=a.slug))
        return redirect(url_for("index"))

    @app.route("/delete/<slug>", methods=["POST"])
    def delete(slug):
        t = studio_ui()
        path = os.path.join(cdir(), f"{slug}.md")
        if os.path.isfile(path):
            os.remove(path)
            flash(t["msg_deleted"].format(slug=slug))
        return redirect(url_for("index"))

    @app.route("/build", methods=["POST"])
    def build():
        t = studio_ui()
        arts = load_dir(cdir())
        info = build_site(arts, app.config["OUTPUT_DIR"], site=site_config())
        eds = info.get("editions") or []
        extra = t["editions_note"].format(n=len(eds), langs="/".join(eds)) if len(eds) > 1 else ""
        flash(t["msg_built"].format(n=info["articles"], extra=extra, dir=info["out_dir"]))
        return redirect(url_for("index"))

    @app.route("/preview/")
    @app.route("/preview/<path:sub>")
    def preview(sub="index.html"):
        out = app.config["OUTPUT_DIR"]
        if not os.path.isfile(os.path.join(out, sub)):
            sub = "index.html"
        if not os.path.isfile(os.path.join(out, sub)):
            flash(studio_ui()["msg_build_first"])
            return redirect(url_for("index"))
        return send_from_directory(out, sub)

    return app


if __name__ == "__main__":  # pragma: no cover
    create_app().run(host="127.0.0.1", port=int(os.environ.get("PORT", "5070")),
                     debug=bool(os.environ.get("OPENBEAT_STUDIO_DEBUG")))
