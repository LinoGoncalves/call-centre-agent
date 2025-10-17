"""
Enhanced Vector Metadata Schema for Intelligent Routing
Demonstrates the proper structure for historical tickets with actual routing outcomes
"""

from datetime import datetime, UTC
from typing import Dict, List, Optional, Any

# 🎯 ENHANCED HISTORICAL TICKETS WITH ACTUAL ROUTING INTELLIGENCE
HISTORICAL_TICKETS_WITH_ROUTING = [
    {
        "ticket_id": "HIST-001",
        "text": "My internet connection keeps dropping every few minutes. Very frustrating!",
        "created_at": "2024-11-15T09:30:00Z",
        
        # 🎯 ACTUAL ROUTING OUTCOMES (Ground Truth)
        "actual_department": "technical_support_l2",  # Where it was ACTUALLY routed
        "actual_agent_id": "AGT-TEC-007",            # Specific agent who handled it
        "actual_team": "network_infrastructure",      # Sub-team within department
        "routing_decision_time": "00:02:30",         # How long routing took
        "first_contact_resolution": False,           # Was it resolved on first contact?
        "escalation_path": ["l1_support", "l2_network", "field_technician"],
        
        # 📈 RESOLUTION METRICS
        "resolution_time_hours": 4.5,               # Total time to resolve
        "customer_satisfaction": 8.2,               # Post-resolution CSAT score
        "resolution_type": "field_visit_required",   # How it was ultimately resolved
        "final_outcome": "resolved_satisfactory",    # Final status
        
        # 🤖 AI PREDICTION COMPARISON (if available)
        "initial_ai_prediction": "technical_support_l1",
        "ai_confidence_score": 0.91,
        "prediction_was_correct": False,             # L1 couldn't handle, needed L2
        "ai_model_version": "v2.3.1",
        
        # 🏷️ BUSINESS CONTEXT
        "customer_tier": "enterprise",               # Customer importance
        "service_type": "fiber_business",            # Product context
        "urgency_business": "high",                  # Business impact
        "urgency_customer": "critical",              # Customer perception
        
        # 📊 CONTENT ANALYSIS
        "sentiment_score": -0.7,                    # Negative sentiment
        "language": "en",
        "channel": "web_portal",                     # How ticket was submitted
        "customer_history": "3_previous_network_issues",
        
        # 🏷️ MANUAL ANNOTATIONS
        "agent_tags": ["wifi", "drops", "intermittent", "business_critical"],
        "supervisor_notes": "Customer has ongoing infrastructure issues, needs field visit",
        "knowledge_base_articles": ["KB-001", "KB-045", "KB-089"],
    },
    
    {
        "ticket_id": "HIST-002", 
        "text": "I received duplicate charges on my monthly bill. Please help resolve this.",
        "created_at": "2024-11-14T14:20:00Z",
        
        # 🎯 ACTUAL ROUTING OUTCOMES
        "actual_department": "billing_disputes",
        "actual_agent_id": "AGT-BIL-003",
        "actual_team": "billing_corrections",
        "routing_decision_time": "00:00:45",        # Quick routing decision
        "first_contact_resolution": True,           # Resolved immediately
        "escalation_path": ["billing_l1"],         # No escalation needed
        
        # 📈 RESOLUTION METRICS  
        "resolution_time_hours": 0.25,             # 15 minutes total
        "customer_satisfaction": 9.1,              # High satisfaction
        "resolution_type": "system_correction",     # Automated billing fix
        "final_outcome": "resolved_refunded",
        
        # 🤖 AI PREDICTION COMPARISON
        "initial_ai_prediction": "billing_disputes",
        "ai_confidence_score": 0.95,
        "prediction_was_correct": True,             # Perfect AI prediction
        "ai_model_version": "v2.3.1",
        
        # 🏷️ BUSINESS CONTEXT
        "customer_tier": "standard",
        "service_type": "residential_mobile", 
        "urgency_business": "medium",
        "urgency_customer": "high",
        
        # 📊 CONTENT ANALYSIS
        "sentiment_score": 0.2,                    # Slightly positive (polite)
        "language": "en",
        "channel": "chat",
        "customer_history": "no_previous_billing_issues",
        
        # 🏷️ MANUAL ANNOTATIONS
        "agent_tags": ["duplicate_charge", "billing_error", "easy_fix"],
        "supervisor_notes": "Standard billing correction, resolved via system adjustment",
        "knowledge_base_articles": ["KB-200", "KB-205"],
    },
    
    {
        "ticket_id": "HIST-003",
        "text": "Cannot access my account online. Password reset not working.",
        "created_at": "2024-11-13T10:15:00Z",
        
        # 🎯 ACTUAL ROUTING OUTCOMES
        "actual_department": "account_security",     # Security issue, not just tech support
        "actual_agent_id": "AGT-SEC-012",
        "actual_team": "identity_verification",
        "routing_decision_time": "00:05:20",        # Took time to identify security concern
        "first_contact_resolution": False,
        "escalation_path": ["tech_support_l1", "account_security", "fraud_prevention"],
        
        # 📈 RESOLUTION METRICS
        "resolution_time_hours": 2.0,
        "customer_satisfaction": 7.5,
        "resolution_type": "identity_verification_required",
        "final_outcome": "resolved_secure_reset",
        
        # 🤖 AI PREDICTION COMPARISON  
        "initial_ai_prediction": "technical_support_l1",
        "ai_confidence_score": 0.78,
        "prediction_was_correct": False,            # Missed the security aspect
        "ai_model_version": "v2.3.1",
        
        # 🏷️ BUSINESS CONTEXT
        "customer_tier": "premium",
        "service_type": "residential_bundle",
        "urgency_business": "medium", 
        "urgency_customer": "high",
        
        # 📊 CONTENT ANALYSIS
        "sentiment_score": -0.3,                   # Mildly frustrated
        "language": "en",
        "channel": "phone",
        "customer_history": "recent_address_change", # Security red flag!
        
        # 🏷️ MANUAL ANNOTATIONS
        "agent_tags": ["account_access", "password", "security_concern", "identity_check"],
        "supervisor_notes": "Required identity verification due to recent address change",
        "knowledge_base_articles": ["KB-300", "KB-315", "KB-320"],
        "security_flags": ["recent_address_change", "multiple_reset_attempts"],
    }
]

def create_enhanced_vector_metadata(historical_ticket: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create enhanced metadata structure for vector storage that captures
    actual routing intelligence for training automated routing systems.
    """
    
    return {
        # 🆔 IDENTIFIERS
        "ticket_id": historical_ticket["ticket_id"],
        "created_at": historical_ticket["created_at"],
        
        # 📝 CONTENT 
        "text": historical_ticket["text"][:500],  # Truncated for metadata limits
        "language": historical_ticket.get("language", "en"),
        "channel": historical_ticket.get("channel", "unknown"),
        
        # 🎯 GROUND TRUTH ROUTING (Critical for ML training)
        "actual_department": historical_ticket["actual_department"],
        "actual_agent_id": historical_ticket["actual_agent_id"], 
        "actual_team": historical_ticket["actual_team"],
        "escalation_path": historical_ticket.get("escalation_path", []),
        "first_contact_resolution": historical_ticket["first_contact_resolution"],
        
        # 📈 OUTCOME METRICS (Success indicators)
        "resolution_time_hours": historical_ticket["resolution_time_hours"],
        "customer_satisfaction": historical_ticket.get("customer_satisfaction"),
        "resolution_type": historical_ticket["resolution_type"],
        "final_outcome": historical_ticket["final_outcome"],
        
        # 🤖 AI LEARNING DATA (Model improvement)
        "initial_ai_prediction": historical_ticket.get("initial_ai_prediction"),
        "ai_confidence_score": historical_ticket.get("ai_confidence_score"),
        "prediction_was_correct": historical_ticket.get("prediction_was_correct"),
        "ai_model_version": historical_ticket.get("ai_model_version"),
        
        # 🏷️ BUSINESS INTELLIGENCE
        "customer_tier": historical_ticket["customer_tier"],
        "service_type": historical_ticket["service_type"],
        "urgency_business": historical_ticket["urgency_business"],
        "urgency_customer": historical_ticket["urgency_customer"],
        "sentiment_score": historical_ticket["sentiment_score"],
        
        # 🔍 SEARCHABLE TAGS
        "agent_tags": historical_ticket.get("agent_tags", []),
        "security_flags": historical_ticket.get("security_flags", []),
        
        # 📚 KNOWLEDGE LINKS
        "knowledge_base_articles": historical_ticket.get("knowledge_base_articles", []),
        
        # ⚡ ROUTING PERFORMANCE
        "routing_decision_time": historical_ticket.get("routing_decision_time"),
        "routing_accuracy": historical_ticket.get("prediction_was_correct", False),
    }

def demonstrate_similarity_search_for_routing(new_ticket_text: str):
    """
    Demonstrate how enhanced metadata enables intelligent routing decisions
    based on historical outcomes.
    """
    
    print(f"🔍 New Ticket: '{new_ticket_text}'")
    print("\n🎯 Similarity Search Results with Routing Intelligence:")
    print("=" * 70)
    
    for i, ticket in enumerate(HISTORICAL_TICKETS_WITH_ROUTING[:2], 1):
        metadata = create_enhanced_vector_metadata(ticket)
        
        print(f"\n{i}. Similarity Score: 0.89 (mock)")
        print(f"   Historical Ticket: {ticket['text'][:80]}...")
        print(f"   ✅ Actual Department: {metadata['actual_department']}")
        print(f"   ⏱️  Resolution Time: {metadata['resolution_time_hours']}h")
        print(f"   😊 Satisfaction: {metadata.get('customer_satisfaction', 'N/A')}")
        print(f"   🎯 AI Was Correct: {metadata.get('prediction_was_correct', 'N/A')}")
        print(f"   🏷️  Key Tags: {', '.join(metadata.get('agent_tags', [])[:3])}")
        
        # 🚀 ROUTING RECOMMENDATION
        satisfaction = metadata.get('customer_satisfaction', 0)
        if metadata.get('prediction_was_correct') and satisfaction > 8:
            confidence = "HIGH"
            recommendation = f"Route to {metadata['actual_department']} (proven successful)"
        elif metadata['resolution_time_hours'] < 1:
            confidence = "MEDIUM" 
            recommendation = f"Quick resolution likely in {metadata['actual_department']}"
        else:
            confidence = "LOW"
            recommendation = f"Consider {metadata['actual_department']} but review escalation path"
            
        print(f"   🚀 Routing Recommendation: {recommendation} (Confidence: {confidence})")

if __name__ == "__main__":
    print("🎯 Enhanced Vector Metadata Schema for Intelligent Routing")
    print("=" * 60)
    
    # Demonstrate with a new ticket
    new_ticket = "My wifi keeps disconnecting during video calls, affecting my work meetings"
    demonstrate_similarity_search_for_routing(new_ticket)
    
    print("\n" + "=" * 60)
    print("💡 Key Insight: With actual routing outcomes in metadata, the AI can learn:")
    print("   • Which departments ACTUALLY solve specific problems")
    print("   • How long resolution typically takes")
    print("   • Which initial predictions were wrong (and why)")
    print("   • Customer satisfaction patterns by routing decision")
    print("   • Escalation paths that lead to successful outcomes")