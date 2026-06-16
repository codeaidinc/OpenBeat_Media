"""OpenBeat Media (OSS) CLI.

  python cli.py studio              start the local editing UI (http://127.0.0.1:5070)
  python cli.py build [--out DIR]   build content/ into a static site (applies site.json branding);
                                    if articles have multiple `lang` values, one edition per language
  python cli.py new "Title" --source URL [--beat ...]   create an article skeleton
  python cli.py seed                load demo articles

Messages are English by default; set OPENBEAT_LANG=ja for the Studio UI in Japanese.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openbeat_media_core import Article, dump_article, load_dir, build_site, slugify  # noqa: E402

CONTENT = os.environ.get("OPENBEAT_CONTENT_DIR", "content")


def load_site() -> dict:
    """Read site.json if present (else defaults): brand name, logo, accent color, etc.
    Same contract as studio.site_config (override the path with OPENBEAT_SITE_JSON)."""
    path = os.environ.get("OPENBEAT_SITE_JSON", "site.json")
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


DEMO = [
    Article(slug="semiconductor-export",
            title="Export controls on semiconductor materials ripple through SMEs",
            beat="science-tech", author="Editorial",
            summary="Tighter controls push smaller suppliers toward alternative sourcing.",
            tags=["semiconductors", "export controls"],
            sources=["https://www.meti.go.jp/example"],
            published_at="2026-06-14T09:00:00Z", lang="en",
            body_md="## Overview\nFacing tighter controls, smaller domestic suppliers are turning to alternative sourcing and reviewing inventory.\n\n- Finding alternative suppliers\n- Revisiting inventory policy\n\nSee the [METI announcement](https://www.meti.go.jp/example) for details."),
    Article(slug="climate-power",
            title="Climate adaptation frontline: local power supply-and-demand measures",
            beat="climate-energy", author="Editorial",
            summary="Peak-demand measures and renewable balancing under extreme heat.",
            tags=["climate", "power"],
            sources=["https://www.enecho.meti.go.jp/example"],
            published_at="2026-06-12T09:00:00Z", lang="en",
            body_md="## The shape of the squeeze\nUnder extreme heat and peak demand, local governments are racing to secure renewable balancing capacity."),
]


def _save(a: Article):
    os.makedirs(CONTENT, exist_ok=True)
    with open(os.path.join(CONTENT, f"{a.slug}.md"), "w", encoding="utf-8") as f:
        f.write(dump_article(a))


def main(argv=None):
    p = argparse.ArgumentParser(prog="openbeat-media")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("studio")
    b = sub.add_parser("build")
    b.add_argument("--out", default=os.environ.get("OPENBEAT_OUTPUT_DIR", "output"))
    n = sub.add_parser("new")
    n.add_argument("title")
    n.add_argument("--source", action="append", default=[])
    n.add_argument("--beat", default="")
    sub.add_parser("seed")
    args = p.parse_args(argv)

    if args.cmd == "studio":
        from studio import create_app
        create_app().run(host="127.0.0.1", port=int(os.environ.get("PORT", "5070")))
        return 0
    if args.cmd == "build":
        info = build_site(load_dir(CONTENT), args.out, site=load_site())
        eds = info.get("editions") or []
        if len(eds) > 1:
            print(f"built {info['articles']} articles in {len(eds)} editions "
                  f"({'/'.join(eds)}, primary={info.get('primary')}) -> {info['out_dir']}")
        else:
            print(f"built {info['articles']} articles -> {info['out_dir']}")
        print("-> Upload this folder to Cloudflare Pages.")
        return 0
    if args.cmd == "new":
        if not args.source:
            print("error: at least one --source is required", file=sys.stderr)
            return 2
        a = Article(slug=slugify(args.title), title=args.title, beat=args.beat,
                    sources=args.source)
        _save(a)
        print(f"created content/{a.slug}.md")
        return 0
    if args.cmd == "seed":
        for a in DEMO:
            _save(a)
        print(f"seeded {len(DEMO)} demo articles into {CONTENT}/")
        return 0
    return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
