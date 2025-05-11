
resource "aws_iam_role" "eventbridge_iam_role" {
  name = "eventbridge-schedule-iam-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Sid = "EventBridgeAssumptionRole"
            Effect = "Allow"
            Action = "sts:AssumeRole"
            Principal = {
                Service = "events.amazonaws.com"
            }
        }
    ]
  })
}

resource "aws_iam_role_policy" "eventbridge_iam_role_policy" {
  name = aws_iam_role.eventbridge_iam_role.name
  role = aws_iam_role.eventbridge_iam_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Sid = "AllowEventBridgeAccessToStepFunction"
            Effect = "Allow"
            Action = "states:StartExecution"
            Resource = "${var.orchestrator_step_function_arn}"
        }
    ]
  })
}