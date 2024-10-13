# Shared Services BackEnd Bucket
resource "aws_s3_bucket" "example" {
  count  = terraform.workspace == "SharedServices-Account" ? 1 : 0
  bucket = "hub-and-spoke-state"

  tags = {
    Name        = "Hub-And-Spoke-State"
    Environment = "Prod"
  }
}
