locals {
  account_config = var.env_config[terraform.workspace]
  # default_config = var.default_config

  tenant_zones = merge(
    { for zone in var.tenant_zones : zone.dns_name => {
      zone    = zone.dns_name
      comment = zone.comment
      }
    }
  )

  tenant_remote_zones = merge(
    { for zone in var.tenant_zones : zone.dns_name => {
      zone_id = zone.zone_id
      }
    }
  )
}



