

resource "aws_cloudwatch_event_rule" "monthly_sf_trigger" {
  name = "monthly-trigger-anime-analytics-step-functions"
  description = "remember that this is set to frankfurt timezone"
  schedule_expression = "cron(0 1 1 * ? *)"
}

resource "aws_cloudwatch_event_target" "monthly_sf_trigger_target" {
  rule = aws_cloudwatch_event_rule.monthly_sf_trigger.name
  arn = var.data_pipeline_step_func_role_arn
  role_arn = var.event_iam_role_arn
}