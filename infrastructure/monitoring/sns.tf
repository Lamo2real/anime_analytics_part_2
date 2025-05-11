
# 1: setup step functions orchestration 
# 2: setup eventbridge
# 3: setup lambda 
# 4: setup sns 
# 5: setup IAM role and policies for all
resource "aws_sns_topic" "sns_for_pipeline" {
    name = "anime-analytics-sns-topic"
}
resource "aws_sns_topic_subscription" "sns_for_pipeline_sub" {
  topic_arn = aws_sns_topic.sns_for_pipeline.arn
  protocol = "email"
  endpoint = "lamochi02@gmail.com"
}