# Terraform + Cloudflare provider requirements.
# Static-asset upload to Workers is supported from cloudflare provider v5.11.0+.
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.11"
    }
  }
}
