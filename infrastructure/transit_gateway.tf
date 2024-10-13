resource "aws_ec2_transit_gateway" "network" {
  count                          = terraform.workspace == "Network-Account" ? 1 : 0
  auto_accept_shared_attachments = "enable"

  description = "network-account-tgw"
}


resource "aws_ram_resource_share" "tgw_share" {
  count                     = terraform.workspace == "Network-Account" ? 1 : 0
  name                      = "transit-gateway-share"
  allow_external_principals = false

  tags = {
    Environment = "production"
  }
}

resource "aws_ram_resource_association" "tgw_association" {
  count              = terraform.workspace == "Network-Account" ? 1 : 0
  resource_arn       = aws_ec2_transit_gateway.network[0].arn
  resource_share_arn = aws_ram_resource_share.tgw_share[0].arn
}

resource "aws_ram_principal_association" "org_association" {
  count              = terraform.workspace == "Network-Account" ? 1 : 0
  principal          = data.aws_organizations_organization.org.arn
  resource_share_arn = aws_ram_resource_share.tgw_share[0].arn
}

