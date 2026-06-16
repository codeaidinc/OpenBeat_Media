# Deploy with Terraform — Cloudflare Workers static assets (optional / advanced)

One `terraform apply` **provisions the project and uploads the built site** to
Cloudflare Workers static assets. The Cloudflare provider (v5.11+) handles the
asset manifest, hashing and chunked upload — no Wrangler needed.

> **OSS users:** you do **not** need this. The simple path is to build and drag
> `output/` onto Cloudflare (see `../../docs/Cloudflare_setup.md`). This folder
> is for operators who want repeatable Infrastructure-as-Code deploys.

> **Publish gate:** OpenBeat Media has no limited-publish mode — deploying makes
> every article public. Do a human neutrality / source review **before** apply.

## What it creates

- `cloudflare_workers_script.site` — an **assets-only** Worker (no code; Cloudflare serves the files in `output/`).
- `cloudflare_workers_script_subdomain.site` — the free `*.workers.dev` URL.
- `cloudflare_workers_custom_domain.site` — *(optional)* a custom hostname, created only if you set `custom_domain`.

## Prerequisites

1. **Terraform** ≥ 1.6.
2. **Build the site first** (this uploads `output/`, it does not build it):

   ```bash
   cd ../..            # OpenBeat_Media/
   python cli.py build # writes output/
   ```

3. **A Cloudflare API token** (Dashboard > My Profile > API Tokens), with:
   - *Account › Workers Scripts › Edit* (deploy worker + assets + workers.dev)
   - *Zone › DNS › Edit* and *Zone › Workers Routes › Edit* — **only if** you use a custom domain.

## Run it

```bash
cd deploy/terraform

# 1) credentials (token via env, account id via tfvars)
export CLOUDFLARE_API_TOKEN="xxxxx"        # PowerShell: $env:CLOUDFLARE_API_TOKEN="xxxxx"
cp terraform.tfvars.example terraform.tfvars   # then edit account_id

# 2) deploy
terraform init
terraform plan
terraform apply
```

After apply, `terraform output` shows the URL. To publish updates, rebuild
(`python cli.py build`) and run `terraform apply` again — only changed files
are uploaded.

## Custom domain

Uncomment `custom_domain`, `zone_id`, `zone_name` in `terraform.tfvars`. The
domain must be on a zone in the same Cloudflare account; Cloudflare issues the
edge TLS certificate automatically.

## Notes

- State (`terraform.tfstate`) and `terraform.tfvars` are gitignored. For team
  use, configure a remote backend (e.g. r2/s3) — not included here.
- This is an assets-only static deploy. If you later add Worker code (APIs,
  redirects logic), add `content_file` + `main_module` to `cloudflare_workers_script`.
