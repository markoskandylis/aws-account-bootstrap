provider "aws" {
  region = "eu-west-2"
  assume_role {
    role_arn     = "arn:aws:iam::${local.account_config.account_id}:role/cross-account-role"
    session_name = "cross-account"
  }
}

terraform {
  backend "s3" {}
}

