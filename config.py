"""
Configuration management for Advisor Sentiment Analysis.
"""

import os
from typing import Optional

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional


class Config:
    """Application configuration."""
    
    # AWS Configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # Bedrock Model Configuration
    # Default to Titan (no use case form required)
    # To use Claude: "anthropic.claude-3-sonnet-20240229-v1:0" (requires Anthropic use case form)
    BEDROCK_MODEL_ID: str = os.getenv(
        "BEDROCK_MODEL_ID",
        "amazon.titan-text-express-v1"
    )
    
    # Default Analysis Parameters
    DEFAULT_MAX_TOKENS: int = 2000
    DEFAULT_TEMPERATURE: float = 0.3
    
    @classmethod
    def validate(cls) -> list[str]:
        """
        Validate configuration and return list of missing required settings.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not cls.AWS_ACCESS_KEY_ID and not os.getenv("AWS_PROFILE"):
            # Check if using IAM role (no explicit credentials)
            # This is valid in AWS environments
            if not os.path.exists(os.path.expanduser("~/.aws/credentials")):
                errors.append(
                    "AWS credentials not found. Set AWS_ACCESS_KEY_ID and "
                    "AWS_SECRET_ACCESS_KEY environment variables, configure "
                    "AWS CLI, or use IAM role."
                )
        
        return errors

