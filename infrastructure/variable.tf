
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
  description = "this is the name of etl secrets manager repo"
  type = string
  sensitive = true
}
variable "secrets_manager_db_credentials" {
  description = "this is the name of etl secrets manager database CREDENTIAL"
  type = map(string) #
  sensitive = true
}