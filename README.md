# OpenBeat Media (OSS, desktop edition)

English · [日本語](README.ja.md)

**OpenBeat Media** is a free, open-source desktop publishing tool. A journalist edits
articles on their PC, **builds a static site locally**, and **uploads the output folder
to Cloudflare Pages** — and has their own media outlet for free (no git, no GitHub account required).

## What it does

- Edit articles (Studio = a local editing UI, or edit the Markdown files directly)
- Source traceability (source URL required), beats/tags, author byline
- Build a static site (index, article pages, RSS feed)
- Theming (drop in a logo / hero image, accent color and font via `site.json`)
- Publish by manual upload to Cloudflare Pages (free, serverless)

> It is a static site: all articles are public (no login, no personal data, no trackers by default).

## Use it

```bash
pip install -r requirements.txt
python cli.py seed        # load demo articles
python cli.py studio      # edit at http://127.0.0.1:5070
python cli.py build       # write the static site to output/
# drag & drop output/ onto Cloudflare Pages (see docs/Cloudflare_setup.md)
```

> Publishing by **file upload** (drag & drop) is the default. For advanced users who want to
> codify repeated deploys, an optional Terraform setup that provisions and serves in one shot
> is bundled (`deploy/terraform/`).

## Multilingual editions

When articles carry a `lang` field, `build` produces one edition per language
(e.g. `output/ja/` and `output/en/`) with a language switcher, and a root page that
redirects to the primary language (`primary_lang` in `site.json`). A single language
builds at the root, unchanged.

## Layout

```
openbeat_media_core/      core library (Apache-2.0)
  content.py   Article model + Markdown front-matter read/write
  feed.py      RSS / Atom generation (deterministic)
  render.py    article -> static HTML (theme applied; single / multi-language editions)
  themes/default/  Jinja theme (with slots for logo / hero / accent / font)
studio.py                 local editing UI (Flask; distributable for Win/Mac via PyInstaller)
cli.py                    new / build / studio / seed
content/                  articles (<slug>.md)
docs/Cloudflare_setup.md  publishing guide (create account -> drag & drop -> custom domain)
```

## Documentation language

Documentation is **English-first**; Japanese versions are provided alongside as `*.ja.md`
(e.g. [`README.ja.md`](README.ja.md), [`docs/Cloudflare_setup.ja.md`](docs/Cloudflare_setup.ja.md)).

## License

Apache-2.0 (`LICENSE`).
