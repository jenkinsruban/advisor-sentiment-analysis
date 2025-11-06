"""
Command-line interface for Advisor Sentiment Analysis tool.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional
from sentiment_analyzer import SentimentAnalyzer
from bedrock_client import BedrockClient


def format_output(result: dict, output_format: str = "pretty") -> str:
    """
    Format the analysis result for display.
    
    Args:
        result: Analysis result dictionary
        output_format: 'pretty', 'json', or 'simple'
        
    Returns:
        Formatted string
    """
    if output_format == "json":
        return json.dumps(result, indent=2)
    elif output_format == "simple":
        return f"Sentiment: {result.get('sentiment', 'unknown')} " \
               f"(Confidence: {result.get('confidence', 0):.2f})"
    else:  # pretty
        lines = [
            "=" * 60,
            "SENTIMENT ANALYSIS RESULTS",
            "=" * 60,
            f"\nSentiment: {result.get('sentiment', 'unknown').upper()}",
            f"Confidence: {result.get('confidence', 0):.2%}",
            f"\nEmotional Tone: {result.get('emotional_tone', 'N/A')}",
            f"\nSummary: {result.get('summary', 'N/A')}",
        ]
        
        key_indicators = result.get('key_indicators', [])
        if key_indicators:
            lines.append(f"\nKey Indicators:")
            for indicator in key_indicators:
                lines.append(f"  • {indicator}")
        
        recommendations = result.get('recommendations')
        if recommendations:
            lines.append(f"\nRecommendations: {recommendations}")
        
        lines.append(f"\nModel Used: {result.get('model_used', 'N/A')}")
        lines.append(f"Text Length: {result.get('text_length', 0)} characters")
        lines.append("=" * 60)
        
        return "\n".join(lines)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Advisor Sentiment Analysis using Amazon Bedrock",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze text directly
  python cli.py "Your advisor text here"
  
  # Analyze from file
  python cli.py --file input.txt
  
  # Output as JSON
  python cli.py "Your text" --format json
  
  # Analyze multiple texts from file (one per line)
  python cli.py --file input.txt --batch
  
  # Use custom model
  python cli.py "Your text" --model anthropic.claude-3-haiku-20240307-v1:0
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "text",
        nargs="?",
        help="Text to analyze (if not using --file)"
    )
    input_group.add_argument(
        "--file",
        "-f",
        type=Path,
        help="Path to file containing text to analyze"
    )
    
    # Optional arguments
    parser.add_argument(
        "--format",
        "-F",
        choices=["pretty", "json", "simple"],
        default="pretty",
        help="Output format (default: pretty)"
    )
    
    parser.add_argument(
        "--model",
        "-m",
        help="Bedrock model ID (overrides BEDROCK_MODEL_ID env var)"
    )
    
    parser.add_argument(
        "--region",
        "-r",
        help="AWS region (overrides AWS_REGION env var)"
    )
    
    parser.add_argument(
        "--batch",
        "-b",
        action="store_true",
        help="Process multiple texts from file (one per line)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file path (default: stdout)"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        bedrock_client = None
        if args.region:
            bedrock_client = BedrockClient(region_name=args.region)
        
        analyzer = SentimentAnalyzer(
            model_id=args.model,
            bedrock_client=bedrock_client
        )
        
        # Get input text(s)
        if args.file:
            if not args.file.exists():
                print(f"Error: File '{args.file}' not found.", file=sys.stderr)
                sys.exit(1)
            
            with open(args.file, 'r', encoding='utf-8') as f:
                if args.batch:
                    texts = [line.strip() for line in f if line.strip()]
                else:
                    texts = [f.read().strip()]
        else:
            texts = [args.text]
        
        if not texts or not any(texts):
            print("Error: No text to analyze.", file=sys.stderr)
            sys.exit(1)
        
        # Analyze
        if args.batch or len(texts) > 1:
            results = analyzer.analyze_batch(texts)
            output_lines = []
            
            for result in results:
                if "error" in result:
                    output_lines.append(
                        f"\n[Error in text {result.get('index', '?')}]: "
                        f"{result.get('error', 'Unknown error')}\n"
                    )
                else:
                    output_lines.append(format_output(result, args.format))
                    output_lines.append("")  # Blank line between results
            
            output = "\n".join(output_lines)
        else:
            result = analyzer.analyze(texts[0])
            output = format_output(result, args.format)
        
        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Results saved to {args.output}")
        else:
            print(output)
    
    except KeyboardInterrupt:
        print("\n\nAnalysis cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

