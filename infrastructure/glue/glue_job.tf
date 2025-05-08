

resource "aws_glue_job" "et_job" {
    name = "glue-etl-anime-analytics-ingestion"
    role_arn ="${var.glue_role_arn}"
    max_capacity = 0.0625
    glue_version = "5.0"

    command {
      name = "pythonshell"
      script_location = "s3://${var.data_lake_bucket_name}/etl/etl_script.py"
      python_version = "3"
    }
    
    default_arguments = {
      "--additional-python-modules" = "snowflake-connector-python==3.14.1,pandas==2.2.3,boto3==1.38.2",
      "--extra-py-files" = "s3://${var.data_lake_bucket_name}/etl/etl_package.zip"
    }
}