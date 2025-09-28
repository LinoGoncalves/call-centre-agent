#!/usr/bin/env python3
"""Test script for final HTML cleaning validation."""

from enhanced_classifier import GeminiEnhancedClassifier
import sys

def test_html_cleaning():
    """Test the nuclear HTML cleaning system."""
    
    # Create classifier
    classifier = GeminiEnhancedClassifier()
    
    # Test the problematic ticket
    ticket_text = '''Customer called to complain about slow internet connection. He is struggling to stream video content and it is severely impacting his productivity. He is considering switching to a competitor if this is not resolved quickly.'''
    
    print('🧪 TESTING FINAL NUCLEAR HTML CLEANING')
    print('='*50)
    
    # Classify the ticket
    result = classifier.classify_ticket(ticket_text)
    
    print(f'Predicted Category: {result.predicted_category}')
    print(f'Sentiment Label: {result.sentiment_label}')
    print(f'Priority Level: {result.priority_level}')
    print()
    print('🔍 CHECKING FOR HTML IN SENTIMENT REASONING:')
    print('='*50)
    print(f'First 300 characters: {repr(result.sentiment_reasoning[:300])}')
    print()
    
    # Check for HTML tags
    has_p_tag = '<p>' in result.sentiment_reasoning
    has_strong_tag = '<strong>' in result.sentiment_reasoning
    has_closing_p = '</p>' in result.sentiment_reasoning
    has_closing_strong = '</strong>' in result.sentiment_reasoning
    has_any_html = '<' in result.sentiment_reasoning or '>' in result.sentiment_reasoning
    
    print(f'Contains <p>: {has_p_tag}')
    print(f'Contains <strong>: {has_strong_tag}')
    print(f'Contains </p>: {has_closing_p}')
    print(f'Contains </strong>: {has_closing_strong}')
    print(f'Contains any < or >: {has_any_html}')
    print()
    
    if has_any_html:
        print('🚨 HTML STILL DETECTED!')
        # Show all angle bracket positions
        html_chars = [i for i, c in enumerate(result.sentiment_reasoning) if c in '<>']
        print(f'HTML character positions: {html_chars[:10]}')
        print()
        print('Full sentiment reasoning:')
        print(repr(result.sentiment_reasoning))
        return False
    else:
        print('✅ NO HTML DETECTED - NUCLEAR CLEANING SUCCESSFUL!')
        print()
        print('Clean sentiment reasoning:')
        print(result.sentiment_reasoning)
        return True

if __name__ == "__main__":
    success = test_html_cleaning()
    sys.exit(0 if success else 1)