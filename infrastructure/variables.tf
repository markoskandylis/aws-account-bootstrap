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

variable "accounts_config" {
  description = "Map of objects for per environment configuration"
  type = map(object({
    account_id = string
  }))
}

variable "vpc_name_prefix" {
  description = "The name of the vpc"
  type        = string
  default     = ""
}

variable "vpc_name" {
  description = "The name of the vpc"
  type        = string
  default     = ""
}

variable "vpc_cidr" {
  description = "the cidr of the vpc"
  type        = string
  default     = ""
}

variable "secondary_vpc_cidr" {
  description = "the secondary non routable cidr of the vpc"
  default     = "100.64.0.0/16"
}

variable "region" {
  description = "deployment region"
  default     = "eu-west-2"
}

variable "deployment_role" {
  description = "role that is used to deploy the vpc"
  default     = ""
}

# Transit gateway configurations
variable "transit_gateway_id" {
  description = "The id of TGW if it doenst exist its an empty string"
  default     = ""
}

variable "tgw_vpc_cidr" {
  description = "the other vpc cidrs that we want tht trafic from private subnets to go"
  type        = list(string)
  default     = []
}
