


terraform {
    backend "s3" {}
    required_version = ">=1.9.5"
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = ">= 5.85.0"
      }
    }
}

provider "aws" {
  region = var.pipeline_region
}

 # these are the values sent out to 
 # child directories (make sure to use the variables
 # here in a variables.tf file in the child directories elsewhere)
module "parent_vars_to_glue" {
  source                   = "./glue"
  
  glue_role_arn            = module.parent_vars_to_security.glue_iam_role_arn
  data_lake_bucket_name    = var.data_lake
}

module "parent_vars_to_monitoring" {
  source                   = "./monitoring"
}

module "parent_vars_to_security" {
  source                   = "./security"
  
  glue_cw_name             = module.parent_vars_to_monitoring.cw_log_group_name
  region                   = var.pipeline_region 
  path_to_secrets          = var.secrets_manager_path
  aws_account_id           = var.account_id
  data_lake_bucket_name    = var.data_lake
  secrets_manager_name     = var.secrets_manager
  security_snowflake_creds = var.secrets_manager_db_credentials
}

