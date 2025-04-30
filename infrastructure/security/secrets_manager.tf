
resource "aws_secretsmanager_secret" "db_secrets" {
  name = var.secrets_manager_name
}

resource "aws_secretsmanager_secret_version" "db_secrets_values" {
  secret_id = aws_secretsmanager_secret.db_secrets.id
  secret_string = jsonencode(var.security_snowflake_creds)
}