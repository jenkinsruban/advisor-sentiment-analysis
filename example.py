"""
Example script demonstrating programmatic usage of the Sentiment Analyzer.
"""

from sentiment_analyzer import SentimentAnalyzer

def main():
    """Example usage of the sentiment analyzer."""
    
    # Initialize the analyzer
    analyzer = SentimentAnalyzer()
    
    # Example advisor communications
    sample_texts = [
        "I'm very satisfied with the investment advice provided. The portfolio performance has exceeded expectations.",
        "I'm concerned about the recent market volatility and would like to discuss risk management strategies.",
        "The quarterly report shows steady growth. Please continue with the current investment approach."
    ]
    
    print("=" * 70)
    print("ADVISOR SENTIMENT ANALYSIS - EXAMPLE USAGE")
    print("=" * 70)
    print()
    
    # Analyze each text
    for i, text in enumerate(sample_texts, 1):
        print(f"\nAnalyzing Text {i}:")
        print(f"'{text[:60]}...'")
        print("-" * 70)
        
        try:
            result = analyzer.analyze(text)
            
            print(f"Sentiment: {result['sentiment'].upper()}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Emotional Tone: {result['emotional_tone']}")
            print(f"Summary: {result['summary']}")
            
            if result.get('key_indicators'):
                print(f"Key Indicators: {', '.join(result['key_indicators'][:3])}")
            
            print()
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print()
    
    # Batch analysis example
    print("=" * 70)
    print("BATCH ANALYSIS EXAMPLE")
    print("=" * 70)
    
    results = analyzer.analyze_batch(sample_texts)
    
    for result in results:
        if 'error' not in result:
            print(f"Text {result.get('index', '?')}: {result['sentiment'].upper()} "
                  f"({result['confidence']:.0%} confidence)")
        else:
            print(f"Text {result.get('index', '?')}: Error - {result.get('error')}")

if __name__ == "__main__":
    main()

