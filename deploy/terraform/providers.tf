# The Cloudflare provider reads the API token from the CLOUDFLARE_API_TOKEN
# environment variable. Do NOT hard-code the token here.
#
#   PowerShell:  $env:CLOUDFLARE_API_TOKEN = "xxxxx"
#   bash:        export CLOUDFLARE_API_TOKEN="xxxxx"
#
# Required token permissions:
#   - Account > Workers Scripts : Edit   (deploy the worker + assets, workers.dev)
#   - Zone   > DNS              : Edit   (only if you set custom_domain)
#   - Zone   > Workers Routes   : Edit   (only if you set custom_domain)
provider "cloudflare" {}
