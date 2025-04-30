


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