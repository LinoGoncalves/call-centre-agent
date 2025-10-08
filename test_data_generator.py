"""
📊 Mock Test Data for Rules Engine + RAG Pipeline Validation
===========================================================

This dataset contains comprehensive test cases that validate both:
1. Rules Engine: High-confidence pattern matches (85%+ confidence)
2. RAG System: Complex scenarios requiring LLM reasoning and context

Data Structure:
- rules_engine_tests: Tickets that should trigger specific rules
- rag_system_tests: Complex tickets requiring LLM analysis
- edge_cases: Borderline scenarios to test thresholds
- performance_tests: High-volume data for benchmarking

Usage:
    from test_data_generator import MockDataGenerator
    generator = MockDataGenerator()
    data = generator.generate_comprehensive_test_set()
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random

class MockDataGenerator:
    """Generate comprehensive mock data for testing Rules Engine and RAG pipeline."""
    
    def __init__(self):
        self.ticket_counter = 1000
        
    def generate_comprehensive_test_set(self) -> Dict[str, Any]:
        """Generate complete test dataset covering all scenarios."""
        
        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_tickets": 50,
                "rules_engine_expected": 30,
                "rag_system_expected": 20,
                "description": "Comprehensive test data for Rules Engine and RAG validation"
            },
            "rules_engine_tests": self._generate_rules_engine_data(),
            "rag_system_tests": self._generate_rag_test_data(),
            "edge_cases": self._generate_edge_cases(),
            "performance_tests": self._generate_performance_data()
        }
    
    def _generate_rules_engine_data(self) -> List[Dict[str, Any]]:
        """Generate test cases that should trigger specific rules with high confidence."""
        
        # Each test case maps to a specific rule from the TelcoRulesEngine
        test_cases = [
            # R001_DISPUTE_EXPLICIT (98% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I dispute this R500 charge on my bill - I never authorized this premium service subscription",
                "expected_rule": "R001_DISPUTE_EXPLICIT",
                "expected_department": "credit_management",
                "expected_confidence": 0.98,
                "expected_urgency": "High",
                "customer_tier": "Gold",
                "category": "DISPUTE_EXPLICIT"
            },
            {
                "ticket_id": self._next_ticket_id(),
                "text": "This billing is incorrect - I disagree with the international charges on my statement",
                "expected_rule": "R001_DISPUTE_EXPLICIT",
                "expected_department": "credit_management",
                "expected_confidence": 0.98,
                "expected_urgency": "High",
                "customer_tier": "Silver",
                "category": "DISPUTE_BILLING"
            },
            
            # R002_REFUND_REQUEST (95% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "Please refund the duplicate charge on my account from last week's payment",
                "expected_rule": "R002_REFUND_REQUEST",
                "expected_department": "credit_management",
                "expected_confidence": 0.95,
                "expected_urgency": "High",
                "customer_tier": "Platinum",
                "category": "REFUND_REQUEST"
            },
            {
                "ticket_id": self._next_ticket_id(),
                "text": "There's a billing error on my statement - please credit my account for the overcharge",
                "expected_rule": "R002_REFUND_REQUEST",
                "expected_department": "credit_management",
                "expected_confidence": 0.95,
                "expected_urgency": "High",
                "customer_tier": "Bronze",
                "category": "BILLING_ERROR"
            },
            
            # R003_DOUBLE_BILLING (97% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I was charged twice for my monthly data package - please investigate this duplicate charge",
                "expected_rule": "R003_DOUBLE_BILLING",
                "expected_department": "credit_management",
                "expected_confidence": 0.97,
                "expected_urgency": "High",
                "customer_tier": "Gold",
                "category": "DUPLICATE_BILLING"
            },
            
            # R004_ACCOUNT_LOCKED (99% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "My account is locked and I cannot login to the customer portal to pay my bill",
                "expected_rule": "R004_ACCOUNT_LOCKED",
                "expected_department": "technical_support_l2",
                "expected_confidence": 0.99,
                "expected_urgency": "High",
                "customer_tier": "Silver",
                "category": "ACCOUNT_ACCESS"
            },
            {
                "ticket_id": self._next_ticket_id(),
                "text": "Access denied when trying to login - says account locked for security reasons",
                "expected_rule": "R004_ACCOUNT_LOCKED",
                "expected_department": "technical_support_l2",
                "expected_confidence": 0.99,
                "expected_urgency": "High",
                "customer_tier": "Gold",
                "category": "LOGIN_BLOCKED"
            },
            
            # R005_PASSWORD_RESET (92% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I forgot my password and need to reset it to access my online account",
                "expected_rule": "R005_PASSWORD_RESET",
                "expected_department": "technical_support_l1",
                "expected_confidence": 0.92,
                "expected_urgency": "Medium",
                "customer_tier": "Bronze",
                "category": "PASSWORD_ISSUE"
            },
            
            # R006_SECURITY_BREACH (98% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "URGENT: I think there's been unauthorized access to my account - possible security breach",
                "expected_rule": "R006_SECURITY_BREACH",
                "expected_department": "security_team",
                "expected_confidence": 0.98,
                "expected_urgency": "Critical",
                "customer_tier": "Platinum",
                "category": "SECURITY_INCIDENT"
            },
            
            # R007_SERVICE_OUTAGE (94% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "The internet service is down in my area - no connection for the past 3 hours",
                "expected_rule": "R007_SERVICE_OUTAGE",
                "expected_department": "technical_support_l2",
                "expected_confidence": 0.94,
                "expected_urgency": "High",
                "customer_tier": "Gold",
                "category": "SERVICE_DOWN"
            },
            {
                "ticket_id": self._next_ticket_id(),
                "text": "Complete network outage - cannot connect to internet or make calls",
                "expected_rule": "R007_SERVICE_OUTAGE",
                "expected_department": "technical_support_l2",
                "expected_confidence": 0.94,
                "expected_urgency": "High",
                "customer_tier": "Silver",
                "category": "NETWORK_OUTAGE"
            },
            
            # R008_SLOW_INTERNET (89% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "My internet connection is extremely slow - speed test shows only 2 Mbps instead of 50 Mbps",
                "expected_rule": "R008_SLOW_INTERNET",
                "expected_department": "technical_support_l1",
                "expected_confidence": 0.89,
                "expected_urgency": "Medium",
                "customer_tier": "Bronze",
                "category": "SPEED_ISSUE"
            },
            
            # R009_BILLING_INQUIRY (87% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "Can you please explain my bill - I don't understand some of the charges listed",
                "expected_rule": "R009_BILLING_INQUIRY",
                "expected_department": "billing_team",
                "expected_confidence": 0.87,
                "expected_urgency": "Medium",
                "customer_tier": "Silver",
                "category": "BILL_EXPLANATION"
            },
            
            # R010_PAYMENT_ISSUES (91% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "My payment failed when trying to pay online - card was declined but should work fine",
                "expected_rule": "R010_PAYMENT_ISSUES",
                "expected_department": "billing_team",
                "expected_confidence": 0.91,
                "expected_urgency": "Medium",
                "customer_tier": "Gold",
                "category": "PAYMENT_FAILED"
            },
            
            # R011_NEW_SERVICE (93% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I want to setup a new internet service at my home - please schedule installation",
                "expected_rule": "R011_NEW_SERVICE",
                "expected_department": "order_management",
                "expected_confidence": 0.93,
                "expected_urgency": "Medium",
                "customer_tier": "Bronze",
                "category": "NEW_INSTALLATION"
            },
            
            # R012_UPGRADE_PLAN (88% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I need to upgrade my plan to get faster internet - current speed is not enough",
                "expected_rule": "R012_UPGRADE_PLAN",
                "expected_department": "order_management",
                "expected_confidence": 0.88,
                "expected_urgency": "Low",
                "customer_tier": "Silver",
                "category": "PLAN_UPGRADE"
            },
            
            # R013_RETENTION_RISK (91% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I'm thinking of leaving your service - the quality has been poor lately",
                "expected_rule": "R013_RETENTION_RISK",
                "expected_department": "crm_team",
                "expected_confidence": 0.91,
                "expected_urgency": "High",
                "customer_tier": "Platinum",
                "category": "CHURN_RISK"
            },
            {
                "ticket_id": self._next_ticket_id(),
                "text": "Considering switching to another provider due to poor service and high costs",
                "expected_rule": "R013_RETENTION_RISK",
                "expected_department": "crm_team",
                "expected_confidence": 0.91,
                "expected_urgency": "High",
                "customer_tier": "Gold",
                "category": "COMPETITOR_CONSIDERATION"
            },
            
            # R014_POSITIVE_FEEDBACK (85% confidence)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "Thank you for the excellent customer service - your technician was very helpful",
                "expected_rule": "R014_POSITIVE_FEEDBACK",
                "expected_department": "crm_team",
                "expected_confidence": 0.85,
                "expected_urgency": "Low",
                "customer_tier": "Gold",
                "category": "POSITIVE_FEEDBACK"
            }
        ]
        
        return test_cases
    
    def _generate_rag_test_data(self) -> List[Dict[str, Any]]:
        """Generate complex test cases requiring RAG/LLM analysis."""
        
        complex_scenarios = [
            # Multi-intent tickets requiring reasoning
            {
                "ticket_id": self._next_ticket_id(),
                "text": "Hi, I have several issues: my bill seems wrong, I want to upgrade my service, and also the internet has been slow. Can you help with all of these? Also, I'm not happy with the customer service I received last week.",
                "expected_category": "COMPLEX_MULTI_ISSUE",
                "expected_departments": ["billing_team", "order_management", "technical_support_l1", "crm_team"],
                "complexity": "High",
                "requires_reasoning": True,
                "customer_tier": "Platinum",
                "category": "MULTI_INTENT"
            },
            
            # Ambiguous language requiring context
            {
                "ticket_id": self._next_ticket_id(),
                "text": "There's something strange going on with my account. The numbers don't seem right and I'm concerned about what I'm seeing. Could you look into this please?",
                "expected_category": "AMBIGUOUS_CONCERN",
                "expected_departments": ["billing_team", "security_team"],
                "complexity": "High",
                "requires_reasoning": True,
                "customer_tier": "Silver",
                "category": "VAGUE_ISSUE"
            },
            
            # Technical issue with business context
            {
                "ticket_id": self._next_ticket_id(),
                "text": "Our business depends on reliable internet for video conferences with clients. The connection keeps dropping during important meetings, which is affecting our revenue. We need a technical solution and possibly compensation for lost business.",
                "expected_category": "BUSINESS_CRITICAL_TECHNICAL",
                "expected_departments": ["technical_support_l2", "crm_team", "credit_management"],
                "complexity": "High", 
                "requires_reasoning": True,
                "customer_tier": "Enterprise",
                "category": "BUSINESS_IMPACT"
            },
            
            # Emotional customer with legitimate concern
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I AM EXTREMELY FRUSTRATED!!! This is the THIRD TIME I'm calling about this issue and nobody seems to understand what I need. The billing department told me one thing, technical support said something else, and now I don't know what to believe. I just want my internet to work and my bill to be correct. Is that too much to ask???",
                "expected_category": "ESCALATED_EMOTIONAL_CUSTOMER",
                "expected_departments": ["crm_team", "billing_team", "technical_support_l2"],
                "complexity": "High",
                "requires_reasoning": True,
                "customer_tier": "Gold",
                "category": "EMOTIONAL_ESCALATION"
            },
            
            # Technical jargon mixed with complaint
            {
                "ticket_id": self._next_ticket_id(),
                "text": "The latency on my fiber connection is terrible - I'm getting 150ms ping times to local servers when it should be under 20ms. My VPN keeps timing out and my remote work is being impacted. I need level 2 technical support to check the routing tables and QoS settings.",
                "expected_category": "TECHNICAL_EXPERT_CUSTOMER",
                "expected_departments": ["technical_support_l2"],
                "complexity": "Medium",
                "requires_reasoning": True,
                "customer_tier": "Platinum", 
                "category": "TECHNICAL_SOPHISTICATED"
            },
            
            # Positive feedback with hidden issue
            {
                "ticket_id": self._next_ticket_id(),
                "text": "Thank you for finally fixing my internet issue after 2 weeks of problems. Your technician Sarah was very professional. However, I'm still concerned about the reliability going forward and would like to understand what caused the initial problem so it doesn't happen again.",
                "expected_category": "POSITIVE_WITH_FOLLOWUP",
                "expected_departments": ["crm_team", "technical_support_l2"],
                "complexity": "Medium",
                "requires_reasoning": True,
                "customer_tier": "Silver",
                "category": "GRATEFUL_BUT_CONCERNED"
            },
            
            # Regulatory/compliance concern
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I need to file a formal complaint with ICASA about your company's handling of my service issues. I've documented multiple failures to meet SLA commitments and want to understand my rights as a consumer. Can you provide me with your complaint handling process and escalation procedures?",
                "expected_category": "REGULATORY_COMPLAINT",
                "expected_departments": ["crm_team", "legal_team", "executive_escalation"],
                "complexity": "Critical",
                "requires_reasoning": True,
                "customer_tier": "Gold",
                "category": "LEGAL_REGULATORY"
            },
            
            # Cross-selling opportunity
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I love my current internet service and I'm wondering what other products you offer. My neighbor mentioned something about mobile plans and TV packages. Could you tell me about bundle deals that might save me money while giving me more services?",
                "expected_category": "SALES_OPPORTUNITY",
                "expected_departments": ["sales_team", "crm_team"],
                "complexity": "Low",
                "requires_reasoning": True,
                "customer_tier": "Bronze",
                "category": "UPSELL_INQUIRY"
            },
            
            # Account security with family context
            {
                "ticket_id": self._next_ticket_id(),
                "text": "My teenage son might have changed some settings on our family account and now I can't access certain features. I also noticed some charges for premium content that we didn't authorize. I need to reset the account to proper settings and understand parental controls.",
                "expected_category": "FAMILY_ACCOUNT_ISSUE",
                "expected_departments": ["technical_support_l1", "billing_team", "crm_team"],
                "complexity": "Medium",
                "requires_reasoning": True,
                "customer_tier": "Silver",
                "category": "FAMILY_MANAGEMENT"
            },
            
            # International roaming complaint
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I traveled to Europe last month and was shocked by roaming charges of R3000 on my bill. Your website said roaming was 'affordable' but didn't clearly explain the rates. I feel misled by your marketing and want these charges reviewed. I'm also concerned about data usage tracking while abroad.",
                "expected_category": "ROAMING_DISPUTE",
                "expected_departments": ["billing_team", "credit_management", "crm_team"],
                "complexity": "High",
                "requires_reasoning": True,
                "customer_tier": "Platinum",
                "category": "INTERNATIONAL_BILLING"
            }
        ]
        
        return complex_scenarios
    
    def _generate_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge cases that test threshold boundaries."""
        
        edge_cases = [
            # Just below rules threshold (should go to ML/LLM)
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I have a question about some charges on my account",  # Too vague for billing rule
                "expected_routing": "ml_llm_pipeline",
                "confidence_expected": 0.75,  # Below 0.85 threshold
                "category": "BELOW_RULES_THRESHOLD"
            },
            
            # Ambiguous dispute language
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I'm not sure if this charge is right - could you check it?",  # Uncertain, not explicit dispute
                "expected_routing": "ml_llm_pipeline", 
                "confidence_expected": 0.70,
                "category": "UNCERTAIN_DISPUTE"
            },
            
            # Technical issue but vague
            {
                "ticket_id": self._next_ticket_id(),
                "text": "Something is wrong with my internet connection",  # Too general for specific rule
                "expected_routing": "ml_llm_pipeline",
                "confidence_expected": 0.65,
                "category": "VAGUE_TECHNICAL"
            },
            
            # Multiple weak signals
            {
                "ticket_id": self._next_ticket_id(),
                "text": "I have concerns about my service quality and billing accuracy",  # Multiple areas, no strong pattern
                "expected_routing": "ml_llm_pipeline",
                "confidence_expected": 0.72,
                "category": "MULTIPLE_WEAK_SIGNALS"
            }
        ]
        
        return edge_cases
    
    def _generate_performance_data(self) -> List[Dict[str, Any]]:
        """Generate high-volume data for performance testing."""
        
        performance_cases = []
        
        # Generate variations of high-confidence rule matches
        dispute_variations = [
            "I dispute this charge completely",
            "This billing is totally wrong", 
            "I disagree with these unauthorized fees",
            "Incorrect charges on my statement",
            "This is an unauthorized billing error"
        ]
        
        for i in range(10):
            performance_cases.append({
                "ticket_id": self._next_ticket_id(),
                "text": random.choice(dispute_variations),
                "expected_rule": "R001_DISPUTE_EXPLICIT",
                "test_type": "performance",
                "batch": f"performance_batch_{i//5 + 1}"
            })
        
        return performance_cases
    
    def _next_ticket_id(self) -> str:
        """Generate next ticket ID."""
        self.ticket_counter += 1
        return f"TICKET_{self.ticket_counter:05d}"

def create_test_data_files():
    """Create comprehensive test data files for validation."""
    
    generator = MockDataGenerator()
    test_data = generator.generate_comprehensive_test_set()
    
    # Save complete dataset
    with open("comprehensive_test_data.json", "w") as f:
        json.dump(test_data, f, indent=2)
    
    # Create rules engine specific test file
    rules_tests = {
        "metadata": {
            "description": "High-confidence test cases that should trigger specific rules",
            "expected_matches": len(test_data["rules_engine_tests"]),
            "confidence_threshold": 0.85
        },
        "test_cases": test_data["rules_engine_tests"]
    }
    
    with open("rules_engine_test_data.json", "w") as f:
        json.dump(rules_tests, f, indent=2)
    
    # Create RAG system specific test file
    rag_tests = {
        "metadata": {
            "description": "Complex scenarios requiring LLM reasoning and context analysis", 
            "expected_llm_usage": len(test_data["rag_system_tests"]),
            "complexity_levels": ["Low", "Medium", "High", "Critical"]
        },
        "test_cases": test_data["rag_system_tests"]
    }
    
    with open("rag_system_test_data.json", "w") as f:
        json.dump(rag_tests, f, indent=2)
    
    # Create CSV for easy analysis
    import pandas as pd
    
    # Flatten rules engine tests
    rules_df_data = []
    for test in test_data["rules_engine_tests"]:
        rules_df_data.append({
            "ticket_id": test["ticket_id"],
            "ticket_text": test["text"],
            "expected_rule": test["expected_rule"],
            "expected_department": test["expected_department"],
            "expected_confidence": test["expected_confidence"],
            "expected_urgency": test["expected_urgency"],
            "customer_tier": test["customer_tier"],
            "category": test["category"]
        })
    
    rules_df = pd.DataFrame(rules_df_data)
    rules_df.to_csv("rules_engine_test_cases.csv", index=False)
    
    # Flatten RAG tests
    rag_df_data = []
    for test in test_data["rag_system_tests"]:
        rag_df_data.append({
            "ticket_id": test["ticket_id"],
            "ticket_text": test["text"],
            "expected_category": test["expected_category"],
            "complexity": test["complexity"],
            "requires_reasoning": test["requires_reasoning"],
            "customer_tier": test["customer_tier"],
            "category": test["category"]
        })
    
    rag_df = pd.DataFrame(rag_df_data)
    rag_df.to_csv("rag_system_test_cases.csv", index=False)
    
    print("📊 Test Data Files Created Successfully!")
    print(f"✅ comprehensive_test_data.json - Complete dataset ({len(test_data['rules_engine_tests']) + len(test_data['rag_system_tests'])} tickets)")
    print(f"✅ rules_engine_test_data.json - Rules Engine tests ({len(test_data['rules_engine_tests'])} tickets)")
    print(f"✅ rag_system_test_data.json - RAG system tests ({len(test_data['rag_system_tests'])} tickets)")
    print(f"✅ rules_engine_test_cases.csv - Rules Engine CSV")
    print(f"✅ rag_system_test_cases.csv - RAG system CSV")

if __name__ == "__main__":
    create_test_data_files()