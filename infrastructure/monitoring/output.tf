

output "cw_log_group_name" {
  value = aws_cloudwatch_log_group.glue_log_group.name
}
output "sns_email_topic_arn" {
  value = aws_sns_topic.sns_for_pipeline.arn
}