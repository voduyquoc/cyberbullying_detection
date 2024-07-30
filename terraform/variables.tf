variable "aws_region" {
  description = "AWS region to create resources"
  default     = "your-default-aws-region"
}

variable "project_id" {
  description = "project_id"
  default     = "mlops-zoomcamp-cyberbullying"
}

variable "source_stream_name" {
  description = "name of stream that send tweet text"
}

variable "output_stream_name" {
  description = "name of stream that send classification result"
}

variable "model_bucket" {
  description = "name of s3_bucket which contains model"
}

variable "lambda_function_local_path" {
  description = "local path of lambda function / python file"
}

variable "docker_image_local_path" {
  description = "local path of Dockerfile"
}

variable "ecr_repo_name" {
  description = "name of ecr repo"
}

variable "lambda_function_name" {
  description = "name of lambda function"
}