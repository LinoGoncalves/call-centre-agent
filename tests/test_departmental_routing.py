#!/usr/bin/env python3
"""
Test script for departmental routing and dispute detection
"""

#!/usr/bin/env python3
"""Test departmental routing functionality."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models.enhanced_classifier import GeminiEnhancedClassifier

def test_departmental_routing():
    """Test the new departmental routing functionality."""
    print('=== DEPARTMENTAL ROUTING & DISPUTE DETECTION TEST ===\n')
    
    try:
        classifier = GeminiEnhancedClassifier()
        
        # Test cases designed to test different departments and dispute detection
        test_cases = [
            {
                'ticket': 'I dispute this R500 charge on my bill - I never authorized this premium service',
                'expected_dept': 'CREDIT_MGMT',
                'expected_dispute': True,
                'description': 'Clear billing dispute'
            },
            {
                'ticket': 'Can you please explain why my bill is R200 higher than last month?',
                'expected_dept': 'BILLING', 
                'expected_dispute': False,
                'description': 'General billing inquiry'
            },
            {
                'ticket': 'I want to upgrade my internet package to fibre and get installation scheduled',
                'expected_dept': 'ORDER_MGMT',
                'expected_dispute': False,
                'description': 'Service order request'
            },
            {
                'ticket': 'Your customer service is absolutely terrible and I am thinking of cancelling',
                'expected_dept': 'CRM',
                'expected_dispute': False,
                'description': 'Customer relationship issue'
            },
            {
                'ticket': 'I was double charged for my data bundle last week - please refund one charge',
                'expected_dept': 'CREDIT_MGMT',
                'expected_dispute': True,
                'description': 'Double billing dispute'
            }
        ]
        
        results = []
        
        for i, case in enumerate(test_cases, 1):
            print(f"--- Test {i}: {case['description']} ---")
            print(f"Ticket: {case['ticket']}")
            
            # Classify the ticket
            result = classifier.classify_ticket(case['ticket'])
            
            # Display results
            print(f"Category: {result.predicted_category}")
            print(f"Department: {result.department_allocation}")
            print(f"Assigned Team: {result.assigned_team}")
            print(f"Dispute Detected: {result.dispute_detected} (Confidence: {result.dispute_confidence:.1%})")
            print(f"Routing Confidence: {result.routing_confidence:.1%}")
            print(f"Priority: {result.priority_level}")
            print(f"HITL Required: {result.requires_hitl}")
            print(f"Sentiment: {result.sentiment_label} (Score: {result.sentiment_score:+.2f})")
            print(f"Processing Time: {result.processing_time_ms:.0f}ms")
            
            # Check accuracy
            dept_correct = result.department_allocation == case['expected_dept']
            dispute_correct = result.dispute_detected == case['expected_dispute']
            
            print(f"✅ Department Correct: {dept_correct}")
            print(f"✅ Dispute Detection Correct: {dispute_correct}")
            
            results.append({
                'case': case['description'],
                'dept_correct': dept_correct,
                'dispute_correct': dispute_correct,
                'result': result
            })
            
            print()
        
        # Summary
        dept_accuracy = sum(r['dept_correct'] for r in results) / len(results)
        dispute_accuracy = sum(r['dispute_correct'] for r in results) / len(results)
        
        print("="*60)
        print("SUMMARY:")
        print(f"Department Routing Accuracy: {dept_accuracy:.1%}")
        print(f"Dispute Detection Accuracy: {dispute_accuracy:.1%}")
        print(f"Total Test Cases: {len(results)}")
        print("="*60)
        
        # Show any failures
        failures = [r for r in results if not (r['dept_correct'] and r['dispute_correct'])]
        if failures:
            print("\nFAILED CASES:")
            for failure in failures:
                print(f"- {failure['case']}")
                if not failure['dept_correct']:
                    print(f"  Department: Expected vs Actual - Need to review routing logic")
                if not failure['dispute_correct']:
                    print(f"  Dispute: Expected vs Actual - Need to review dispute detection")
        else:
            print("\n🎉 ALL TESTS PASSED! The departmental routing system is working correctly.")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_departmental_routing()