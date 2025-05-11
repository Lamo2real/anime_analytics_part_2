
output "glue_iam_role_arn" {
  value = aws_iam_role.glue_iam_role.arn
}
output "step_func_role_arn" {
  value = aws_iam_role.step_func_role.arn
}
output "stfu_extract_workflow" {
  value = data.aws_sfn_state_machine.sfn_extract_workflow.arn
}