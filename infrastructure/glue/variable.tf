

variable "data_lake_bucket_name" {
  description = "this is inherited from parent directory adn it is the bucket name"
  type = string
  sensitive = true
}
variable "glue_role_arn" {
  description = "this is the AWS IAM Role ARN for glue job"
  type = string
  sensitive = true
}