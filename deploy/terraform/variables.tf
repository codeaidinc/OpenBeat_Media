variable "account_id" {
  type        = string
  description = "Cloudflare account ID (Dashboard > Workers & Pages > Account ID)."
}

variable "worker_name" {
  type        = string
  description = "Worker (project) name. Becomes <worker_name>.<your-subdomain>.workers.dev."
  default     = "middle-east-watch"

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{0,62}$", var.worker_name))
    error_message = "worker_name must be lowercase letters, digits and hyphens (max 63)."
  }
}

variable "assets_dir" {
  type        = string
  description = "Path to the built static site (output of `python cli.py build`)."
  default     = "../../output"
}

variable "enable_workers_dev" {
  type        = bool
  description = "Expose the site on the free <name>.<subdomain>.workers.dev URL."
  default     = true
}

# --- Optional custom domain (leave blank to skip) ---------------------------
variable "custom_domain" {
  type        = string
  description = "Custom hostname to route to the Worker (e.g. watch.example.com). Empty = skip."
  default     = ""
}

variable "zone_id" {
  type        = string
  description = "Zone ID that contains custom_domain (required only if custom_domain is set)."
  default     = ""
}

variable "zone_name" {
  type        = string
  description = "Zone name for custom_domain (e.g. example.com). Required only if custom_domain is set."
  default     = ""
}

# --- Static-asset serving behaviour -----------------------------------------
variable "not_found_handling" {
  type        = string
  description = "How to respond when no asset matches: none | 404-page | single-page-application."
  default     = "404-page"

  validation {
    condition     = contains(["none", "404-page", "single-page-application"], var.not_found_handling)
    error_message = "not_found_handling must be one of: none, 404-page, single-page-application."
  }
}
