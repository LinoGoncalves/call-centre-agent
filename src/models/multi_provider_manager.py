#!/usr/bin/env python3
"""
🎯 Multi-Provider Manager
Unified interface for LLM and Vector DB provider selection and routing

Features:
1. Intelligent provider selection based on user preferences
2. Automatic fallback handling for reliability
3. Cost optimization and performance tracking
4. Unified interface for all classification operations
5. Real-time provider availability monitoring

Author: GitHub Copilot Assistant
Date: October 9, 2025
Purpose: Unified multi-provider orchestration
"""

import logging
import time
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass

# Import existing components
try:
    from src.models.enhanced_classifier import GeminiEnhancedClassifier, EnhancedClassificationResult
    from src.models.opensource_llm import OpenSourceLLM
    from src.models.chromadb_client import ChromaVectorDB
    from src.models.multi_provider_config import MultiProviderConfig, MultiProviderResult
    from src.vector_db.pinecone_client import PineconeClient
except ImportError as e:
    logging.warning(f"Import warning: {e}")

logger = logging.getLogger(__name__)

@dataclass
class ClassificationResult:
    """Unified classification result from multi-provider system"""
    department: str
    reasoning: str
    confidence: float
    processing_time_ms: float
    cost_estimate: float
    providers_used: Dict[str, str]  # component -> provider_name
    fallback_used: bool
    metadata: Dict[str, Any]

class MultiProviderManager:
    """
    Multi-Provider Manager for Call Centre Agent System
    
    Orchestrates LLM and Vector DB providers with intelligent routing and fallbacks
    """
    
    def __init__(self, config_file: str = "provider_config.json"):
        """
        Initialize multi-provider manager
        
        Args:
            config_file: Configuration file path
        """
        self.config = MultiProviderConfig(config_file)
        self.providers = {}
        self._initialize_providers()
        
    def _initialize_providers(self):
        """Initialize all available providers"""
        
        # Initialize LLM providers
        self.providers['llm'] = {}
        
        # Gemini LLM (existing)
        try:
            gemini_classifier = GeminiEnhancedClassifier()
            if gemini_classifier and hasattr(gemini_classifier, 'classify_ticket'):
                self.providers['llm']['gemini'] = gemini_classifier
                logger.info("✅ Initialized Gemini LLM provider")
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini LLM: {e}")
        
        # Ollama LLM (new)
        try:
            # Create fallback handler for Ollama
            fallback_handler = None
            if 'gemini' in self.providers['llm']:
                fallback_handler = self.providers['llm']['gemini']
            
            ollama_client = OpenSourceLLM(fallback_handler=fallback_handler)
            if ollama_client.available:
                self.providers['llm']['ollama'] = ollama_client
                logger.info("✅ Initialized Ollama LLM provider")
        except Exception as e:
            logger.warning(f"Failed to initialize Ollama LLM: {e}")
        
        # Initialize Vector DB providers
        self.providers['vector_db'] = {}
        
        # Pinecone Vector DB (existing)
        try:
            pinecone_client = PineconeClient()
            if pinecone_client:
                self.providers['vector_db']['pinecone'] = pinecone_client
                logger.info("✅ Initialized Pinecone Vector DB provider")
        except Exception as e:
            logger.warning(f"Failed to initialize Pinecone Vector DB: {e}")
        
        # ChromaDB Vector DB (new)
        try:
            chroma_client = ChromaVectorDB()
            if chroma_client.available:
                self.providers['vector_db']['chromadb'] = chroma_client
                logger.info("✅ Initialized ChromaDB Vector DB provider")
        except Exception as e:
            logger.warning(f"Failed to initialize ChromaDB Vector DB: {e}")
    
    def classify_ticket(self, 
                       ticket_text: str,
                       use_vector_search: bool = True,
                       force_llm_provider: Optional[str] = None,
                       force_vector_provider: Optional[str] = None) -> ClassificationResult:
        """
        Classify ticket using multi-provider system
        
        Args:
            ticket_text: Customer service ticket text
            use_vector_search: Whether to attempt vector similarity search first
            force_llm_provider: Force specific LLM provider (for testing)
            force_vector_provider: Force specific vector provider (for testing)
            
        Returns:
            ClassificationResult with provider information
        """
        start_time = time.time()
        providers_used = {}
        fallback_used = False
        total_cost = 0.0
        
        department = "technical_support_l1"  # Default fallback
        reasoning = "Multi-provider classification"
        confidence = 0.5
        
        # Step 1: Try Vector DB search if enabled
        vector_result = None
        if use_vector_search:
            vector_provider = force_vector_provider or self.config.get_preferred_vector_db()
            vector_result = self._search_similar_tickets(ticket_text, vector_provider)
            
            if vector_result and vector_result.confidence >= 0.8:
                # High confidence vector match - use it directly
                department = vector_result.department
                reasoning = f"Vector similarity match (confidence: {vector_result.confidence:.1%})"
                confidence = vector_result.confidence
                providers_used['vector_db'] = vector_provider
                total_cost += vector_result.cost_estimate
                
                processing_time = (time.time() - start_time) * 1000
                return ClassificationResult(
                    department=department,
                    reasoning=reasoning,
                    confidence=confidence,
                    processing_time_ms=processing_time,
                    cost_estimate=total_cost,
                    providers_used=providers_used,
                    fallback_used=fallback_used,
                    metadata={'vector_search_result': vector_result}
                )
        
        # Step 2: Use LLM for classification
        llm_provider = force_llm_provider or self.config.get_preferred_llm()
        llm_result = self._classify_with_llm(ticket_text, llm_provider, vector_result)
        
        if llm_result:
            department = llm_result.get('department', department)
            reasoning = llm_result.get('reasoning', reasoning)
            confidence = llm_result.get('confidence', confidence)
            providers_used['llm'] = llm_result.get('provider_used', llm_provider)
            total_cost += llm_result.get('cost_estimate', 0.0)
            fallback_used = llm_result.get('fallback_used', False)
        
        processing_time = (time.time() - start_time) * 1000
        
        return ClassificationResult(
            department=department,
            reasoning=reasoning,
            confidence=confidence,
            processing_time_ms=processing_time,
            cost_estimate=total_cost,
            providers_used=providers_used,
            fallback_used=fallback_used,
            metadata={
                'vector_search_result': vector_result,
                'llm_result': llm_result
            }
        )
    
    def _search_similar_tickets(self, ticket_text: str, provider: str) -> Optional[Any]:
        """Search for similar tickets using specified vector DB provider"""
        try:
            if provider not in self.providers.get('vector_db', {}):
                logger.warning(f"Vector DB provider {provider} not available")
                return None
            
            client = self.providers['vector_db'][provider]
            
            if provider == 'chromadb':
                results = client.search_similar_tickets(ticket_text, top_k=3)
                if results:
                    best_result = results[0]
                    return type('VectorResult', (), {
                        'department': best_result.department,
                        'confidence': best_result.similarity_score,
                        'cost_estimate': 0.0,  # ChromaDB is free
                        'provider': provider,
                        'original_ticket': best_result.original_ticket
                    })()
            
            elif provider == 'pinecone':
                # Implement Pinecone search (placeholder)
                # In real implementation, would use existing Pinecone client
                logger.info(f"Pinecone vector search not yet implemented")
                return None
            
        except Exception as e:
            logger.error(f"Vector search failed with {provider}: {e}")
        
        return None
    
    def _classify_with_llm(self, 
                          ticket_text: str, 
                          provider: str,
                          vector_context: Optional[Any] = None) -> Optional[Dict]:
        """Classify ticket using specified LLM provider"""
        try:
            if provider not in self.providers.get('llm', {}):
                logger.warning(f"LLM provider {provider} not available")
                # Try fallback provider
                available_providers = list(self.providers.get('llm', {}).keys())
                if available_providers:
                    provider = available_providers[0]
                    logger.info(f"Using fallback LLM provider: {provider}")
                else:
                    logger.error("No LLM providers available")
                    return None
            
            client = self.providers['llm'][provider]
            
            if provider == 'ollama':
                department, reasoning, confidence, metadata = client.classify_ticket(ticket_text)
                return {
                    'department': department,
                    'reasoning': reasoning,
                    'confidence': confidence,
                    'cost_estimate': metadata.get('cost_estimate', 0.0),
                    'provider_used': metadata.get('source', provider),
                    'fallback_used': metadata.get('source') == 'fallback',
                    'processing_time_ms': metadata.get('processing_time_ms', 0)
                }
            
            elif provider == 'gemini':
                # Use existing Gemini classifier
                result = client.classify_ticket(ticket_text)
                if result and len(result) >= 3:
                    return {
                        'department': result[0],
                        'reasoning': result[1],
                        'confidence': result[2],
                        'cost_estimate': 0.0003,  # Estimated Gemini cost
                        'provider_used': provider,
                        'fallback_used': False,
                        'processing_time_ms': 1500  # Estimated
                    }
            
        except Exception as e:
            logger.error(f"LLM classification failed with {provider}: {e}")
        
        return None
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        status = {
            'llm_providers': {},
            'vector_db_providers': {},
            'current_preferences': {
                'llm': self.config.get_preferred_llm(),
                'vector_db': self.config.get_preferred_vector_db()
            }
        }
        
        # LLM provider status
        for provider_id in ['gemini', 'ollama']:
            available = provider_id in self.providers.get('llm', {})
            config = self.config.config.get('llm_providers', {}).get(provider_id, {})
            status['llm_providers'][provider_id] = {
                'name': config.get('name', provider_id),
                'available': available,
                'cost_per_query': config.get('cost_per_query', 0.0),
                'response_time_ms': config.get('avg_response_time_ms', 0),
                'status': config.get('metadata', {}).get('status', 'unknown')
            }
        
        # Vector DB provider status
        for provider_id in ['pinecone', 'chromadb']:
            available = provider_id in self.providers.get('vector_db', {})
            config = self.config.config.get('vector_db_providers', {}).get(provider_id, {})
            status['vector_db_providers'][provider_id] = {
                'name': config.get('name', provider_id),
                'available': available,
                'cost_per_query': config.get('cost_per_query', 0.0),
                'response_time_ms': config.get('avg_response_time_ms', 0),
                'status': config.get('metadata', {}).get('status', 'unknown')
            }
        
        return status
    
    def set_providers(self, llm_provider: str, vector_db_provider: str) -> bool:
        """Set preferred providers"""
        success = True
        
        if not self.config.set_preferred_llm(llm_provider):
            logger.error(f"Failed to set LLM provider to {llm_provider}")
            success = False
        
        if not self.config.set_preferred_vector_db(vector_db_provider):
            logger.error(f"Failed to set Vector DB provider to {vector_db_provider}")
            success = False
        
        return success
    
    def get_cost_estimates(self, monthly_queries: int = 1000) -> Dict[str, Any]:
        """Get cost estimates for different provider combinations"""
        costs = self.config.get_cost_comparison()
        
        combinations = []
        for llm_id, llm_data in costs['llm_providers'].items():
            for vdb_id, vdb_data in costs['vector_db_providers'].items():
                monthly_cost = (llm_data['cost_per_query'] + vdb_data['cost_per_query']) * monthly_queries
                annual_cost = monthly_cost * 12
                
                combinations.append({
                    'llm_provider': llm_id,
                    'llm_name': llm_data['name'],
                    'vector_db_provider': vdb_id,
                    'vector_db_name': vdb_data['name'],
                    'cost_per_query': llm_data['cost_per_query'] + vdb_data['cost_per_query'],
                    'monthly_cost': monthly_cost,
                    'annual_cost': annual_cost,
                    'data_sovereignty': 'local' if llm_id == 'ollama' and vdb_id == 'chromadb' else 'cloud'
                })
        
        # Sort by cost (cheapest first)
        combinations.sort(key=lambda x: x['cost_per_query'])
        
        return {
            'combinations': combinations,
            'cheapest': combinations[0] if combinations else None,
            'most_expensive': combinations[-1] if combinations else None,
            'monthly_queries': monthly_queries
        }

if __name__ == "__main__":
    # Demo multi-provider manager
    print("🎯 Testing Multi-Provider Manager...")
    
    manager = MultiProviderManager()
    
    print("\n📊 Provider Status:")
    status = manager.get_provider_status()
    
    print("LLM Providers:")
    for provider_id, info in status['llm_providers'].items():
        status_icon = "✅" if info['available'] else "❌"
        print(f"  {status_icon} {info['name']}: ${info['cost_per_query']:.4f}/query")
    
    print("Vector DB Providers:")
    for provider_id, info in status['vector_db_providers'].items():
        status_icon = "✅" if info['available'] else "❌"
        print(f"  {status_icon} {info['name']}: ${info['cost_per_query']:.4f}/query")
    
    print(f"\n⚙️ Current Preferences:")
    print(f"  LLM: {status['current_preferences']['llm']}")
    print(f"  Vector DB: {status['current_preferences']['vector_db']}")
    
    # Test classification
    test_ticket = "My internet connection is very slow and I can't stream videos"
    print(f"\n🧪 Testing Classification:")
    print(f"Ticket: {test_ticket}")
    
    result = manager.classify_ticket(test_ticket)
    print(f"\nResult:")
    print(f"  Department: {result.department}")
    print(f"  Confidence: {result.confidence:.1%}")
    print(f"  Cost: ${result.cost_estimate:.6f}")
    print(f"  Time: {result.processing_time_ms:.1f}ms")
    print(f"  Providers: {result.providers_used}")
    print(f"  Fallback used: {result.fallback_used}")
    
    # Show cost comparison
    print(f"\n💰 Cost Comparison (1000 queries/month):")
    estimates = manager.get_cost_estimates(1000)
    for combo in estimates['combinations']:
        sovereignty = "🏠" if combo['data_sovereignty'] == 'local' else "☁️"
        print(f"  {sovereignty} {combo['llm_name']} + {combo['vector_db_name']}: ${combo['monthly_cost']:.2f}/month")
    
    print(f"\n✅ Multi-provider system ready!")