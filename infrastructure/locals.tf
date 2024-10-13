locals {
  account_config     = var.accounts_config[terraform.workspace]
  vpc_name           = var.vpc_name_prefix != "" ? "${var.vpc_name_prefix}-${var.vpc_name}" : var.vpc_name
  vpc_cidr           = var.vpc_cidr
  transit_gateway_id = try(var.transit_gateway_id, "")
  secondary_vpc_cidr = var.secondary_vpc_cidr
  azs                = slice(data.aws_availability_zones.available.names, 0, 3)
  environment        = terraform.workspace

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

  tags = {
    Environment = local.environment
  }
}



