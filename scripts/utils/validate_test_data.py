"""
🧪 Test Validation Script - Rules Engine + RAG Pipeline
=======================================================

This script validates that the mock data correctly triggers:
1. Rules Engine: High-confidence pattern matches (≥85%)
2. RAG Pipeline: Complex scenarios requiring LLM reasoning

Usage:
    python validate_test_data.py

Expected Results:
- Rules Engine: 19 tickets should match specific rules
- RAG System: 10 tickets should require LLM analysis
- Performance: Sub-millisecond rules evaluation
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import time

# Add src to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.models.rules_engine import TelcoRulesEngine
    from src.models.enhanced_classifier import GeminiEnhancedClassifier
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure src/models/rules_engine.py and enhanced_classifier.py are available")
    sys.exit(1)

class TestValidator:
    """Validate mock data against Rules Engine and RAG pipeline."""
    
    def __init__(self):
        print("🔧 Initializing Test Validator...")
        
        # Initialize Rules Engine
        self.rules_engine = TelcoRulesEngine()
        print(f"✅ Rules Engine loaded with {len(self.rules_engine.rules)} rules")
        
        # Initialize Enhanced Classifier (for RAG validation)
        try:
            self.classifier = GeminiEnhancedClassifier()
            print("✅ Enhanced Classifier (RAG) initialized")
        except Exception as e:
            print(f"⚠️ Enhanced Classifier not available: {e}")
            print("RAG tests will be skipped")
            self.classifier = None
        
        # Load test data
        self.load_test_data()
    
    def load_test_data(self):
        """Load generated test data files."""
        try:
            with open("rules_engine_test_data.json", "r") as f:
                self.rules_test_data = json.load(f)
            print(f"✅ Loaded {len(self.rules_test_data['test_cases'])} Rules Engine test cases")
            
            with open("rag_system_test_data.json", "r") as f:
                self.rag_test_data = json.load(f)
            print(f"✅ Loaded {len(self.rag_test_data['test_cases'])} RAG system test cases")
            
        except FileNotFoundError as e:
            print(f"❌ Test data files not found: {e}")
            print("Please run test_data_generator.py first")
            sys.exit(1)
    
    def validate_rules_engine(self) -> Dict[str, Any]:
        """Validate that Rules Engine correctly identifies high-confidence patterns."""
        
        print("\n🔧 VALIDATING RULES ENGINE")
        print("=" * 50)
        
        results = {
            "total_tests": len(self.rules_test_data['test_cases']),
            "successful_matches": 0,
            "failed_matches": 0,
            "incorrect_rules": 0,
            "confidence_errors": 0,
            "department_errors": 0,
            "processing_times": [],
            "detailed_results": []
        }
        
        for i, test_case in enumerate(self.rules_test_data['test_cases'], 1):
            ticket_text = test_case['text']
            expected_rule = test_case['expected_rule']
            expected_dept = test_case['expected_department']
            expected_conf = test_case['expected_confidence']
            
            print(f"\n📧 Test {i:2d}: {test_case['ticket_id']}")
            print(f"   Text: {ticket_text[:60]}...")
            print(f"   Expected: {expected_rule} → {expected_dept} ({expected_conf:.1%})")
            
            # Time the evaluation
            start_time = time.perf_counter()
            match = self.rules_engine.evaluate_ticket(ticket_text)
            processing_time = (time.perf_counter() - start_time) * 1000  # Convert to ms
            
            results["processing_times"].append(processing_time)
            
            test_result = {
                "ticket_id": test_case['ticket_id'],
                "ticket_text": ticket_text,
                "expected_rule": expected_rule,
                "expected_department": expected_dept,
                "expected_confidence": expected_conf,
                "processing_time_ms": processing_time
            }
            
            if match:
                print(f"   ✅ MATCH: {match.rule_id} → {match.department} ({match.confidence:.1%}) [{processing_time:.2f}ms]")
                
                # Validate rule ID
                if match.rule_id == expected_rule:
                    results["successful_matches"] += 1
                    test_result["result"] = "SUCCESS"
                else:
                    results["incorrect_rules"] += 1
                    test_result["result"] = "WRONG_RULE"
                    test_result["actual_rule"] = match.rule_id
                    print(f"   ⚠️ Wrong rule: got {match.rule_id}, expected {expected_rule}")
                
                # Validate department
                if match.department != expected_dept:
                    results["department_errors"] += 1
                    test_result["department_error"] = f"got {match.department}, expected {expected_dept}"
                
                # Validate confidence (within 5% tolerance)
                if abs(match.confidence - expected_conf) > 0.05:
                    results["confidence_errors"] += 1
                    test_result["confidence_error"] = f"got {match.confidence:.1%}, expected {expected_conf:.1%}"
                
                test_result["actual_rule"] = match.rule_id
                test_result["actual_department"] = match.department
                test_result["actual_confidence"] = match.confidence
                
            else:
                print(f"   ❌ NO MATCH: Rules engine did not trigger (should have matched {expected_rule})")
                results["failed_matches"] += 1
                test_result["result"] = "NO_MATCH"
                test_result["actual_rule"] = None
            
            results["detailed_results"].append(test_result)
        
        # Calculate statistics
        avg_processing_time = sum(results["processing_times"]) / len(results["processing_times"])
        max_processing_time = max(results["processing_times"])
        
        print(f"\n📊 RULES ENGINE VALIDATION SUMMARY")
        print("=" * 50)
        print(f"✅ Successful Matches: {results['successful_matches']}/{results['total_tests']} ({results['successful_matches']/results['total_tests']:.1%})")
        print(f"❌ Failed Matches: {results['failed_matches']}")
        print(f"⚠️ Incorrect Rules: {results['incorrect_rules']}")
        print(f"⚠️ Department Errors: {results['department_errors']}")
        print(f"⚠️ Confidence Errors: {results['confidence_errors']}")
        print(f"⚡ Avg Processing Time: {avg_processing_time:.2f}ms")
        print(f"⚡ Max Processing Time: {max_processing_time:.2f}ms")
        
        return results
    
    def validate_rag_system(self) -> Dict[str, Any]:
        """Validate that complex cases are handled by RAG/LLM pipeline."""
        
        if not self.classifier:
            print("\n⚠️ SKIPPING RAG VALIDATION - Classifier not available")
            return {"skipped": True, "reason": "classifier_not_available"}
        
        print(f"\n🤖 VALIDATING RAG SYSTEM")
        print("=" * 50)
        
        results = {
            "total_tests": len(self.rag_test_data['test_cases']),
            "successful_classifications": 0,
            "failed_classifications": 0,
            "processing_times": [],
            "confidence_scores": [],
            "detailed_results": []
        }
        
        for i, test_case in enumerate(self.rag_test_data['test_cases'], 1):
            ticket_text = test_case['text']
            expected_category = test_case['expected_category']
            complexity = test_case['complexity']
            
            print(f"\n📧 Test {i:2d}: {test_case['ticket_id']}")
            print(f"   Text: {ticket_text[:60]}...")
            print(f"   Expected: {expected_category} (Complexity: {complexity})")
            
            # Check if this would trigger rules engine first
            start_time = time.perf_counter()
            rules_match = self.rules_engine.evaluate_ticket(ticket_text)
            
            if rules_match:
                print(f"   ⚠️ Unexpected rules match: {rules_match.rule_id} (should go to RAG)")
                continue
            
            # Test RAG/LLM classification
            try:
                result = self.classifier.classify_ticket(ticket_text)
                processing_time = result.processing_time_ms
                
                results["processing_times"].append(processing_time)
                results["confidence_scores"].append(result.confidence)
                
                print(f"   ✅ RAG Result: {result.predicted_category} ({result.confidence:.1%}) [{processing_time:.0f}ms]")
                print(f"   💭 Reasoning: {result.reasoning[:100]}...")
                
                test_result = {
                    "ticket_id": test_case['ticket_id'],
                    "expected_category": expected_category,
                    "actual_category": result.predicted_category,
                    "confidence": result.confidence,
                    "processing_time_ms": processing_time,
                    "reasoning": result.reasoning,
                    "result": "SUCCESS"
                }
                
                results["successful_classifications"] += 1
                
            except Exception as e:
                print(f"   ❌ RAG Classification failed: {e}")
                test_result = {
                    "ticket_id": test_case['ticket_id'],
                    "expected_category": expected_category,
                    "error": str(e),
                    "result": "FAILED"
                }
                results["failed_classifications"] += 1
            
            results["detailed_results"].append(test_result)
        
        # Calculate statistics
        if results["processing_times"]:
            avg_processing_time = sum(results["processing_times"]) / len(results["processing_times"])
            avg_confidence = sum(results["confidence_scores"]) / len(results["confidence_scores"])
        else:
            avg_processing_time = 0
            avg_confidence = 0
        
        print(f"\n📊 RAG SYSTEM VALIDATION SUMMARY")
        print("=" * 50)
        print(f"✅ Successful Classifications: {results['successful_classifications']}/{results['total_tests']}")
        print(f"❌ Failed Classifications: {results['failed_classifications']}")
        print(f"⚡ Avg Processing Time: {avg_processing_time:.0f}ms")
        print(f"📊 Avg Confidence: {avg_confidence:.1%}")
        
        return results
    
    def run_comprehensive_validation(self):
        """Run complete validation of both Rules Engine and RAG system."""
        
        print("🧪 COMPREHENSIVE TEST VALIDATION")
        print("=" * 60)
        print("Testing mock data against Rules Engine and RAG pipeline...")
        
        # Validate Rules Engine
        rules_results = self.validate_rules_engine()
        
        # Validate RAG System  
        rag_results = self.validate_rag_system()
        
        # Overall summary
        print(f"\n🎯 OVERALL VALIDATION RESULTS")
        print("=" * 60)
        
        print(f"📋 Rules Engine:")
        print(f"   ✅ Success Rate: {rules_results['successful_matches']}/{rules_results['total_tests']} ({rules_results['successful_matches']/rules_results['total_tests']:.1%})")
        print(f"   ⚡ Avg Speed: {sum(rules_results['processing_times'])/len(rules_results['processing_times']):.2f}ms")
        
        if not rag_results.get('skipped', False):
            print(f"📋 RAG System:")
            print(f"   ✅ Success Rate: {rag_results['successful_classifications']}/{rag_results['total_tests']}")
            if rag_results["processing_times"]:
                avg_rag_time = sum(rag_results["processing_times"]) / len(rag_results["processing_times"])
                print(f"   ⚡ Avg Speed: {avg_rag_time:.0f}ms")
        
        # Performance comparison
        if rules_results['processing_times']:
            rules_avg = sum(rules_results['processing_times']) / len(rules_results['processing_times'])
            if not rag_results.get('skipped', False) and rag_results["processing_times"]:
                rag_avg = sum(rag_results["processing_times"]) / len(rag_results["processing_times"])
                speedup = rag_avg / rules_avg
                print(f"\n⚡ Performance:")
                print(f"   Rules Engine: {rules_avg:.2f}ms avg")
                print(f"   RAG System: {rag_avg:.0f}ms avg")
                print(f"   🚀 Rules Engine is {speedup:.0f}x faster")
        
        # Save detailed results
        validation_results = {
            "timestamp": time.time(),
            "rules_engine_results": rules_results,
            "rag_system_results": rag_results
        }
        
        with open("validation_results.json", "w") as f:
            json.dump(validation_results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to validation_results.json")
        
        return validation_results

def main():
    """Main validation execution."""
    validator = TestValidator()
    results = validator.run_comprehensive_validation()
    
    # Quick pass/fail summary
    rules_success_rate = results['rules_engine_results']['successful_matches'] / results['rules_engine_results']['total_tests']
    
    if rules_success_rate >= 0.85:  # 85% success rate threshold
        print(f"\n🎉 VALIDATION PASSED!")
        print(f"Rules Engine achieving {rules_success_rate:.1%} accuracy")
        return True
    else:
        print(f"\n❌ VALIDATION FAILED!")
        print(f"Rules Engine only achieving {rules_success_rate:.1%} accuracy (need ≥85%)")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)