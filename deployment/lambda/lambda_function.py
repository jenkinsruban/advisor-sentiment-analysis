"""
Lambda handler for Advisor Sentiment Analysis API.
Handles API Gateway requests and returns sentiment analysis results.
"""

import json
import os
from typing import Dict, Any, Optional
from sentiment_analyzer import SentimentAnalyzer
from bedrock_client import BedrockClient


def create_response(
    status_code: int,
    body: Dict[str, Any],
    cors_origins: str = "*"
) -> Dict[str, Any]:
    """
    Create API Gateway HTTP API response with CORS headers.
    
    Args:
        status_code: HTTP status code
        body: Response body as dictionary
        cors_origins: CORS allowed origins
        
    Returns:
        API Gateway response dictionary
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": cors_origins,
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for API Gateway HTTP API requests.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    # Get CORS origins from environment variable or use default
    cors_origins = os.getenv("CORS_ORIGINS", "*")
    
    # Handle OPTIONS request for CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return create_response(200, {"message": "OK"}, cors_origins)
    
    try:
        # Parse request body
        body = {}
        if event.get("body"):
            try:
                body = json.loads(event["body"])
            except json.JSONDecodeError:
                return create_response(
                    400,
                    {"error": "Invalid JSON in request body"},
                    cors_origins
                )
        
        # Get route path - API Gateway HTTP API v2 structure
        # Try multiple possible locations for path and method
        request_context = event.get("requestContext", {})
        http_context = request_context.get("http", {})
        
        # Get path from various possible locations
        path = (
            http_context.get("path") or 
            event.get("rawPath") or 
            event.get("path") or 
            ""
        )
        
        # Get method
        method = (
            http_context.get("method") or 
            event.get("requestContext", {}).get("httpMethod") or 
            event.get("httpMethod") or 
            ""
        ).upper()
        
        # Get route key as fallback (format: "POST /analyze")
        route_key = event.get("routeKey", "")
        
        # Debug logging (for troubleshooting - remove in production if needed)
        print(f"Debug - Path: {path}, Method: {method}, RouteKey: {route_key}")
        print(f"Debug - Event keys: {list(event.keys())}")
        
        # Route to appropriate handler
        # Check by route key first (most reliable for HTTP API v2)
        if route_key == "POST /analyze" or (path == "/analyze" and method == "POST"):
            return handle_analyze(body, cors_origins)
        elif route_key == "POST /analyze-batch" or (path == "/analyze-batch" and method == "POST"):
            return handle_analyze_batch(body, cors_origins)
        else:
            return create_response(
                404,
                {
                    "error": "Endpoint not found. Use /analyze or /analyze-batch",
                    "debug": {
                        "path": path,
                        "method": method,
                        "routeKey": route_key,
                        "eventKeys": list(event.keys())
                    }
                },
                cors_origins
            )
            
    except Exception as e:
        # Log error (CloudWatch will capture this)
        print(f"Error in lambda_handler: {str(e)}")
        return create_response(
            500,
            {"error": "Internal server error", "message": str(e)},
            cors_origins
        )


def handle_analyze(body: Dict[str, Any], cors_origins: str) -> Dict[str, Any]:
    """
    Handle single text analysis request.
    
    Args:
        body: Request body
        cors_origins: CORS origins
        
    Returns:
        API Gateway response
    """
    try:
        # Validate input
        if "text" not in body:
            return create_response(
                400,
                {"error": "Missing 'text' field in request body"},
                cors_origins
            )
        
        text = body["text"]
        if not text or not isinstance(text, str) or not text.strip():
            return create_response(
                400,
                {"error": "Text cannot be empty"},
                cors_origins
            )
        
        # Get model ID from body or environment
        model_id = body.get("model_id") or os.getenv("BEDROCK_MODEL_ID", "amazon.titan-text-express-v1")
        
        # Debug: Log IAM role information for troubleshooting
        try:
            import boto3
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            print(f"Debug - Lambda execution role: {identity.get('Arn', 'Unknown')}")
        except Exception as e:
            print(f"Debug - Could not get caller identity: {e}")
        
        # Initialize analyzer
        analyzer = SentimentAnalyzer(model_id=model_id)
        
        # Analyze text
        result = analyzer.analyze(text)
        
        # Return success response
        return create_response(
            200,
            {
                "success": True,
                "data": result
            },
            cors_origins
        )
        
    except ValueError as e:
        return create_response(
            400,
            {"error": "Validation error", "message": str(e)},
            cors_origins
        )
    except Exception as e:
        print(f"Error in analyze: {str(e)}")
        return create_response(
            500,
            {"error": "Analysis failed", "message": str(e)},
            cors_origins
        )


def handle_analyze_batch(body: Dict[str, Any], cors_origins: str) -> Dict[str, Any]:
    """
    Handle batch text analysis request.
    
    Args:
        body: Request body
        cors_origins: CORS origins
        
    Returns:
        API Gateway response
    """
    try:
        # Validate input
        if "texts" not in body:
            return create_response(
                400,
                {"error": "Missing 'texts' field in request body. Expected array of strings."},
                cors_origins
            )
        
        texts = body["texts"]
        if not isinstance(texts, list) or len(texts) == 0:
            return create_response(
                400,
                {"error": "Texts must be a non-empty array"},
                cors_origins
            )
        
        # Validate each text
        for i, text in enumerate(texts):
            if not isinstance(text, str) or not text.strip():
                return create_response(
                    400,
                    {"error": f"Text at index {i} is empty or invalid"},
                    cors_origins
                )
        
        # Get model ID from body or environment
        model_id = body.get("model_id") or os.getenv("BEDROCK_MODEL_ID", "amazon.titan-text-express-v1")
        
        # Initialize analyzer
        analyzer = SentimentAnalyzer(model_id=model_id)
        
        # Analyze texts
        results = analyzer.analyze_batch(texts)
        
        # Return success response
        return create_response(
            200,
            {
                "success": True,
                "data": {
                    "results": results,
                    "count": len(results)
                }
            },
            cors_origins
        )
        
    except ValueError as e:
        return create_response(
            400,
            {"error": "Validation error", "message": str(e)},
            cors_origins
        )
    except Exception as e:
        print(f"Error in analyze_batch: {str(e)}")
        return create_response(
            500,
            {"error": "Batch analysis failed", "message": str(e)},
            cors_origins
        )

