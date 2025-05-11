
variable "data_pipeline_step_func_role_arn" {
  description = "this is the arn of the entore workflow/orchestration of step functions"
  type = string
  sensitive = true
}
variable "extract_sfn" {
  description = "this is the arn of the extract sfn"
  type = string
  sensitive = true
}
variable "glue_job_name" {
  description = "this is the name of the glue etl job set in the infra configurations in file: ./glue/glue_job.tf"
  type = string
  sensitive = false
}
variable "sns_arn" {
  description = "this is the arn of the SNS Topic: ./monitoring/sns.tf"
  type = string
  sensitive = true
}
