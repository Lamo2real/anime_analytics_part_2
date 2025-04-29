

data "aws_s3_bucket" "anime_data_lake" {
  bucket = var.data_lake_bucket_name
}