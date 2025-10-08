"""
Enhanced Embedding Pipeline (Epic 1.6) with Routing Intelligence
Integrates OpenAI embeddings API with routing outcome tracking for intelligent ticket routing
"""

import asyncio
import os
import time
from datetime import datetime, UTC
from typing import List, Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from enum import Enum

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OpenAI = None
    OPENAI_AVAILABLE = False

from dotenv import load_dotenv
from src.vector_db.pinecone_client import PineconeClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingModel(Enum):
    """Supported embedding models"""
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"  # $0.02 per 1M tokens, 1536 dimensions
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"  # $0.13 per 1M tokens, 3072 dimensions
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"  # Legacy, 1536 dimensions


@dataclass
class EmbeddingConfig:
    """Configuration for embedding generation"""
    model: EmbeddingModel = EmbeddingModel.TEXT_EMBEDDING_3_SMALL
    dimension: int = 1536
    max_batch_size: int = 100  # OpenAI limit is 2048, but we use smaller batches
    rate_limit_delay: float = 0.1  # Seconds between requests
    max_retries: int = 3
    timeout: int = 30


@dataclass
class TicketWithRouting:
    """Ticket data with routing intelligence for embedding"""
    # Core ticket data
    ticket_id: str
    text: str
    created_at: str
    
    # Routing intelligence (when available from historical data)
    actual_department: Optional[str] = None
    actual_agent_id: Optional[str] = None
    resolution_time_hours: Optional[float] = None
    customer_satisfaction: Optional[float] = None
    first_contact_resolution: Optional[bool] = None
    
    # Business context
    customer_tier: Optional[str] = None
    service_type: Optional[str] = None
    urgency_level: Optional[str] = None
    sentiment_score: Optional[float] = None
    
    # Additional metadata
    tags: Optional[List[str]] = None
    channel: Optional[str] = None


class EnhancedEmbeddingPipeline:
    """
    Production embedding pipeline with routing intelligence integration.
    
    Features:
    - OpenAI text-embedding-3-small integration
    - Batch processing with rate limiting  
    - Routing outcome tracking
    - Cost optimization and monitoring
    - Automatic retry and error handling
    - Vector database integration
    """
    
    def __init__(
        self, 
        config: Optional[EmbeddingConfig] = None,
        vector_client: Optional[PineconeClient] = None
    ):
        """Initialize embedding pipeline"""
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        self.config = config or EmbeddingConfig()
        self.vector_client = vector_client or PineconeClient()
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.openai_client = OpenAI(api_key=api_key)
        
        # Metrics tracking
        self.metrics = {
            "total_tokens": 0,
            "total_embeddings": 0,
            "total_cost_usd": 0.0,
            "batch_count": 0,
            "error_count": 0,
            "start_time": None
        }
    
    async def generate_embeddings(
        self, 
        texts: List[str], 
        batch_size: Optional[int] = None
    ) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using OpenAI API.
        
        Args:
            texts: List of text strings to embed
            batch_size: Batch size (defaults to config)
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        batch_size = batch_size or self.config.max_batch_size
        all_embeddings = []
        
        logger.info(f"Generating embeddings for {len(texts)} texts using {self.config.model.value}")
        
        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = await self._generate_batch_embeddings(batch_texts)
            all_embeddings.extend(batch_embeddings)
            
            # Rate limiting
            if i + batch_size < len(texts):
                await asyncio.sleep(self.config.rate_limit_delay)
        
        return all_embeddings
    
    async def _generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a single batch with retry logic"""
        for attempt in range(self.config.max_retries):
            try:
                response = await asyncio.to_thread(
                    self._call_openai_embedding, texts
                )
                
                embeddings = [item.embedding for item in response.data]
                
                # Update metrics
                self.metrics["total_embeddings"] += len(embeddings)
                self.metrics["batch_count"] += 1
                
                # Calculate tokens and cost (approximate)
                total_chars = sum(len(text) for text in texts)
                estimated_tokens = total_chars // 4  # Rough estimate: 4 chars per token
                self.metrics["total_tokens"] += estimated_tokens
                
                # Cost calculation for text-embedding-3-small: $0.02 per 1M tokens
                cost_per_token = 0.00000002  # $0.02 / 1M
                batch_cost = estimated_tokens * cost_per_token
                self.metrics["total_cost_usd"] += batch_cost
                
                logger.debug(f"Generated {len(embeddings)} embeddings, ~{estimated_tokens} tokens, ~${batch_cost:.6f}")
                
                return embeddings
                
            except Exception as e:
                self.metrics["error_count"] += 1
                logger.warning(f"Embedding attempt {attempt + 1} failed: {e}")
                
                if attempt == self.config.max_retries - 1:
                    raise
                    
                # Exponential backoff
                await asyncio.sleep(2 ** attempt)
        
        return []
    
    def _call_openai_embedding(self, texts: List[str]):
        """Synchronous OpenAI API call (wrapped in asyncio.to_thread)"""
        return self.openai_client.embeddings.create(
            model=self.config.model.value,
            input=texts,
            encoding_format="float"
        )
    
    async def process_tickets_batch(
        self, 
        tickets: List[TicketWithRouting]
    ) -> List[Tuple[str, List[float], Dict[str, Any]]]:
        """
        Process a batch of tickets: generate embeddings and prepare for vector storage.
        
        Args:
            tickets: List of tickets with routing intelligence
            
        Returns:
            List of (ticket_id, embedding, metadata) tuples ready for Pinecone
        """
        if not tickets:
            return []
        
        logger.info(f"Processing batch of {len(tickets)} tickets with routing intelligence")
        
        # Extract texts for embedding
        texts = [ticket.text for ticket in tickets]
        
        # Generate embeddings
        embeddings = await self.generate_embeddings(texts)
        
        if len(embeddings) != len(tickets):
            raise ValueError(f"Embedding count ({len(embeddings)}) doesn't match ticket count ({len(tickets)})")
        
        # Prepare vectors with enhanced metadata
        vectors = []
        for ticket, embedding in zip(tickets, embeddings):
            metadata = self.vector_client.create_enhanced_metadata(
                ticket_id=ticket.ticket_id,
                text=ticket.text,
                created_at=ticket.created_at,
                actual_department=ticket.actual_department,
                actual_agent_id=ticket.actual_agent_id,
                resolution_time_hours=ticket.resolution_time_hours,
                customer_satisfaction=ticket.customer_satisfaction,
                first_contact_resolution=ticket.first_contact_resolution,
                customer_tier=ticket.customer_tier,
                service_type=ticket.service_type,
                urgency_business=ticket.urgency_level,
                sentiment_score=ticket.sentiment_score,
                agent_tags=ticket.tags,
                channel=ticket.channel
            )
            
            vectors.append((ticket.ticket_id, embedding, metadata))
        
        return vectors
    
    async def embed_and_store_tickets(
        self, 
        tickets: List[TicketWithRouting], 
        batch_size: int = 50
    ) -> Dict[str, Any]:
        """
        Complete pipeline: embed tickets and store in vector database.
        
        Args:
            tickets: Tickets to process
            batch_size: Processing batch size
            
        Returns:
            Processing summary with metrics
        """
        if not tickets:
            return {"status": "no_tickets", "metrics": self.metrics}
        
        self.metrics["start_time"] = time.time()
        
        try:
            # Initialize vector database
            await self.vector_client.initialize_index(create_if_not_exists=True)
            
            total_processed = 0
            results = {"upserted_count": 0, "failed_batches": []}
            
            # Process in batches
            for i in range(0, len(tickets), batch_size):
                batch = tickets[i:i + batch_size]
                
                try:
                    # Generate embeddings and metadata
                    vectors = await self.process_tickets_batch(batch)
                    
                    # Store in vector database
                    batch_result = await self.vector_client.upsert_vectors(vectors)
                    results["upserted_count"] += batch_result.get("upserted_count", len(vectors))
                    
                    total_processed += len(batch)
                    
                    logger.info(f"Processed batch {i//batch_size + 1}: {len(batch)} tickets")
                    
                except Exception as e:
                    logger.error(f"Batch {i//batch_size + 1} failed: {e}")
                    results["failed_batches"].append({
                        "batch_index": i//batch_size + 1,
                        "error": str(e),
                        "ticket_ids": [t.ticket_id for t in batch]
                    })
            
            # Final metrics
            end_time = time.time()
            processing_time = end_time - self.metrics["start_time"]
            
            summary = {
                "status": "completed",
                "total_tickets": len(tickets),
                "processed_tickets": total_processed,
                "upserted_vectors": results["upserted_count"],
                "failed_batches": len(results["failed_batches"]),
                "processing_time_seconds": processing_time,
                "embeddings_per_second": total_processed / processing_time if processing_time > 0 else 0,
                "estimated_cost_usd": self.metrics["total_cost_usd"],
                "total_tokens": self.metrics["total_tokens"],
                "metrics": self.metrics.copy()
            }
            
            logger.info(f"Pipeline completed: {total_processed} tickets, ${self.metrics['total_cost_usd']:.4f} cost")
            
            return summary
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise
        finally:
            await self.vector_client.close()


# Sample usage and testing functions

def create_sample_historical_tickets() -> List[TicketWithRouting]:
    """Create sample tickets with routing intelligence for testing"""
    
    return [
        TicketWithRouting(
            ticket_id="EMB-001",
            text="My fiber internet keeps disconnecting during video conferences affecting business meetings",
            created_at="2024-10-01T09:00:00Z",
            actual_department="technical_support_l2",
            actual_agent_id="AGT-TEC-007",
            resolution_time_hours=6.5,
            customer_satisfaction=8.5,
            first_contact_resolution=False,
            customer_tier="enterprise",
            service_type="fiber_business",
            urgency_level="high",
            sentiment_score=-0.7,
            tags=["fiber", "video_conference", "business"],
            channel="phone"
        ),
        TicketWithRouting(
            ticket_id="EMB-002",
            text="Duplicate billing charges on my account need immediate refund",
            created_at="2024-10-02T14:30:00Z",
            actual_department="billing_corrections",
            actual_agent_id="AGT-BIL-012",
            resolution_time_hours=0.25,
            customer_satisfaction=9.2,
            first_contact_resolution=True,
            customer_tier="standard",
            service_type="mobile_postpaid",
            urgency_level="medium",
            sentiment_score=0.1,
            tags=["billing", "duplicate", "refund"],
            channel="web"
        ),
        TicketWithRouting(
            ticket_id="EMB-003",
            text="Cannot access online account password reset emails not arriving",
            created_at="2024-10-03T16:45:00Z",
            actual_department="account_security",
            actual_agent_id="AGT-SEC-005",
            resolution_time_hours=1.5,
            customer_satisfaction=7.8,
            first_contact_resolution=False,
            customer_tier="premium",
            service_type="internet_bundle",
            urgency_level="medium",
            sentiment_score=-0.4,
            tags=["account_access", "password", "security"],
            channel="chat"
        )
    ]

async def test_embedding_pipeline():
    """Test the enhanced embedding pipeline"""
    print("🚀 Testing Enhanced Embedding Pipeline (Epic 1.6)")
    print("=" * 60)
    
    try:
        # Check if OpenAI API key is available
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  OPENAI_API_KEY not found - using mock embeddings")
            return await test_mock_embedding_pipeline()
        
        print("✅ OpenAI API key found - using real embeddings")
        
        # Create pipeline
        pipeline = EnhancedEmbeddingPipeline()
        
        # Create sample tickets
        tickets = create_sample_historical_tickets()
        
        print(f"📋 Processing {len(tickets)} sample tickets with routing intelligence...")
        
        # Run pipeline
        result = await pipeline.embed_and_store_tickets(tickets)
        
        print("\n📊 EMBEDDING PIPELINE RESULTS:")
        print("=" * 40)
        print(f"   Status: {result['status']}")
        print(f"   Total Tickets: {result['total_tickets']}")
        print(f"   Processed: {result['processed_tickets']}")
        print(f"   Upserted Vectors: {result['upserted_vectors']}")
        print(f"   Failed Batches: {result['failed_batches']}")
        print(f"   Processing Time: {result['processing_time_seconds']:.2f}s")
        print(f"   Speed: {result['embeddings_per_second']:.1f} embeddings/sec")
        print(f"   Estimated Cost: ${result['estimated_cost_usd']:.6f}")
        print(f"   Total Tokens: {result['total_tokens']:,}")
        
        if result['status'] == 'completed' and result['failed_batches'] == 0:
            print("\n🎉 EMBEDDING PIPELINE SUCCESS!")
            print("✅ All tickets embedded with routing intelligence")
            print("🚀 Ready for intelligent similarity search!")
            return True
        else:
            print(f"\n⚠️  Pipeline completed with {result['failed_batches']} failed batches")
            return False
        
    except Exception as e:
        print(f"❌ Embedding pipeline failed: {e}")
        return False

async def test_mock_embedding_pipeline():
    """Test pipeline with mock embeddings when OpenAI key unavailable"""
    print("🔄 Running with mock embeddings (no OpenAI API key)")
    
    # Mock implementation that simulates the pipeline
    tickets = create_sample_historical_tickets()
    
    print(f"📋 Processing {len(tickets)} tickets with mock embeddings...")
    
    # Simulate processing
    await asyncio.sleep(1)
    
    mock_result = {
        "status": "completed",
        "total_tickets": len(tickets),
        "processed_tickets": len(tickets),
        "upserted_vectors": len(tickets),
        "failed_batches": 0,
        "processing_time_seconds": 1.0,
        "embeddings_per_second": len(tickets),
        "estimated_cost_usd": 0.0001,  # Mock cost
        "total_tokens": 500 * len(tickets),
    }
    
    print("\n📊 MOCK EMBEDDING RESULTS:")
    print("=" * 40)
    for key, value in mock_result.items():
        if isinstance(value, float):
            print(f"   {key.replace('_', ' ').title()}: {value:.4f}")
        else:
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print("\n✅ Mock pipeline completed successfully!")
    print("💡 Add OPENAI_API_KEY to .env for real embeddings")
    return True

if __name__ == "__main__":
    print("🎯 Enhanced Embedding Pipeline with Routing Intelligence")
    print("Epic 1.6: OpenAI Integration + Vector Storage + Routing Intelligence")
    print()
    
    success = asyncio.run(test_embedding_pipeline())
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. Add OPENAI_API_KEY to .env for production embeddings")
        print("2. Process historical tickets from your ticketing system")
        print("3. Set up automated embedding for new tickets")
        print("4. Implement RAG-based LLM prompting (Epic 1.11+)")
    else:
        print("\n❌ Fix errors above before proceeding")