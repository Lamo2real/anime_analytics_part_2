
data "aws_sfn_state_machine" "sfn_extract_workflow" {
  name = var.sfn_part_1
}


resource "aws_iam_role" "step_func_role" {
  name = "step-functions-orchestration-iam-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Sid = "StepFunctionsFullDataPipelineIAMRole"
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
                Service = "states.amazonaws.com"
            }
        }
    ]
  })
}

resource "aws_iam_role_policy" "step_func_role_policy" {
  name = aws_iam_role.step_func_role.name
  role = aws_iam_role.step_func_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Sid = "AllowStepFunctionsAccessToPartOneStepFunc"
            Effect = "Allow"
            Action = [
              "states:StartExecution",
              "states:DescribeExecution"
            ]
            Resource = "${data.aws_sfn_state_machine.sfn_extract_workflow.arn}"
        },
        {
            Sid = "AllowAccessToGlue"
            Effect = "Allow"
            Action = [
                "glue:StartJobRun",
                "glue:GetJobRun",
                "glue:GetJob",
            ]
            Resource = "${var.glue_job_arn}"
        },
        {
            Sid = "AllowStepFunctionsAccessToSNS"
            Effect = "Allow"
            Action = "sns:Publish"
            Resource = "${var.sns_topic_arn}"
        },
        {
          Sid = "AllowAccessToManagedEvents"
          Effect = "Allow"
          Action = [
            "events:PutRule",
            "events:PutTargets",
            "events:DescribeRule",
            "events:DeleteRule",
            "events:RemoveTargets"
          ]
          Resource = "arn:aws:events:${var.region}:${var.aws_account_id}:rule/StepFunctionsGetEventsForStepFunctionsExecutionRule*"
        }
    ]
  })
}

