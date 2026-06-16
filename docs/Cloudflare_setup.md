# Publishing to Cloudflare Pages (no git, no GitHub)

English · [日本語](Cloudflare_setup.ja.md)

When you "Build site" in OpenBeat Media Studio, a static site is written to `output/`.
You can publish it by **drag & drop** onto Cloudflare Pages.

## What you need

- A free Cloudflare account (no GitHub account needed)
- A built `output/` folder

## Steps

1. Sign in to [dash.cloudflare.com](https://dash.cloudflare.com).
2. Left menu **Workers & Pages** → **Create application** → **Pages** → **Upload assets** (Direct Upload).
3. Enter a project name (e.g. `my-beat`). The public URL becomes `<project>.pages.dev`.
4. Drag & drop the contents of `output/` → **Deploy site**.
5. In a few seconds it is live at `https://<project>.pages.dev`.

> Limit: one drag & drop is up to **1,000 files, 25 MiB per file** (plenty for article media).

## After adding or updating articles

1. Edit in Studio → "Build site".
2. Open the same Pages project and re-upload `output/` as a **new deployment**.

## Custom domain (optional)

- `*.pages.dev` is free. For a custom domain (e.g. `news.example.com`), buy the domain and add it from
  Pages **Custom domains** (the Cloudflare-side setup is free; only the domain registration costs money).

## Note

- If you choose Direct Upload, you cannot later switch the same project to Git integration (you would have
  to create a separate project). This tool runs without Git, so that is not a problem.
