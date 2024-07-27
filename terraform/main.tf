# Make sure to create state bucket beforehand
terraform {
  required_version = ">= 1.0"
  backend "s3" {
    bucket  = "tf-state-mlops-zoomcamp-cyberbullying"
    key     = "mlops-zoomcamp-cyberbullying-stg.tfstate"
    region  = "eu-north-1"
    encrypt = true
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current_identity" {}

locals {
  account_id = data.aws_caller_identity.current_identity.account_id
}

# tweet_events
module "source_kinesis_stream" {
  source           = "./modules/kinesis"
  retention_period = 24
  shard_count      = 1
  stream_name      = var.source_stream_name
  tags             = var.project_id
}

# tweet_classification
module "output_kinesis_stream" {
  source           = "./modules/kinesis"
  retention_period = 24
  shard_count      = 1
  stream_name      = var.output_stream_name
  tags             = var.project_id
}

# model bucket
module "s3_bucket" {
  source      = "./modules/s3"
  bucket_name = var.model_bucket
}

# image registry
module "ecr_image" {
  source                     = "./modules/ecr"
  ecr_repo_name              = var.ecr_repo_name
  account_id                 = local.account_id
  lambda_function_local_path = var.lambda_function_local_path
  docker_image_local_path    = var.docker_image_local_path
}

module "lambda_function" {
  source               = "./modules/lambda"
  image_uri            = module.ecr_image.image_uri
  lambda_function_name = var.lambda_function_name
  model_bucket         = module.s3_bucket.name
  output_stream_name   = var.output_stream_name
  output_stream_arn    = module.output_kinesis_stream.stream_arn
  source_stream_name   = var.source_stream_name
  source_stream_arn    = module.source_kinesis_stream.stream_arn
}

# For CI/CD
output "lambda_function" {
  value = var.lambda_function_name
}

output "model_bucket" {
  value = module.s3_bucket.name
}

output "predictions_stream_name" {
  value = var.output_stream_name
}

output "ecr_repo" {
  value = var.ecr_repo_name
}
