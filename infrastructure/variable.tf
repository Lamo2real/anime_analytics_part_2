
variable "pipeline_region" {
  description = "this is the region where the infrastrcuture of ETL anime analytics will be hosted"
  type = string
  sensitive = true
}

variable "data_lake" {
  description = "this is the data lake hosted on amazon s3 (name)"
  type = string
  sensitive = true
}

variable "secrets_manager" {
  default = "secret-variables/anime-analytics"
  description = "this is the name of etl secrets manager repo"
  type = string
  sensitive = true
}
variable "secrets_manager_db_credentials" {
  description = "this is the name of etl secrets manager database CREDENTIAL"
  type = map(string) #this is the structure it expects: {"key1":"value1", "key2": "value2", "key3": "value3", "key4": "value4"}
  sensitive = true
}
variable "account_id" {
  description = "this is the aws account id like: 32795627856"
  type = string
  sensitive = true
}
variable "secrets_manager_path" {
  description = "this is the aws secrets manager secrets path where the secrets are stored"
  type = string
  sensitive = true
}
variable "sfn_data_extract_name" {
  description = "this is the name of the lamba function from part 1 repository"
  type = string
  sensitive = true
}