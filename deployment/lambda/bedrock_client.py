"""
Amazon Bedrock client for sentiment analysis.
Handles connection and configuration for AWS Bedrock service.
"""

import boto3
import json
import os
from typing import Optional
from botocore.exceptions import ClientError


class BedrockClient:
    """Client for interacting with Amazon Bedrock."""
    
    def __init__(
        self,
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None
    ):
        """
        Initialize Bedrock client.
        
        Args:
            region_name: AWS region (defaults to AWS_REGION env var or us-east-1)
            aws_access_key_id: AWS access key (defaults to AWS_ACCESS_KEY_ID env var)
            aws_secret_access_key: AWS secret key (defaults to AWS_SECRET_ACCESS_KEY env var)
        """
        # In Lambda, AWS_REGION is automatically set by the runtime
        # Don't try to set it manually - it's a reserved environment variable
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
        
        # Initialize boto3 client
        # In Lambda, boto3 automatically uses the IAM role - don't pass credentials
        self.client = self._create_client()
        
    def _create_client(self):
        """
        Create and return a Bedrock runtime client.
        
        Credential resolution order:
        1. Explicit credentials passed to constructor
        2. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        3. AWS CLI credentials (~/.aws/credentials or AWS config)
        4. IAM role (if running on AWS infrastructure)
        """
        try:
            # In Lambda, use boto3's default session which automatically uses IAM role
            # IMPORTANT: Do NOT pass credentials - let boto3 use the Lambda execution role
            # Even if aws_access_key_id/secret are set, don't use them in Lambda
            
            # Check if we're in Lambda (AWS_LAMBDA_FUNCTION_NAME is set)
            is_lambda = os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None
            
            if is_lambda:
                # In Lambda: Use default credentials (IAM role)
                # Don't pass any credentials at all
                client_kwargs = {
                    "service_name": "bedrock-runtime",
                    "region_name": self.region_name
                }
                # Explicitly do NOT pass credentials - use IAM role
            else:
                # Local/testing: Use credentials if provided
                client_kwargs = {
                    "service_name": "bedrock-runtime",
                    "region_name": self.region_name
                }
                if self.aws_access_key_id and self.aws_secret_access_key:
                    client_kwargs["aws_access_key_id"] = self.aws_access_key_id
                    client_kwargs["aws_secret_access_key"] = self.aws_secret_access_key
            
            # Create client - boto3 automatically uses IAM role in Lambda
            client = boto3.client(**client_kwargs)
            
            # Log for debugging
            print(f"Bedrock client created for region: {self.region_name}")
            print(f"Running in Lambda: {is_lambda}")
            if is_lambda:
                try:
                    # boto3 is already imported at top of file
                    sts = boto3.client('sts')
                    identity = sts.get_caller_identity()
                    print(f"Using IAM role: {identity.get('Arn', 'Unknown')}")
                except Exception as e:
                    print(f"Could not get IAM identity: {e}")
            
            return client
        except Exception as e:
            error_msg = f"Failed to create Bedrock client in region {self.region_name}: {str(e)}"
            print(error_msg)
            raise ConnectionError(error_msg)
    
    def invoke_model(
        self,
        model_id: str,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """
        Invoke a Bedrock model with the given prompt.
        
        Args:
            model_id: The Bedrock model ID (e.g., 'anthropic.claude-3-sonnet-20240229-v1:0')
            prompt: The input prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-1.0)
            
        Returns:
            The model's response text
            
        Raises:
            ClientError: If the API call fails
        """
        try:
            # Determine the model provider and format request accordingly
            if "anthropic.claude" in model_id:
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            elif "amazon.titan" in model_id:
                body = {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": max_tokens,
                        "temperature": temperature
                    }
                }
            elif "ai21.j2" in model_id:
                body = {
                    "prompt": prompt,
                    "maxTokens": max_tokens,
                    "temperature": temperature
                }
            else:
                # Default to Claude format
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(body).encode('utf-8'),
                contentType="application/json",
                accept="application/json"
            )
            
            # Parse response based on model type
            response_body = json.loads(response['body'].read())
            
            if "anthropic.claude" in model_id:
                return response_body.get("content", [{}])[0].get("text", "")
            elif "amazon.titan" in model_id:
                return response_body.get("results", [{}])[0].get("outputText", "")
            elif "ai21.j2" in model_id:
                return response_body.get("completions", [{}])[0].get("data", {}).get("text", "")
            else:
                # Default parsing
                if "content" in response_body:
                    return response_body["content"][0]["text"]
                return str(response_body)
                
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            raise ClientError(
                {"Error": {"Code": error_code, "Message": error_message}},
                "invoke_model"
            )
        except Exception as e:
            raise Exception(f"Error invoking model: {str(e)}")

