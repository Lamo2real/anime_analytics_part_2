

resource "aws_sfn_state_machine" "orchestrator" {
  name = "data-pipeline-orchestration"
  role_arn = var.data_pipeline_step_func_role_arn

  definition = jsonencode(
    {
        Comment = "this is the orchestration tool to run the workflow of the entire data pipeline"
        StartAt = "runWorkflow"
        States = {

            runWorkflow = {
                Type = "Task"
                Resource = "arn:aws:states:::states:startExecution.sync"
                Parameters = {
                    StateMachineArn = "${var.extract_sfn}"
                }
                ResultPath = "$.extractWorkflowResult"        
                Retry = [
                  {
                    ErrorEquals = ["Lambda.AWSLambdaException"]
                    IntervalSeconds = 2
                    MaxAttempts = 3
                    BackoffRate = 2.0
                  }
                ]
                Catch = [
                    {
                        ErrorEquals = ["States.ALL"]
                        Next = "publishFailMessage"
                    }
                ]
                Next = "runGlueJob"
            }

            runGlueJob = {
                Type = "Task"
                Resource = "arn:aws:states:::glue:startJobRun.sync"
                Parameters = {
                    JobName = "${var.glue_job_name}"
                }
                Catch = [
                    {
                        ErrorEquals = ["States.ALL"]
                        Next = "publishFailMessage"
                    }
                ]
                Next = "publishSuccessMessage"
            }

            publishFailMessage = {
                Type = "Task"
                Resource = "arn:aws:states:::sns:publish"
                Parameters = {
                    TopicArn = "${var.sns_arn}"
                    Message = "AWS Anime Analytics data pipeline failed during execution"
                    Subject = "Step Function FAILED"
                }
                End = true
            }

            publishSuccessMessage = {
                Type = "Task"
                Resource = "arn:aws:states:::sns:publish"
                Parameters = {
                    TopicArn = "${var.sns_arn}"
                    Message = "AWS Anime Analytics data pipeline was Successful"
                    Subject = "Step Function PASSED"
                }
                End = true
            }
        }
    }
  )
}