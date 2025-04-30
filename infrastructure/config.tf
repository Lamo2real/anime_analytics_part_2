


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
  source = "./glue"

  data_lake_bucket_name = var.data_lake
}

module "parent_vars_to_security" {
  source = "./security"
  
  secrets_manager_name = var.secrets_manager
  security_snowflake_creds = var.secrets_manager_db_credentials
}

