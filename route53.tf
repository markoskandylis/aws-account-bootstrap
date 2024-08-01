module "tenant_zones" {
  count  = length(local.tenant_zones) > 0 ? 1 : 0
  source = "git@github.com:The-Stinky-Badger/terraform-aws-route53.git//modules/zones?ref=master"

  zones = local.tenant_zones

  tags = {
    ManagedBy = "Terraform"
  }
}

resource "aws_route53_record" "this" {
  provider = aws.dns
  for_each = length(local.tenant_zones) > 0 ? toset(sort(keys(module.tenant_zones[0].route53_zone_zone_id))) : toset([])
  zone_id  = local.tenant_remote_zones[each.key]["zone_id"]
  name     = module.tenant_zones[0].route53_zone_name[each.key]
  type     = "NS"
  ttl      = "30"
  records  = module.tenant_zones[0].route53_zone_name_servers[each.key]
}


