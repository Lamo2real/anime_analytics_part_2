

resource "aws_iam_role" "glue_iam_role" {
    name = "glue-iam-role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Sid = "GlueIAMRoleSTS"
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "glue.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_iam_role_policy" "glue_iam_role_policy" {
    name = "${aws_iam_role.glue_iam_role.name}-policy"
    role = aws_iam_role.glue_iam_role.id
    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Sid = "GlueIAMRolePolicy"
                Effect = "Allow"
                Action = [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ]
                Resource = [
                    "arn:aws:s3:::${var.data_lake_bucket_name}/*",
                    "arn:aws:s3:::${var.data_lake_bucket_name}"
                ]
            },
            {
              Sid    = "GlueLogsAnimeAnalytics"
              Effect = "Allow"
              Action = [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
              ]
              Resource = [
                "arn:aws:logs:*:*:*",
                "arn:aws:logs:${var.region}:${var.aws_account_id}:log-group:${var.glue_cw_name}:*",
                "arn:aws:logs:${var.region}:${var.aws_account_id}:log-group:${var.glue_cw_name}:log-stream:*"
                ]
            },
            {
                Sid = "GetSecretsManagerAccess"
                Effect = "Allow"
                Action = "secretsmanager:GetSecretValue"
                Resource = "arn:aws:secretsmanager:${var.region}:${var.aws_account_id}:secret:secret-variables/${var.path_to_secrets}"
            }
        ]
    })

}