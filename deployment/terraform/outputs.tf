output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_api.api.api_endpoint
}

output "api_invoke_url" {
  description = "API Gateway invoke URL (same as api_endpoint)"
  value       = aws_apigatewayv2_api.api.api_endpoint
}

output "analyze_endpoint" {
  description = "Full URL for /analyze endpoint"
  value       = "${aws_apigatewayv2_api.api.api_endpoint}/analyze"
}

output "analyze_batch_endpoint" {
  description = "Full URL for /analyze-batch endpoint"
  value       = "${aws_apigatewayv2_api.api.api_endpoint}/analyze-batch"
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.sentiment_analyzer.function_name
}

output "lambda_function_arn" {
  description = "Lambda function ARN"
  value       = aws_lambda_function.sentiment_analyzer.arn
}

output "lambda_role_arn" {
  description = "Lambda IAM role ARN"
  value       = aws_iam_role.lambda_role.arn
}

