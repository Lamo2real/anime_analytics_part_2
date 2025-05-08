

variable "region" {
  description = "this is the region of where the etl pipeline on glue is hosted"
  type = string
  sensitive = true
}
variable "secrets_manager_name" {
  default = "secret-variables/anime-analytics"
  description = "this is inherited from parent directory for the name of the secrets manager repository"
  type = string
  sensitive = false
}
variable "security_snowflake_creds" {
  description = "this is the name of etl secrets manager database CREDENTIAL"
  type = map(string)
  sensitive = true
}
variable "data_lake_bucket_name" {
  description = "this is inherited from parent directory adn it is the bucket name"
  type = string
  sensitive = true
}
variable "aws_accound_id" {
  type = string
  sensitive = true
}
variable "path_to_secrets" {
  type = string
  sensitive = true
}