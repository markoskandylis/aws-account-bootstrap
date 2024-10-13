data "aws_organizations_organization" "org" {}

data "aws_availability_zones" "available" {
  state = "available"
}
