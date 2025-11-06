"""
Sentiment analysis module for advisor text using Amazon Bedrock.
"""

import json
import os
from typing import Dict, Any, Optional
from bedrock_client import BedrockClient


class SentimentAnalyzer:
    """Analyzes sentiment of advisor communications using AI."""
    
    def __init__(
        self,
        model_id: Optional[str] = None,
        bedrock_client: Optional[BedrockClient] = None
    ):
        """
        Initialize the sentiment analyzer.
        
        Args:
            model_id: Bedrock model ID (defaults to BEDROCK_MODEL_ID env var)
            bedrock_client: Optional pre-configured BedrockClient instance
        """
        # Default to Titan (no use case form required)
        # To use Claude: "anthropic.claude-3-sonnet-20240229-v1:0" (requires Anthropic use case form)
        self.model_id = model_id or os.getenv(
            "BEDROCK_MODEL_ID",
            "amazon.titan-text-express-v1"
        )
        self.client = bedrock_client or BedrockClient()
        
    def _create_sentiment_prompt(self, text: str) -> str:
        """
        Create a prompt for sentiment analysis.
        
        Args:
            text: The advisor text to analyze
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Analyze the sentiment of the following advisor communication and provide a detailed analysis.

Text to analyze:
"{text}"

Please provide a JSON response with the following structure:
{{
    "sentiment": "positive" | "negative" | "neutral" | "mixed",
    "confidence": 0.0-1.0,
    "emotional_tone": "brief description",
    "key_indicators": ["list", "of", "key", "phrases", "or", "words"],
    "summary": "brief summary of the sentiment",
    "recommendations": "actionable recommendations based on the sentiment"
}}

Analyze the text carefully and provide accurate sentiment assessment."""
        
        return prompt
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of advisor text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary containing sentiment analysis results
            
        Raises:
            ValueError: If text is empty
            Exception: If analysis fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            prompt = self._create_sentiment_prompt(text)
            response = self.client.invoke_model(
                model_id=self.model_id,
                prompt=prompt,
                max_tokens=2000,
                temperature=0.3  # Lower temperature for more consistent analysis
            )
            
            # Try to parse JSON from response
            result = self._parse_response(response)
            
            # Add metadata
            result["model_used"] = self.model_id
            result["text_length"] = len(text)
            
            return result
            
        except Exception as e:
            raise Exception(f"Sentiment analysis failed: {str(e)}")
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the model response into structured data.
        
        Args:
            response: Raw model response
            
        Returns:
            Parsed sentiment analysis dictionary
        """
        # Try to extract JSON from response
        response_clean = response.strip()
        
        # Look for JSON block in markdown code blocks
        if "```json" in response_clean:
            start = response_clean.find("```json") + 7
            end = response_clean.find("```", start)
            if end != -1:
                response_clean = response_clean[start:end].strip()
        elif "```" in response_clean:
            start = response_clean.find("```") + 3
            end = response_clean.find("```", start)
            if end != -1:
                response_clean = response_clean[start:end].strip()
        
        # Try to find JSON object in response
        start_brace = response_clean.find("{")
        end_brace = response_clean.rfind("}")
        
        if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
            json_str = response_clean[start_brace:end_brace + 1]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # If JSON parsing fails, create structured response from text
        return {
            "sentiment": "unknown",
            "confidence": 0.5,
            "emotional_tone": "Unable to parse",
            "key_indicators": [],
            "summary": response,
            "recommendations": "Please review the raw response"
        }
    
    def analyze_batch(self, texts: list[str]) -> list[Dict[str, Any]]:
        """
        Analyze sentiment for multiple texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of sentiment analysis results
        """
        results = []
        for i, text in enumerate(texts, 1):
            try:
                result = self.analyze(text)
                result["index"] = i
                results.append(result)
            except Exception as e:
                results.append({
                    "index": i,
                    "error": str(e),
                    "sentiment": "error"
                })
        
        return results

