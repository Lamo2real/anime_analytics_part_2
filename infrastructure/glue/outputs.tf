

output "glue_arn" {
  value = aws_glue_job.et_job.arn
}
output "glue_name" {
  value = aws_glue_job.et_job.name
}