
resource "aws_cloudwatch_log_group" "glue_log_group" {
  name = "anime-analytics/logs/glue-job"
}