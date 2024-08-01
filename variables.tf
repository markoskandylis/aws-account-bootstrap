# Remote Account DNS Configuration
variable "tenant_zones" {
  description = "List of tenant zones with DNS name and zone ID"
  type = list(object({
    dns_name = string
    zone_id  = string
    comment  = string
  }))
  default = []
}

variable "env_config" {
  description = "Map of objects for per environment configuration"
  type = map(object({
    account_id = string
  }))
}
