"""
Pinecone Vector Database Client with Production Features

This module provides a robust Pinecone client wrapper with:
- Connection pooling and retry logic
- Exponential backoff for transient failures
- Health checks and monitoring
- Proper error handling and logging
- Metadata filtering capabilities
"""

import os
import time
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
from contextlib import asynccontextmanager

try:
    from pinecone import Pinecone, ServerlessSpec, PodSpec
    from pinecone import PineconeException as PineconeApiException
except ImportError:
    # Fallback for development without Pinecone installed
    Pinecone = None
    ServerlessSpec = None
    PodSpec = None
    PineconeApiException = Exception

import backoff
import numpy as np
from pydantic import BaseModel, Field


# Configure logging
logger = logging.getLogger(__name__)


class VectorDBHealth(Enum):
    """Vector database health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class VectorMetadata:
    """Enhanced metadata for vector storage with routing intelligence"""
    # 🆔 Core Identifiers
    ticket_id: str
    created_at: str
    text: str = ""
    
    # 🎯 ROUTING INTELLIGENCE (Ground Truth for ML Training)
    actual_department: Optional[str] = None          # Where it was ACTUALLY routed
    actual_agent_id: Optional[str] = None            # Which agent handled it  
    actual_team: Optional[str] = None                # Sub-team within department
    resolution_time_hours: Optional[float] = None    # How long to resolve
    customer_satisfaction: Optional[float] = None    # CSAT score (1-10)
    first_contact_resolution: Optional[bool] = None  # Resolved on first contact?
    escalation_path: Optional[List[str]] = None      # Route taken to resolution
    resolution_type: Optional[str] = None            # How it was resolved
    final_outcome: Optional[str] = None              # Final status
    
    # 🤖 AI PREDICTION TRACKING (Model Performance)
    initial_ai_prediction: Optional[str] = None      # What AI predicted
    ai_confidence_score: Optional[float] = None      # AI confidence (0-1)
    prediction_was_correct: Optional[bool] = None    # Was prediction accurate?
    ai_model_version: Optional[str] = None           # Model version used
    
    # 🏷️ BUSINESS CONTEXT
    customer_tier: Optional[str] = None              # Customer importance level
    service_type: Optional[str] = None               # Product/service context
    urgency_business: Optional[str] = None           # Business impact level
    urgency_customer: Optional[str] = None           # Customer perception
    sentiment_score: Optional[float] = None          # Sentiment analysis (-1 to 1)
    language: Optional[str] = "en"                   # Content language
    channel: Optional[str] = None                    # How ticket was submitted
    
    # 🔍 SEARCHABLE ANNOTATIONS
    agent_tags: Optional[List[str]] = None           # Manual agent tags
    security_flags: Optional[List[str]] = None       # Security concerns
    knowledge_base_articles: Optional[List[str]] = None  # Related KB articles
    
    # 📊 LEGACY COMPATIBILITY (Deprecated but maintained)
    department: Optional[str] = None                 # ⚠️ Use actual_department instead
    urgency: Optional[str] = None                    # ⚠️ Use urgency_business instead  
    sentiment: Optional[str] = None                  # ⚠️ Use sentiment_score instead
    resolved: bool = False                           # ⚠️ Use final_outcome instead
    confidence_score: Optional[float] = None         # ⚠️ Use ai_confidence_score instead


class PineconeConfig(BaseModel):
    """Pinecone configuration settings"""
    api_key: str = Field(..., description="Pinecone API key")
    environment: str = Field(default="us-west1-gcp", description="Pinecone environment")
    index_name: str = Field(default="call-centre-tickets", description="Index name")
    dimension: int = Field(default=1536, description="Vector dimension (OpenAI embeddings)")
    metric: str = Field(default="cosine", description="Distance metric")
    cloud: str = Field(default="gcp", description="Cloud provider")
    region: str = Field(default="us-west1", description="Cloud region")
    
    class Config:
        env_prefix = "PINECONE_"


class PineconeClient:
    """
    Production-ready Pinecone client with resilience features.
    
    Features:
    - Automatic retry with exponential backoff
    - Connection pooling and health monitoring
    - Structured metadata handling
    - Batch operations with rate limiting
    - Comprehensive error handling
    """
    
    def __init__(self, config: Optional[PineconeConfig] = None):
        """Initialize Pinecone client with configuration."""
        if Pinecone is None:
            raise ImportError("pinecone package not installed. Run: pip install pinecone")
            
        # Load configuration
        self.config = config or PineconeConfig(
            api_key=os.getenv("PINECONE_API_KEY", ""),
            environment=os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp"),
            index_name=os.getenv("PINECONE_INDEX_NAME", "call-centre-tickets")
        )
        
        if not self.config.api_key:
            raise ValueError("PINECONE_API_KEY environment variable is required")
        
        # Initialize client
        self.pc = Pinecone(api_key=self.config.api_key)
        self.index = None
        self._health_status = VectorDBHealth.UNKNOWN
        self._last_health_check = 0
        self._health_check_interval = 300  # 5 minutes
        
        logger.info(f"Initialized Pinecone client for index: {self.config.index_name}")
    
    async def initialize_index(self, create_if_not_exists: bool = True) -> None:
        """Initialize or create the Pinecone index."""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes().names()
            
            if self.config.index_name not in existing_indexes:
                if not create_if_not_exists:
                    raise ValueError(f"Index {self.config.index_name} does not exist")
                
                logger.info(f"Creating new index: {self.config.index_name}")
                
                # Create serverless index (recommended for variable workloads)
                self.pc.create_index(
                    name=self.config.index_name,
                    dimension=self.config.dimension,
                    metric=self.config.metric,
                    spec=ServerlessSpec(
                        cloud=self.config.cloud,
                        region=self.config.region
                    )
                )
                
                # Wait for index to be ready
                await self._wait_for_index_ready()
            
            # Connect to index
            self.index = self.pc.Index(self.config.index_name)
            logger.info(f"Connected to index: {self.config.index_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize index: {e}")
            self._health_status = VectorDBHealth.UNHEALTHY
            raise
    
    async def _wait_for_index_ready(self, timeout: int = 300) -> None:
        """Wait for index to be ready with timeout."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                index_description = self.pc.describe_index(self.config.index_name)
                if index_description.status['ready']:
                    logger.info(f"Index {self.config.index_name} is ready")
                    return
                    
                logger.info("Waiting for index to be ready...")
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.warning(f"Error checking index status: {e}")
                await asyncio.sleep(10)
        
        raise TimeoutError(f"Index {self.config.index_name} not ready after {timeout} seconds")
    
    @staticmethod
    def create_enhanced_metadata(
        ticket_id: str,
        text: str,
        created_at: str,
        actual_department: Optional[str] = None,
        actual_agent_id: Optional[str] = None,
        resolution_time_hours: Optional[float] = None,
        customer_satisfaction: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create enhanced metadata dictionary with routing intelligence.
        
        Args:
            ticket_id: Unique ticket identifier
            text: Ticket content (truncated for metadata)
            created_at: ISO timestamp
            actual_department: Where ticket was actually routed
            actual_agent_id: Agent who handled the ticket
            resolution_time_hours: Time to resolve (hours)
            customer_satisfaction: CSAT score (1-10)
            **kwargs: Additional metadata fields
            
        Returns:
            Structured metadata dictionary
        """
        metadata = {
            # Core fields
            "ticket_id": ticket_id,
            "text": text[:500] if text else "",  # Truncate for Pinecone limits
            "created_at": created_at,
            
            # Routing intelligence
            "actual_department": actual_department,
            "actual_agent_id": actual_agent_id,
            "resolution_time_hours": resolution_time_hours,
            "customer_satisfaction": customer_satisfaction,
        }
        
        # Add optional fields from kwargs
        optional_fields = [
            "actual_team", "first_contact_resolution", "escalation_path", 
            "resolution_type", "final_outcome", "initial_ai_prediction",
            "ai_confidence_score", "prediction_was_correct", "ai_model_version",
            "customer_tier", "service_type", "urgency_business", "urgency_customer",
            "sentiment_score", "language", "channel", "agent_tags", 
            "security_flags", "knowledge_base_articles"
        ]
        
        for field in optional_fields:
            if field in kwargs and kwargs[field] is not None:
                metadata[field] = kwargs[field]
        
        # Remove None values to keep metadata clean
        return {k: v for k, v in metadata.items() if v is not None}
    
    @staticmethod
    def create_legacy_metadata(
        ticket_id: str,
        department: str,
        urgency: str,
        sentiment: str,
        created_at: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create legacy metadata for backward compatibility.
        ⚠️ DEPRECATED: Use create_enhanced_metadata for new implementations.
        """
        return {
            "ticket_id": ticket_id,
            "department": department,
            "urgency": urgency,
            "sentiment": sentiment,
            "created_at": created_at,
            "resolved": kwargs.get("resolved", False),
            "confidence_score": kwargs.get("confidence_score"),
            "text": kwargs.get("text", "")[:500]
        }
    
    async def upsert_enhanced_vectors(
        self,
        vectors_with_metadata: List[Tuple[str, List[float], VectorMetadata]],
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Upsert vectors with enhanced VectorMetadata objects.
        
        Args:
            vectors_with_metadata: List of (id, vector, VectorMetadata) tuples
            batch_size: Batch size for processing
            
        Returns:
            Upsert response summary
        """
        # Convert VectorMetadata to dict format
        formatted_vectors = []
        for vec_id, vector, metadata in vectors_with_metadata:
            if isinstance(metadata, VectorMetadata):
                # Convert dataclass to dict, filtering None values
                metadata_dict = {
                    k: v for k, v in metadata.__dict__.items() 
                    if v is not None and not k.startswith('_')
                }
            else:
                metadata_dict = metadata
                
            formatted_vectors.append((vec_id, vector, metadata_dict))
        
        return await self.upsert_vectors(formatted_vectors, batch_size)
    
    @backoff.on_exception(
        backoff.expo,
        (PineconeApiException, ConnectionError, TimeoutError),
        max_tries=3,
        factor=2,
        jitter=backoff.random_jitter
    )
    async def upsert_vectors(
        self, 
        vectors: List[Tuple[str, List[float], Dict[str, Any]]], 
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Upsert vectors in batches with retry logic.
        
        Args:
            vectors: List of (id, vector, metadata) tuples
            batch_size: Number of vectors per batch
            
        Returns:
            Upsert response summary
        """
        if not self.index:
            await self.initialize_index()
        
        total_vectors = len(vectors)
        results = {"upserted_count": 0, "failed_batches": []}
        
        # Process in batches to avoid rate limits
        for i in range(0, total_vectors, batch_size):
            batch = vectors[i:i + batch_size]
            
            try:
                # Format for Pinecone API
                formatted_batch = [
                    {
                        "id": vec_id,
                        "values": values,
                        "metadata": metadata
                    }
                    for vec_id, values, metadata in batch
                ]
                
                response = self.index.upsert(vectors=formatted_batch)
                results["upserted_count"] += response.get("upserted_count", len(batch))
                
                logger.debug(f"Upserted batch {i//batch_size + 1}/{(total_vectors-1)//batch_size + 1}")
                
                # Rate limiting - respect Pinecone limits
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Failed to upsert batch {i//batch_size + 1}: {e}")
                results["failed_batches"].append({"batch_start": i, "batch_size": len(batch), "error": str(e)})
        
        logger.info(f"Upserted {results['upserted_count']}/{total_vectors} vectors")
        return results
    
    @backoff.on_exception(
        backoff.expo,
        (PineconeApiException, ConnectionError, TimeoutError),
        max_tries=3,
        factor=2
    )
    async def query_vectors(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
        include_values: bool = False,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Query for similar vectors with metadata filtering.
        
        Args:
            query_vector: Query vector embeddings
            top_k: Number of similar vectors to return
            filter_metadata: Metadata filters (e.g., {"department": "billing"})
            include_values: Whether to include vector values in response
            include_metadata: Whether to include metadata in response
            
        Returns:
            Query results with matches
        """
        if not self.index:
            await self.initialize_index()
        
        try:
            response = self.index.query(
                vector=query_vector,
                top_k=top_k,
                filter=filter_metadata,
                include_values=include_values,
                include_metadata=include_metadata
            )
            
            logger.debug(f"Found {len(response.matches)} matches for query")
            return response
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise
    
    @backoff.on_exception(
        backoff.expo,
        (PineconeApiException, ConnectionError),
        max_tries=3,
        factor=2
    )
    async def delete_vectors(self, ids: List[str]) -> Dict[str, Any]:
        """Delete vectors by IDs with retry logic."""
        if not self.index:
            await self.initialize_index()
        
        try:
            response = self.index.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} vectors")
            return response
            
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            raise
    
    async def get_index_stats(self) -> Dict[str, Any]:
        """Get index statistics and health information."""
        if not self.index:
            await self.initialize_index()
        
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vector_count": stats.get("total_vector_count", 0),
                "dimension": stats.get("dimension", self.config.dimension),
                "index_fullness": stats.get("index_fullness", 0.0),
                "namespaces": stats.get("namespaces", {}),
            }
        except Exception as e:
            logger.error(f"Failed to get index stats: {e}")
            return {"error": str(e)}
    
    async def health_check(self, force_check: bool = False) -> VectorDBHealth:
        """
        Perform health check on the vector database.
        
        Args:
            force_check: Force immediate check, ignore cache
            
        Returns:
            Health status
        """
        current_time = time.time()
        
        # Use cached result if recent and not forced
        if not force_check and (current_time - self._last_health_check) < self._health_check_interval:
            return self._health_status
        
        try:
            if not self.index:
                await self.initialize_index()
            
            # Test basic connectivity
            stats = await self.get_index_stats()
            
            if "error" in stats:
                self._health_status = VectorDBHealth.UNHEALTHY
            else:
                # Check if index is responding normally
                fullness = stats.get("index_fullness", 0.0)
                if fullness > 0.9:  # Index is getting full
                    self._health_status = VectorDBHealth.DEGRADED
                else:
                    self._health_status = VectorDBHealth.HEALTHY
            
            self._last_health_check = current_time
            logger.debug(f"Health check result: {self._health_status}")
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            self._health_status = VectorDBHealth.UNHEALTHY
        
        return self._health_status
    
    async def close(self):
        """Clean up resources."""
        logger.info("Closing Pinecone client connections")
        # Pinecone client doesn't require explicit closing, but we can reset state
        self.index = None
        self._health_status = VectorDBHealth.UNKNOWN


# Async context manager for automatic resource management
@asynccontextmanager
async def get_pinecone_client(config: Optional[PineconeConfig] = None):
    """Async context manager for Pinecone client."""
    client = PineconeClient(config)
    try:
        await client.initialize_index()
        yield client
    finally:
        await client.close()


# Factory function for easy client creation
def create_pinecone_client() -> PineconeClient:
    """Create a Pinecone client with default configuration."""
    return PineconeClient()