output "worker_name" {
  description = "The deployed Worker (project) name."
  value       = cloudflare_workers_script.site.script_name
}

output "workers_dev_note" {
  description = "Where to find the live site on workers.dev."
  value = var.enable_workers_dev ? "https://${var.worker_name}.<your-account-subdomain>.workers.dev (find <your-account-subdomain> in Dashboard > Workers & Pages > your worker > Settings > Domains & Routes)" : "workers.dev disabled (enable_workers_dev = false)"
}

output "custom_domain_url" {
  description = "Custom-domain URL, if configured."
  value       = var.custom_domain == "" ? "(no custom domain set)" : "https://${var.custom_domain}"
}
