# Deploy the built static site (output/) to Cloudflare Workers static assets.
#
# This is an ASSETS-ONLY Worker: there is no Worker code — Cloudflare serves the
# files directly. The provider scans `assets.directory`, hashes each file,
# builds the manifest, and uploads only changed files on each `terraform apply`.
# So a single `terraform apply` provisions AND deploys the whole site.

resource "cloudflare_workers_script" "site" {
  account_id  = var.account_id
  script_name = var.worker_name

  assets = {
    directory = var.assets_dir

    config = {
      html_handling      = "auto-trailing-slash"
      not_found_handling = var.not_found_handling
    }
  }
}

# Expose on the free workers.dev subdomain (https://<name>.<subdomain>.workers.dev).
resource "cloudflare_workers_script_subdomain" "site" {
  account_id       = var.account_id
  script_name      = cloudflare_workers_script.site.script_name
  enabled          = var.enable_workers_dev
  previews_enabled = false
}

# Optional: route a custom hostname to the Worker. Created only when
# custom_domain is non-empty. Cloudflare provisions the edge TLS certificate.
resource "cloudflare_workers_custom_domain" "site" {
  count = var.custom_domain == "" ? 0 : 1

  account_id = var.account_id
  hostname   = var.custom_domain
  service    = cloudflare_workers_script.site.script_name
  zone_id    = var.zone_id
  zone_name  = var.zone_name
}
