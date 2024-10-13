output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = try(module.vpc[0].vpc_cidr_block, null)
}

output "vpc_id" {
  description = "The VPC ID"
  value       = try(module.vpc[0].vpc_id, null)
}
