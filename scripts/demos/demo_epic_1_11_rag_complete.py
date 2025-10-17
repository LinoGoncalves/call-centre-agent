"""
EPIC 1.11 COMPLETE DEMONSTRATION: RAG-Based LLM Prompting with Routing Intelligence
====================================================================================

This demonstration showcases the complete RAG (Retrieval-Augmented Generation) system
that uses historical routing intelligence to enhance LLM-based ticket classification.

Key Features Demonstrated:
- Enhanced similarity search with routing intelligence metadata
- Confidence-based routing decisions (cached routes vs LLM analysis) 
- RAG prompts with historical routing outcomes as few-shot examples
- Complete intelligent routing with evidence and reasoning
- Production-ready fallback handling for API limitations

Architecture:
1. IntelligentSimilaritySearch - Retrieves similar tickets with routing outcomes
2. RAGPromptTemplate - Creates few-shot prompts with historical intelligence
3. LLMClassifier - OpenAI GPT integration with RAG prompts
4. RAGIntelligentRouting - Complete system orchestration with confidence logic

This represents a significant advancement over traditional classification approaches
by leveraging actual routing success patterns from historical data.
"""

import asyncio
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.models.rag_intelligent_routing import (
    RAGIntelligentRouting,
    IntelligentSimilaritySearch, 
    RAGPromptTemplate
)


def print_banner(title: str, symbol: str = "=", width: int = 60):
    """Print a formatted banner"""
    print(f"\n{symbol * width}")
    print(f"{title:^{width}}")
    print(f"{symbol * width}")


def print_section(title: str):
    """Print a section header"""
    print(f"\n🔸 {title}")
    print("-" * (len(title) + 4))


async def demonstrate_similarity_search():
    """Demonstrate intelligent similarity search with routing intelligence"""
    
    print_section("Enhanced Similarity Search with Routing Intelligence")
    
    similarity_search = IntelligentSimilaritySearch()
    
    # Test case: Enterprise connectivity issue
    test_query = "My office fiber internet connection is unstable and drops during client calls"
    
    print(f"📝 Query Ticket: '{test_query}'")
    
    # Search for similar tickets
    matches = await similarity_search.search_similar_tickets_with_routing(
        query_text=test_query,
        top_k=3
    )
    
    print(f"\n🔍 Found {len(matches)} similar historical tickets:")
    
    for i, match in enumerate(matches, 1):
        print(f"\n   {i}. Ticket ID: {match.ticket_id}")
        print(f"      Similarity: {match.similarity_score:.3f}")
        print(f"      Text: {match.text}")
        print(f"      ✅ Actual Department: {match.actual_department}")
        if match.resolution_time_hours:
            print(f"      ⏱️ Resolution Time: {match.resolution_time_hours}h") 
        if match.customer_satisfaction:
            print(f"      😊 Satisfaction: {match.customer_satisfaction}/10")
        if match.first_contact_resolution is not None:
            fcr = "Yes" if match.first_contact_resolution else "No"
            print(f"      🎯 First Contact Resolution: {fcr}")
    
    # Analyze routing confidence
    recommendation = similarity_search.analyze_routing_confidence(matches)
    
    print("\n📊 ROUTING CONFIDENCE ANALYSIS:")
    print(f"   Recommended Department: {recommendation.recommended_department}")
    print(f"   Confidence Level: {recommendation.confidence.value}")
    print(f"   Use Cached Route: {recommendation.use_cached_route}")
    print(f"   Reasoning: {recommendation.reasoning}")
    print(f"   Historical Success Rate: {recommendation.success_rate:.1%}")
    
    return matches


async def demonstrate_rag_prompts(historical_matches):
    """Demonstrate RAG prompt generation with routing intelligence"""
    
    print_section("RAG Prompt Generation with Historical Intelligence")
    
    query_ticket = "My business internet keeps disconnecting during important video conferences"
    
    print(f"📝 New Ticket to Classify: '{query_ticket}'")
    
    # Generate RAG prompt with historical intelligence
    rag_prompt = RAGPromptTemplate.create_few_shot_prompt_with_routing_intelligence(
        query_ticket=query_ticket,
        historical_matches=historical_matches[:2],  # Use top 2 matches
        max_examples=2
    )
    
    print("\n🤖 Generated RAG Prompt (first 500 chars):")
    print("-" * 50)
    print(rag_prompt[:500] + "..." if len(rag_prompt) > 500 else rag_prompt)
    print("-" * 50)
    
    # Key elements validation
    key_elements = [
        "historical routing outcomes",
        "ACTUAL Department:",
        "Resolution Time:", 
        "Customer Satisfaction:",
        "Previous AI Prediction:"
    ]
    
    print("\n✅ RAG Prompt Quality Check:")
    for element in key_elements:
        found = element in rag_prompt
        status = "✅" if found else "❌"
        print(f"   {status} Contains '{element}': {found}")
    
    return rag_prompt


async def demonstrate_complete_rag_system():
    """Demonstrate the complete RAG intelligent routing system"""
    
    print_section("Complete RAG Intelligent Routing System")
    
    rag_system = RAGIntelligentRouting()
    
    # Test scenarios with different complexity levels
    test_scenarios = [
        {
            "ticket": "My enterprise internet service is experiencing intermittent connectivity issues affecting our video conferences",
            "category": "High-Impact Enterprise Issue",
            "description": "Complex technical issue requiring L2 support"
        },
        {
            "ticket": "I need to dispute a billing charge that appeared on my account without authorization", 
            "category": "Billing Dispute",
            "description": "Clear billing issue requiring corrections team"
        },
        {
            "ticket": "Unable to access my account dashboard, getting authentication errors repeatedly",
            "category": "Account Security Issue", 
            "description": "Security-related access problem"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🎯 Scenario {i}: {scenario['category']}")
        print(f"📝 Ticket: '{scenario['ticket']}'")
        print(f"💡 Context: {scenario['description']}")
        
        # Get complete intelligent routing decision
        result = await rag_system.route_ticket_intelligently(scenario['ticket'])
        
        print("\n📊 INTELLIGENT ROUTING DECISION:")
        print(f"   🎯 Department: {result['recommended_department']}")
        print(f"   📈 Confidence: {result['confidence_level']}")
        print(f"   🔄 Method: {result['routing_method']}")
        print(f"   💭 Reasoning: {result['reasoning']}")
        
        print("\n📋 EVIDENCE & SUPPORTING DATA:")
        print(f"   🔍 Historical Matches Found: {result['historical_matches_found']}")
        print(f"   📏 Top Similarity Score: {result['top_similarity_score']:.3f}")
        print(f"   ✅ Historical Success Rate: {result['historical_success_rate']:.1%}")
        print(f"   ⏱️ Avg Resolution Time: {result['avg_resolution_time']:.1f} hours")
        print(f"   😊 Avg Customer Satisfaction: {result['avg_customer_satisfaction']:.1f}/10")
        
        # Show most relevant historical tickets
        if result['similar_tickets']:
            print("\n📚 Most Relevant Historical Cases:")
            for j, ticket in enumerate(result['similar_tickets'][:3], 1):
                dept = ticket['actual_department'] or 'Unknown'
                sim = ticket['similarity']
                res_time = ticket['resolution_time'] or 0
                satisfaction = ticket['satisfaction'] or 0
                
                print(f"   {j}. {ticket['ticket_id']}: {dept}")
                print(f"      Similarity: {sim:.3f} | Resolution: {res_time:.1f}h | Satisfaction: {satisfaction:.1f}/10")


def demonstrate_architecture_benefits():
    """Explain the architectural benefits of the RAG approach"""
    
    print_section("RAG Architecture Benefits Over Traditional Approaches")
    
    print("🎯 TRADITIONAL CLASSIFICATION LIMITATIONS:")
    print("   ❌ Zero-shot prompts lack historical context")
    print("   ❌ No access to actual routing success patterns")  
    print("   ❌ Cannot leverage resolution outcomes for learning")
    print("   ❌ Limited confidence in routing decisions")
    print("   ❌ No evidence-based reasoning for routes")
    
    print("\n🚀 RAG-ENHANCED ADVANTAGES:")
    print("   ✅ Few-shot prompts with actual routing outcomes")
    print("   ✅ Historical success patterns guide decisions")
    print("   ✅ Resolution times and satisfaction scores as context")
    print("   ✅ Confidence-based routing (cached vs LLM)")
    print("   ✅ Evidence-backed reasoning with similar cases")
    print("   ✅ Escalation patterns from successful resolutions")
    print("   ✅ AI prediction accuracy tracking for improvement")
    
    print("\n💡 PRODUCTION BENEFITS:")
    print("   🎯 Higher routing accuracy through historical learning")
    print("   ⚡ Faster responses via cached high-confidence routes")
    print("   📊 Comprehensive metrics for continuous improvement")
    print("   🔍 Transparent decision-making with evidence")
    print("   🛡️ Graceful fallback handling for API limitations")
    print("   📈 Self-improving system as more data accumulates")


def demonstrate_production_readiness():
    """Showcase production-ready features"""
    
    print_section("Production-Ready Features")
    
    print("🔧 RELIABILITY & ROBUSTNESS:")
    print("   ✅ Graceful OpenAI API failure handling")
    print("   ✅ Mock fallback responses for testing")
    print("   ✅ Comprehensive error logging and monitoring")
    print("   ✅ Configurable confidence thresholds") 
    print("   ✅ Vector database connection management")
    
    print("\n📊 MONITORING & OBSERVABILITY:")
    print("   ✅ Detailed routing decision logging")
    print("   ✅ Historical accuracy tracking")
    print("   ✅ Performance metrics collection")
    print("   ✅ Evidence trail for audit purposes")
    print("   ✅ Similarity score distribution analysis")
    
    print("\n⚡ PERFORMANCE OPTIMIZATION:")
    print("   ✅ Cached routing for high-confidence matches")
    print("   ✅ Configurable similarity search parameters")
    print("   ✅ Batch processing capabilities")
    print("   ✅ Efficient vector database queries")
    print("   ✅ Minimal API calls through smart caching")


async def run_complete_demonstration():
    """Run the complete Epic 1.11 RAG demonstration"""
    
    print_banner("🚀 EPIC 1.11: RAG-BASED LLM PROMPTING", "=", 70)
    print("Enhanced Intelligent Routing with Historical Intelligence")
    print_banner("COMPLETE SYSTEM DEMONSTRATION", "=", 70)
    
    try:
        # 1. Demonstrate similarity search
        historical_matches = await demonstrate_similarity_search()
        
        # 2. Demonstrate RAG prompt generation
        await demonstrate_rag_prompts(historical_matches)
        
        # 3. Demonstrate complete system
        await demonstrate_complete_rag_system()
        
        # 4. Explain architectural benefits
        demonstrate_architecture_benefits()
        
        # 5. Showcase production readiness
        demonstrate_production_readiness()
        
        print_banner("🎉 EPIC 1.11 DEMONSTRATION COMPLETE", "=", 70)
        print("🧠 RAG System Successfully Demonstrated!")
        print("🎯 Ready for Production Deployment!")
        
        print("\n💡 NEXT STEPS:")
        print("   1. Deploy to production with real OpenAI API quota")
        print("   2. Monitor routing accuracy and performance metrics")
        print("   3. Continuously improve with new historical data")
        print("   4. Expand to additional ticket categories and departments")
        print("   5. Implement advanced confidence learning algorithms")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Starting Epic 1.11 RAG System Demonstration...")
    success = asyncio.run(run_complete_demonstration())
    
    if success:
        print("\n✅ All demonstrations completed successfully!")
    else:
        print("\n❌ Some demonstrations failed. Check logs for details.")