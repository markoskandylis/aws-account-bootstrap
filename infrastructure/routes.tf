# Transit Gateway Route
resource "aws_route" "tgw_route" {
  for_each = length(var.tgw_vpc_cidr) > 0 ? toset(var.tgw_vpc_cidr) : toset([])

  route_table_id         = try(module.vpc[0].private_route_table_ids[0], "")
  destination_cidr_block = each.value
  transit_gateway_id     = local.transit_gateway_id

  depends_on = [module.vpc]
}

resource "aws_route" "intra_subnets_default_gateway" {
  count                  = local.vpc_name != "" ? 1 : 0
  route_table_id         = try(module.vpc[0].intra_route_table_ids[0], "")
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = try(aws_nat_gateway.private_nat[0].id, "")
  depends_on             = [aws_nat_gateway.private_nat]
}
