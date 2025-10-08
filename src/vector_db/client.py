"""
🗃️ Vector Database Client Infrastructure for Call Centre Agent
Pinecone-based vector storage with OpenAI embeddings integration

Features:
1. Pinecone serverless index management
2. Connection pooling and retry logic  
3. Health check endpoints
4. Batch operations for embeddings
5. Metadata filtering and similarity search

Author: Master Agent Orchestrator
Date: October 7, 2025
Purpose: Epic 1.1-1.5 - Vector DB Infrastructure Setup
"""

import os
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

import pinecone
from pinecone import Pinecone, ServerlessSpec
import openai
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VectorSearchResult:
    """Result from vector similarity search."""
    ticket_id: str
    similarity_score: float
    metadata: Dict[str, Any]
    ticket_text: str
    department: str
    urgency: str
    sentiment: str
    historical_accuracy: float = 0.0

@dataclass
class VectorEmbedding:
    """Embedding with metadata for storage."""
    ticket_id: str
    embedding: List[float]
    metadata: Dict[str, Any]
    text: str

class VectorDatabaseClient:
    """
    Production-grade Pinecone vector database client with retry logic.
    
    Handles:
    - Connection management with exponential backoff
    - Batch upsert operations (1000 vectors per batch)
    - Health checks and monitoring
    - Metadata filtering for similarity search
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        environment: str = "us-west1-gcp",  # Pinecone serverless region
        index_name: str = "telco-tickets",
        dimension: int = 1536,  # OpenAI text-embedding-3-small dimension
        metric: str = "cosine",
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """Initialize Pinecone client with configuration."""
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.environment = environment
        self.index_name = index_name
        self.dimension = dimension
        self.metric = metric
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY environment variable is required")
        
        # Initialize Pinecone client
        self.pc = Pinecone(api_key=self.api_key)
        self.index = None
        
        # Initialize OpenAI client for embeddings
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Performance tracking
        self.stats = {
            "queries": 0,
            "upserts": 0,
            "errors": 0,
            "total_latency_ms": 0
        }
    
    def _exponential_backoff_retry(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry logic."""
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                latency_ms = (time.time() - start_time) * 1000
                self.stats["total_latency_ms"] += latency_ms
                return result
            
            except Exception as e:
                self.stats["errors"] += 1
                if attempt == self.max_retries - 1:
                    logger.error(f"Max retries exceeded. Last error: {e}")
                    raise
                
                delay = self.retry_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
    
    def initialize_index(self) -> bool:
        """
        Initialize or connect to Pinecone serverless index.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if index exists
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                logger.info(f"Creating new Pinecone index: {self.index_name}")
                
                # Create serverless index
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric=self.metric,
                    spec=ServerlessSpec(
                        cloud='gcp',
                        region=self.environment
                    ),
                    deletion_protection="disabled"  # Enable for production
                )
                
                # Wait for index to be ready
                logger.info("Waiting for index to be ready...")
                time.sleep(10)
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            
            logger.info(f"✅ Connected to Pinecone index: {self.index_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize index: {e}")
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on vector database.
        
        Returns:
            Dict with health status, latency, and stats
        """
        try:
            start_time = time.time()
            
            if not self.index:
                return {
                    "status": "unhealthy",
                    "error": "Index not initialized",
                    "latency_ms": 0
                }
            
            # Perform test query
            stats = self.index.describe_index_stats()
            latency_ms = (time.time() - start_time) * 1000
            
            return {
                "status": "healthy",
                "latency_ms": round(latency_ms, 2),
                "vector_count": stats.total_vector_count,
                "dimensions": self.dimension,
                "performance_stats": self.stats,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "latency_ms": 0,
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate OpenAI embedding for text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding
        """
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required for embeddings")
        
        try:
            response = openai.embeddings.create(
                input=text,
                model="text-embedding-3-small"  # 1536 dimensions, $0.00002/1K tokens
            )
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise
    
    def upsert_embeddings(self, embeddings: List[VectorEmbedding]) -> bool:
        """
        Batch upsert embeddings to Pinecone (1000 per batch).
        
        Args:
            embeddings: List of VectorEmbedding objects
            
        Returns:
            bool: True if successful
        """
        if not self.index:
            logger.error("Index not initialized")
            return False
        
        try:
            batch_size = 1000
            total_batches = len(embeddings) // batch_size + (1 if len(embeddings) % batch_size else 0)
            
            for i in range(0, len(embeddings), batch_size):
                batch = embeddings[i:i + batch_size]
                
                # Format for Pinecone upsert
                vectors = [
                    {
                        "id": emb.ticket_id,
                        "values": emb.embedding,
                        "metadata": {
                            **emb.metadata,
                            "text": emb.text[:1000],  # Limit metadata text size
                            "upserted_at": datetime.now().isoformat()
                        }
                    }
                    for emb in batch
                ]
                
                # Upsert with retry logic
                self._exponential_backoff_retry(
                    self.index.upsert,
                    vectors=vectors
                )
                
                batch_num = i // batch_size + 1
                logger.info(f"✅ Upserted batch {batch_num}/{total_batches} ({len(batch)} vectors)")
                
                self.stats["upserts"] += len(batch)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to upsert embeddings: {e}")
            return False
    
    def similarity_search(
        self, 
        query_text: str, 
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
        similarity_threshold: float = 0.0
    ) -> List[VectorSearchResult]:
        """
        Perform similarity search using cosine similarity.
        
        Args:
            query_text: Text to search for similar tickets
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of VectorSearchResult objects
        """
        if not self.index:
            logger.error("Index not initialized")
            return []
        
        try:
            # Generate embedding for query
            query_embedding = self.generate_embedding(query_text)
            
            # Perform search with retry logic
            search_results = self._exponential_backoff_retry(
                self.index.query,
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_metadata
            )
            
            # Convert to VectorSearchResult objects
            results = []
            for match in search_results.matches:
                if match.score >= similarity_threshold:
                    metadata = match.metadata or {}
                    
                    result = VectorSearchResult(
                        ticket_id=match.id,
                        similarity_score=round(match.score, 4),
                        metadata=metadata,
                        ticket_text=metadata.get("text", ""),
                        department=metadata.get("department", "UNKNOWN"),
                        urgency=metadata.get("urgency", "MEDIUM"),
                        sentiment=metadata.get("sentiment", "NEUTRAL"),
                        historical_accuracy=metadata.get("historical_accuracy", 0.0)
                    )
                    results.append(result)
            
            self.stats["queries"] += 1
            logger.info(f"✅ Found {len(results)} similar tickets (threshold: {similarity_threshold})")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Similarity search failed: {e}")
            return []
    
    def delete_vectors(self, ticket_ids: List[str]) -> bool:
        """
        Delete vectors by ticket IDs.
        
        Args:
            ticket_ids: List of ticket IDs to delete
            
        Returns:
            bool: True if successful
        """
        if not self.index:
            logger.error("Index not initialized")
            return False
        
        try:
            self._exponential_backoff_retry(
                self.index.delete,
                ids=ticket_ids
            )
            
            logger.info(f"✅ Deleted {len(ticket_ids)} vectors")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete vectors: {e}")
            return False
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        avg_latency = (
            self.stats["total_latency_ms"] / self.stats["queries"] 
            if self.stats["queries"] > 0 else 0
        )
        
        return {
            **self.stats,
            "average_latency_ms": round(avg_latency, 2),
            "error_rate": round(
                self.stats["errors"] / max(self.stats["queries"] + self.stats["upserts"], 1) * 100, 2
            )
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize client (requires PINECONE_API_KEY and OPENAI_API_KEY in .env)
    client = VectorDatabaseClient()
    
    # Initialize index
    if client.initialize_index():
        print("✅ Vector database initialized successfully")
        
        # Health check
        health = client.health_check()
        print(f"Health status: {health}")
        
        # Example embedding and search
        sample_ticket = "My account was charged twice for the same service"
        
        try:
            # Generate embedding
            embedding = client.generate_embedding(sample_ticket)
            print(f"✅ Generated embedding with {len(embedding)} dimensions")
            
            # Example search (will be empty until we have data)
            results = client.similarity_search(sample_ticket, top_k=3)
            print(f"Found {len(results)} similar tickets")
            
        except Exception as e:
            print(f"⚠️  Embeddings require OPENAI_API_KEY: {e}")
    
    else:
        print("❌ Failed to initialize vector database")