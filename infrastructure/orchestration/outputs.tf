
output "data_pipeline_step_function_arn" {
  value = aws_sfn_state_machine.orchestrator.arn
}