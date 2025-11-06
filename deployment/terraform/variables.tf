variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "advisor-sentiment-analysis"
}

variable "bedrock_model_id" {
  description = "Bedrock model ID to use for sentiment analysis"
  type        = string
  default     = "amazon.titan-text-express-v1"
}

variable "cors_origins" {
  description = "CORS allowed origins (use * for development, specific URL for production)"
  type        = string
  default     = "*"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "lambda_memory_size" {
  description = "Lambda function memory size in MB"
  type        = number
  default     = 512
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 30
}

variable "lambda_runtime" {
  description = "Lambda runtime version"
  type        = string
  default     = "python3.11"
}

