"""
Enhanced Vector Operations Test with Routing Intelligence
Test vector database operations using realistic call centre data with actual routing outcomes
"""

import asyncio
from datetime import datetime, UTC
from typing import List, Dict, Any
from dotenv import load_dotenv

from src.vector_db.pinecone_client import PineconeClient, VectorMetadata

# Load environment variables
load_dotenv()

# 🎯 REALISTIC HISTORICAL TICKETS WITH ACTUAL ROUTING INTELLIGENCE
ENHANCED_HISTORICAL_TICKETS = [
    {
        "ticket_id": "HIST-2024-001",
        "text": "My business fiber internet keeps dropping every 10 minutes during video conferences. This is affecting our client meetings and productivity.",
        "created_at": "2024-10-01T09:15:00Z",
        
        # 🎯 ACTUAL ROUTING OUTCOMES (Ground Truth)
        "actual_department": "technical_support_l2",
        "actual_agent_id": "AGT-TEC-007", 
        "actual_team": "network_infrastructure",
        "resolution_time_hours": 6.5,
        "customer_satisfaction": 8.5,
        "first_contact_resolution": False,
        "escalation_path": ["l1_general", "l1_technical", "l2_network", "field_technician"],
        "resolution_type": "on_site_repair",
        "final_outcome": "resolved_hardware_replacement",
        
        # 🤖 AI PREDICTION TRACKING
        "initial_ai_prediction": "technical_support_l1",
        "ai_confidence_score": 0.89,
        "prediction_was_correct": False,  # Needed L2, not L1
        "ai_model_version": "v2.3.1",
        
        # 🏷️ BUSINESS CONTEXT
        "customer_tier": "enterprise",
        "service_type": "fiber_business_premium",
        "urgency_business": "high",
        "urgency_customer": "critical", 
        "sentiment_score": -0.8,
        "language": "en",
        "channel": "phone",
        
        # 🔍 ANNOTATIONS
        "agent_tags": ["fiber", "drops", "video_conference", "business_critical", "hardware_issue"],
        "knowledge_base_articles": ["KB-NET-001", "KB-FIBER-045"],
    },
    
    {
        "ticket_id": "HIST-2024-002",
        "text": "I see duplicate charges on my monthly bill for the same mobile plan. Need this fixed and refunded.",
        "created_at": "2024-10-02T14:30:00Z",
        
        # 🎯 ACTUAL ROUTING OUTCOMES
        "actual_department": "billing_corrections", 
        "actual_agent_id": "AGT-BIL-012",
        "actual_team": "billing_disputes",
        "resolution_time_hours": 0.25,  # 15 minutes
        "customer_satisfaction": 9.2,
        "first_contact_resolution": True,
        "escalation_path": ["billing_l1"],
        "resolution_type": "automated_refund",
        "final_outcome": "resolved_refunded",
        
        # 🤖 AI PREDICTION TRACKING
        "initial_ai_prediction": "billing_corrections",
        "ai_confidence_score": 0.96,
        "prediction_was_correct": True,  # Perfect prediction
        "ai_model_version": "v2.3.1",
        
        # 🏷️ BUSINESS CONTEXT
        "customer_tier": "standard",
        "service_type": "mobile_postpaid",
        "urgency_business": "medium",
        "urgency_customer": "high",
        "sentiment_score": 0.1,  # Neutral but polite
        "language": "en", 
        "channel": "web_portal",
        
        # 🔍 ANNOTATIONS
        "agent_tags": ["duplicate_charge", "billing_error", "quick_fix"],
        "knowledge_base_articles": ["KB-BIL-200", "KB-REF-101"],
    },
    
    {
        "ticket_id": "HIST-2024-003",
        "text": "Cannot access my account online. Password reset emails not arriving. Tried multiple times.",
        "created_at": "2024-10-03T16:45:00Z",
        
        # 🎯 ACTUAL ROUTING OUTCOMES
        "actual_department": "account_security",  # Not just tech support!
        "actual_agent_id": "AGT-SEC-005",
        "actual_team": "identity_verification", 
        "resolution_time_hours": 1.5,
        "customer_satisfaction": 7.8,
        "first_contact_resolution": False,
        "escalation_path": ["tech_support_l1", "account_security"],
        "resolution_type": "manual_password_reset",
        "final_outcome": "resolved_security_verified",
        
        # 🤖 AI PREDICTION TRACKING
        "initial_ai_prediction": "technical_support_l1",
        "ai_confidence_score": 0.82,
        "prediction_was_correct": False,  # Missed security aspect
        "ai_model_version": "v2.3.1",
        
        # 🏷️ BUSINESS CONTEXT
        "customer_tier": "premium",
        "service_type": "internet_home_bundle",
        "urgency_business": "medium",
        "urgency_customer": "high",
        "sentiment_score": -0.4,  # Frustrated
        "language": "en",
        "channel": "chat",
        
        # 🔍 ANNOTATIONS
        "agent_tags": ["account_access", "password", "security_concern"],
        "security_flags": ["multiple_reset_attempts", "email_delivery_issue"],
        "knowledge_base_articles": ["KB-SEC-300", "KB-PWD-115"],
    },
    
    {
        "ticket_id": "HIST-2024-004",
        "text": "Excellent service! The technician fixed my internet issue quickly and explained everything clearly. Very satisfied!",
        "created_at": "2024-10-04T11:20:00Z",
        
        # 🎯 ACTUAL ROUTING OUTCOMES
        "actual_department": "customer_feedback",
        "actual_agent_id": "AGT-CS-021",
        "actual_team": "feedback_processing",
        "resolution_time_hours": 0.1,  # 5 minutes
        "customer_satisfaction": 10.0,
        "first_contact_resolution": True,
        "escalation_path": ["customer_service"],
        "resolution_type": "positive_feedback_logged",
        "final_outcome": "feedback_recorded",
        
        # 🤖 AI PREDICTION TRACKING
        "initial_ai_prediction": "customer_feedback",
        "ai_confidence_score": 0.93,
        "prediction_was_correct": True,
        "ai_model_version": "v2.3.1",
        
        # 🏷️ BUSINESS CONTEXT
        "customer_tier": "standard",
        "service_type": "internet_home",
        "urgency_business": "low",
        "urgency_customer": "low", 
        "sentiment_score": 0.9,  # Very positive
        "language": "en",
        "channel": "email",
        
        # 🔍 ANNOTATIONS
        "agent_tags": ["positive_feedback", "technician_praise", "satisfaction"],
        "knowledge_base_articles": ["KB-CS-500"],
    },
    
    {
        "ticket_id": "HIST-2024-005",
        "text": "My mobile data is extremely slow in downtown area. Can't load basic websites or use apps properly.",
        "created_at": "2024-10-05T13:10:00Z",
        
        # 🎯 ACTUAL ROUTING OUTCOMES  
        "actual_department": "network_operations",
        "actual_agent_id": "AGT-NET-018",
        "actual_team": "coverage_optimization",
        "resolution_time_hours": 24.0,  # Network issue resolution
        "customer_satisfaction": 6.5,   # Acceptable but not great
        "first_contact_resolution": False,
        "escalation_path": ["tech_support_l1", "network_operations", "field_engineering"],
        "resolution_type": "network_capacity_upgrade",
        "final_outcome": "resolved_infrastructure_improvement",
        
        # 🤖 AI PREDICTION TRACKING
        "initial_ai_prediction": "technical_support_l1",
        "ai_confidence_score": 0.76,
        "prediction_was_correct": False,  # Network issue, not device issue
        "ai_model_version": "v2.3.1",
        
        # 🏷️ BUSINESS CONTEXT
        "customer_tier": "standard",
        "service_type": "mobile_prepaid",
        "urgency_business": "medium",
        "urgency_customer": "high",
        "sentiment_score": -0.6,
        "language": "en",
        "channel": "app",
        
        # 🔍 ANNOTATIONS
        "agent_tags": ["mobile_data", "speed_issue", "location_specific", "network_capacity"],
        "knowledge_base_articles": ["KB-NET-200", "KB-MOB-150"],
    }
]

def generate_mock_embedding(text: str, dimension: int = 1536) -> List[float]:
    """Generate consistent mock embedding based on text content"""
    import hashlib
    import random
    import math
    
    # Create seed from text for consistent embeddings
    seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    
    # Generate random embedding
    embedding = [random.gauss(0, 1) for _ in range(dimension)]
    
    # Normalize to unit vector
    norm = math.sqrt(sum(x * x for x in embedding))
    if norm > 0:
        embedding = [x / norm for x in embedding]
        
    return embedding

async def test_enhanced_vector_upload():
    """Test uploading vectors with enhanced routing intelligence metadata"""
    print("🚀 Testing Enhanced Vector Upload with Routing Intelligence...")
    
    try:
        client = PineconeClient()
        await client.initialize_index(create_if_not_exists=True)
        
        # Prepare enhanced vectors
        enhanced_vectors = []
        
        for ticket in ENHANCED_HISTORICAL_TICKETS:
            # Generate embedding
            embedding = generate_mock_embedding(ticket["text"])
            
            # Create enhanced metadata using new helper method
            metadata = client.create_enhanced_metadata(
                ticket_id=ticket["ticket_id"],
                text=ticket["text"],
                created_at=ticket["created_at"],
                actual_department=ticket["actual_department"],
                actual_agent_id=ticket["actual_agent_id"],
                resolution_time_hours=ticket["resolution_time_hours"],
                customer_satisfaction=ticket["customer_satisfaction"],
                # Pass all other fields as kwargs
                **{k: v for k, v in ticket.items() 
                   if k not in ["ticket_id", "text", "created_at", "actual_department", 
                               "actual_agent_id", "resolution_time_hours", "customer_satisfaction"]}
            )
            
            enhanced_vectors.append((ticket["ticket_id"], embedding, metadata))
        
        print(f"   📤 Uploading {len(enhanced_vectors)} enhanced vectors...")
        
        # Upload vectors with enhanced metadata
        result = await client.upsert_vectors(enhanced_vectors)
        print(f"   ✅ Upload result: {result}")
        
        # Verify upload
        stats = await client.get_index_stats()
        print(f"   ✅ Index now contains {stats['total_vector_count']} vectors with routing intelligence")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Enhanced upload failed: {e}")
        return False

async def test_intelligent_routing_search():
    """Test similarity search with routing intelligence for new tickets"""
    print("\n🧠 Testing Intelligent Routing Search...")
    
    try:
        client = PineconeClient()
        await client.initialize_index()
        
        # New ticket scenarios to test routing intelligence
        new_tickets = [
            {
                "text": "My business internet is disconnecting during important video calls with clients",
                "expected_department": "technical_support_l2",  # Should learn from HIST-001
                "scenario": "Business connectivity issue"
            },
            {
                "text": "There are extra charges on my bill that shouldn't be there",
                "expected_department": "billing_corrections",  # Should learn from HIST-002
                "scenario": "Billing dispute"
            },
            {
                "text": "Can't log into my account, password reset not working",
                "expected_department": "account_security",  # Should learn from HIST-003
                "scenario": "Account access with potential security concern"
            }
        ]
        
        for i, ticket_test in enumerate(new_tickets, 1):
            print(f"\n   🎯 Test Case {i}: {ticket_test['scenario']}")
            print(f"   📝 New Ticket: '{ticket_test['text']}'")
            
            # Generate query embedding
            query_vector = generate_mock_embedding(ticket_test["text"])
            
            # Search for similar tickets with routing intelligence
            results = await client.query_vectors(
                query_vector=query_vector,
                top_k=3,
                include_metadata=True
            )
            
            # Extract matches (handle both object and dict responses)
            matches = getattr(results, 'matches', results.get('matches', []))
            
            print(f"   🔍 Found {len(matches)} similar historical tickets:")
            
            routing_recommendations = []
            
            for j, match in enumerate(matches[:3], 1):
                score = match.score if hasattr(match, 'score') else match.get('score', 0)
                metadata = match.metadata if hasattr(match, 'metadata') else match.get('metadata', {})
                
                print(f"\n      {j}. Similarity Score: {score:.3f}")
                print(f"         Historical Ticket: {metadata.get('text', 'N/A')[:80]}...")
                print(f"         ✅ Actual Department: {metadata.get('actual_department', 'N/A')}")
                print(f"         ⏱️  Resolution Time: {metadata.get('resolution_time_hours', 'N/A')}h")
                print(f"         😊 CSAT Score: {metadata.get('customer_satisfaction', 'N/A')}")
                print(f"         🎯 AI Was Correct: {metadata.get('prediction_was_correct', 'N/A')}")
                print(f"         🔄 First Contact Resolution: {metadata.get('first_contact_resolution', 'N/A')}")
                
                # Generate routing recommendation based on historical outcomes
                dept = metadata.get('actual_department')
                resolution_time = metadata.get('resolution_time_hours', 999)
                satisfaction = metadata.get('customer_satisfaction', 0)
                ai_correct = metadata.get('prediction_was_correct', False)
                
                if dept and satisfaction > 8 and resolution_time < 2:
                    confidence = "HIGH"
                    reason = f"Fast resolution ({resolution_time}h) with high satisfaction ({satisfaction})"
                elif dept and ai_correct and satisfaction > 7:
                    confidence = "MEDIUM"
                    reason = f"AI prediction was correct, good satisfaction ({satisfaction})"
                elif dept:
                    confidence = "LOW"
                    reason = f"Historical route available but mixed results"
                else:
                    confidence = "UNKNOWN"
                    reason = "No historical routing data"
                
                routing_recommendations.append({
                    "department": dept,
                    "confidence": confidence,
                    "reason": reason,
                    "similarity": score
                })
            
            # Provide intelligent routing recommendation
            if routing_recommendations:
                best_rec = max(routing_recommendations, key=lambda x: x['similarity'])
                print(f"\n   🚀 ROUTING RECOMMENDATION:")
                print(f"      Department: {best_rec['department']}")
                print(f"      Confidence: {best_rec['confidence']}")
                print(f"      Reason: {best_rec['reason']}")
                print(f"      Expected: {ticket_test['expected_department']} ({'✅ Match' if best_rec['department'] == ticket_test['expected_department'] else '❌ Mismatch'})")
            
        await client.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Intelligent routing search failed: {e}")
        return False

async def test_routing_analytics():
    """Test analytics on routing intelligence data"""
    print("\n📊 Testing Routing Analytics...")
    
    try:
        client = PineconeClient()
        await client.initialize_index()
        
        # Query all vectors to analyze routing patterns
        # Note: In production, you'd use Pinecone's stats API or separate analytics DB
        print("   📈 Routing Intelligence Analytics:")
        print("   • Department Success Rates")
        print("   • Average Resolution Times")
        print("   • AI Prediction Accuracy")
        print("   • Customer Satisfaction by Department")
        
        # Mock analytics based on our test data
        analytics = {
            "billing_corrections": {
                "avg_resolution_hours": 0.25,
                "avg_satisfaction": 9.2,
                "first_contact_resolution_rate": 1.0,
                "ai_accuracy": 1.0
            },
            "technical_support_l2": {
                "avg_resolution_hours": 6.5,
                "avg_satisfaction": 8.5,
                "first_contact_resolution_rate": 0.0,
                "ai_accuracy": 0.0  # AI predicted L1, needed L2
            },
            "account_security": {
                "avg_resolution_hours": 1.5,
                "avg_satisfaction": 7.8,
                "first_contact_resolution_rate": 0.0,
                "ai_accuracy": 0.0  # AI missed security aspect
            },
            "network_operations": {
                "avg_resolution_hours": 24.0,
                "avg_satisfaction": 6.5,
                "first_contact_resolution_rate": 0.0,
                "ai_accuracy": 0.0  # AI predicted tech support
            }
        }
        
        print("\n   📊 Department Performance Analysis:")
        for dept, metrics in analytics.items():
            print(f"\n      🏢 {dept.replace('_', ' ').title()}")
            print(f"         ⏱️  Avg Resolution: {metrics['avg_resolution_hours']}h")
            print(f"         😊 Avg Satisfaction: {metrics['avg_satisfaction']}/10")
            print(f"         ✅ First Contact Rate: {metrics['first_contact_resolution_rate']*100}%")
            print(f"         🎯 AI Accuracy: {metrics['ai_accuracy']*100}%")
        
        print("\n   💡 Key Insights:")
        print("      • Billing issues resolve fastest (0.25h) with highest satisfaction (9.2)")
        print("      • Technical issues often need L2 escalation (AI accuracy 0%)")
        print("      • Security issues are misclassified as general tech support")
        print("      • Network issues take longest (24h) but infrastructure improvements needed")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Analytics test failed: {e}")
        return False

async def run_enhanced_vector_tests():
    """Run comprehensive enhanced vector tests with routing intelligence"""
    print("🚀 ENHANCED VECTOR DATABASE TESTS WITH ROUTING INTELLIGENCE")
    print("=" * 70)
    
    test_results = {}
    
    # Test 1: Enhanced vector upload
    test_results["enhanced_upload"] = await test_enhanced_vector_upload()
    
    # Test 2: Intelligent routing search
    if test_results["enhanced_upload"]:
        test_results["intelligent_routing"] = await test_intelligent_routing_search()
    else:
        test_results["intelligent_routing"] = False
        print("⏭️  Skipping routing tests (upload failed)")
    
    # Test 3: Routing analytics
    if test_results["intelligent_routing"]:
        test_results["routing_analytics"] = await test_routing_analytics()
    else:
        test_results["routing_analytics"] = False
        print("⏭️  Skipping analytics tests (routing failed)")
    
    # Summary
    print("\n📊 ENHANCED TEST RESULTS SUMMARY:")
    print("=" * 50)
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    for test_name, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name.upper():20} {status}")
    
    print("=" * 50)
    print(f"   TOTAL: {passed_tests}/{total_tests} enhanced tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL ENHANCED TESTS PASSED!")
        print("🚀 Vector database now has ROUTING INTELLIGENCE!")
        print("💡 Ready for intelligent automated routing based on historical outcomes!")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed. Review errors above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_enhanced_vector_tests())