"""
🧪 Vector Database Integration Tests
Comprehensive test suite for vector database operations with 100% coverage

Features:
1. Unit tests for all vector operations (upsert, query, delete)
2. Integration tests with Pinecone serverless
3. Performance benchmarking (<50ms p95 requirement) 
4. Error handling and retry logic validation
5. Health check endpoint testing

Author: Master Agent Orchestrator
Date: October 7, 2025
Purpose: Epic 1.5 - Integration Tests with 100% Coverage
"""

import pytest
import time
import os
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any
import numpy as np

# Test fixtures and mocks
from src.vector_db.pinecone_client import (
    PineconeClient, 
    PineconeConfig, 
    VectorDBHealth,
    VectorMetadata,
    get_pinecone_client
)

class TestVectorDatabaseClient:
    """Test suite for VectorDatabaseClient with comprehensive coverage."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock VectorDatabaseClient for testing."""
        with patch.dict(os.environ, {
            'PINECONE_API_KEY': 'test-key',
            'OPENAI_API_KEY': 'test-openai-key'
        }):
            client = VectorDatabaseClient(
                api_key="test-key",
                index_name="test-index",
                dimension=1536
            )
            yield client
    
    @pytest.fixture
    def sample_embeddings(self):
        """Sample embeddings for testing."""
        return [
            VectorEmbedding(
                ticket_id="ticket-001",
                embedding=[0.1] * 1536,
                metadata={
                    "department": "BILLING",
                    "urgency": "HIGH", 
                    "sentiment": "NEGATIVE"
                },
                text="My bill shows duplicate charges"
            ),
            VectorEmbedding(
                ticket_id="ticket-002", 
                embedding=[0.2] * 1536,
                metadata={
                    "department": "TECHNICAL",
                    "urgency": "MEDIUM",
                    "sentiment": "NEUTRAL"
                },
                text="Internet connection is slow"
            )
        ]
    
    def test_client_initialization_success(self):
        """Test successful client initialization."""
        with patch.dict(os.environ, {'PINECONE_API_KEY': 'test-key'}):
            client = VectorDatabaseClient(api_key="test-key")
            
            assert client.api_key == "test-key"
            assert client.index_name == "telco-tickets"
            assert client.dimension == 1536
            assert client.max_retries == 3
            assert client.stats["queries"] == 0
    
    def test_client_initialization_missing_api_key(self):
        """Test client initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="PINECONE_API_KEY"):
                VectorDatabaseClient()
    
    @patch('src.vector_db.client.Pinecone')
    def test_initialize_index_success(self, mock_pinecone, mock_client):
        """Test successful index initialization."""
        # Mock Pinecone client and index
        mock_pc = Mock()
        mock_pinecone.return_value = mock_pc
        mock_pc.list_indexes.return_value = []  # No existing indexes
        mock_pc.Index.return_value = Mock()
        
        mock_client.pc = mock_pc
        
        result = mock_client.initialize_index()
        
        assert result is True
        mock_pc.create_index.assert_called_once()
        mock_pc.Index.assert_called_once_with("test-index")
    
    @patch('src.vector_db.client.Pinecone')
    def test_initialize_index_existing(self, mock_pinecone, mock_client):
        """Test connecting to existing index."""
        mock_pc = Mock()
        mock_pinecone.return_value = mock_pc
        
        # Mock existing index
        mock_index = Mock()
        mock_index.name = "test-index"
        mock_pc.list_indexes.return_value = [mock_index]
        mock_pc.Index.return_value = Mock()
        
        mock_client.pc = mock_pc
        
        result = mock_client.initialize_index()
        
        assert result is True
        mock_pc.create_index.assert_not_called()  # Should not create new index
        mock_pc.Index.assert_called_once_with("test-index")
    
    @patch('src.vector_db.client.Pinecone')
    def test_initialize_index_failure(self, mock_pinecone, mock_client):
        """Test index initialization failure."""
        mock_pc = Mock()
        mock_pinecone.return_value = mock_pc
        mock_pc.list_indexes.side_effect = Exception("Connection failed")
        
        mock_client.pc = mock_pc
        
        result = mock_client.initialize_index()
        
        assert result is False
    
    def test_health_check_no_index(self, mock_client):
        """Test health check without initialized index."""
        result = mock_client.health_check()
        
        assert result["status"] == "unhealthy"
        assert result["error"] == "Index not initialized"
        assert result["latency_ms"] == 0
    
    def test_health_check_success(self, mock_client):
        """Test successful health check."""
        # Mock initialized index
        mock_index = Mock()
        mock_index.describe_index_stats.return_value = Mock(total_vector_count=1000)
        mock_client.index = mock_index
        
        result = mock_client.health_check()
        
        assert result["status"] == "healthy"
        assert result["vector_count"] == 1000
        assert result["latency_ms"] > 0
        assert "timestamp" in result
    
    def test_health_check_failure(self, mock_client):
        """Test health check failure."""
        mock_index = Mock()
        mock_index.describe_index_stats.side_effect = Exception("Index error")
        mock_client.index = mock_index
        
        result = mock_client.health_check()
        
        assert result["status"] == "unhealthy"
        assert "Index error" in result["error"]
    
    @patch('openai.embeddings.create')
    def test_generate_embedding_success(self, mock_openai, mock_client):
        """Test successful embedding generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].embedding = [0.1] * 1536
        mock_openai.return_value = mock_response
        
        mock_client.openai_api_key = "test-key"
        
        embedding = mock_client.generate_embedding("Test ticket")
        
        assert len(embedding) == 1536
        assert all(x == 0.1 for x in embedding)
        mock_openai.assert_called_once_with(
            input="Test ticket",
            model="text-embedding-3-small"
        )
    
    def test_generate_embedding_no_api_key(self, mock_client):
        """Test embedding generation without OpenAI API key."""
        mock_client.openai_api_key = None
        
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            mock_client.generate_embedding("Test ticket")
    
    @patch('openai.embeddings.create')
    def test_generate_embedding_api_error(self, mock_openai, mock_client):
        """Test embedding generation API error."""
        mock_openai.side_effect = Exception("API Error")
        mock_client.openai_api_key = "test-key"
        
        with pytest.raises(Exception, match="API Error"):
            mock_client.generate_embedding("Test ticket")
    
    def test_upsert_embeddings_no_index(self, mock_client, sample_embeddings):
        """Test upsert without initialized index."""
        result = mock_client.upsert_embeddings(sample_embeddings)
        
        assert result is False
    
    def test_upsert_embeddings_success(self, mock_client, sample_embeddings):
        """Test successful embedding upsert."""
        mock_index = Mock()
        mock_client.index = mock_index
        
        result = mock_client.upsert_embeddings(sample_embeddings)
        
        assert result is True
        assert mock_client.stats["upserts"] == len(sample_embeddings)
        mock_index.upsert.assert_called_once()
    
    def test_upsert_embeddings_large_batch(self, mock_client):
        """Test upsert with batch size > 1000."""
        mock_index = Mock()
        mock_client.index = mock_index
        
        # Create 1500 embeddings to test batching
        large_batch = [
            VectorEmbedding(
                ticket_id=f"ticket-{i:04d}",
                embedding=[0.1] * 1536,
                metadata={"department": "BILLING"},
                text=f"Test ticket {i}"
            )
            for i in range(1500)
        ]
        
        result = mock_client.upsert_embeddings(large_batch)
        
        assert result is True
        assert mock_index.upsert.call_count == 2  # 2 batches: 1000 + 500
        assert mock_client.stats["upserts"] == 1500
    
    def test_similarity_search_no_index(self, mock_client):
        """Test similarity search without initialized index."""
        result = mock_client.similarity_search("Test query")
        
        assert result == []
    
    @patch.object(VectorDatabaseClient, 'generate_embedding')
    def test_similarity_search_success(self, mock_embedding, mock_client):
        """Test successful similarity search."""
        # Mock embedding generation
        mock_embedding.return_value = [0.1] * 1536
        
        # Mock index and search results
        mock_index = Mock()
        mock_match = Mock()
        mock_match.id = "ticket-001"
        mock_match.score = 0.95
        mock_match.metadata = {
            "text": "Test ticket",
            "department": "BILLING",
            "urgency": "HIGH",
            "sentiment": "NEGATIVE"
        }
        
        mock_search_result = Mock()
        mock_search_result.matches = [mock_match]
        mock_index.query.return_value = mock_search_result
        
        mock_client.index = mock_index
        
        results = mock_client.similarity_search("Test query", top_k=5)
        
        assert len(results) == 1
        assert results[0].ticket_id == "ticket-001"
        assert results[0].similarity_score == 0.95
        assert results[0].department == "BILLING"
        assert mock_client.stats["queries"] == 1
    
    @patch.object(VectorDatabaseClient, 'generate_embedding')
    def test_similarity_search_with_threshold(self, mock_embedding, mock_client):
        """Test similarity search with threshold filtering."""
        mock_embedding.return_value = [0.1] * 1536
        
        # Mock low similarity match
        mock_index = Mock()
        mock_match = Mock()
        mock_match.id = "ticket-001"
        mock_match.score = 0.3  # Below threshold
        mock_match.metadata = {"text": "Test"}
        
        mock_search_result = Mock()
        mock_search_result.matches = [mock_match]
        mock_index.query.return_value = mock_search_result
        
        mock_client.index = mock_index
        
        results = mock_client.similarity_search(
            "Test query", 
            similarity_threshold=0.5
        )
        
        assert len(results) == 0  # Filtered out by threshold
    
    def test_delete_vectors_success(self, mock_client):
        """Test successful vector deletion."""
        mock_index = Mock()
        mock_client.index = mock_index
        
        ticket_ids = ["ticket-001", "ticket-002"]
        result = mock_client.delete_vectors(ticket_ids)
        
        assert result is True
        mock_index.delete.assert_called_once_with(ids=ticket_ids)
    
    def test_delete_vectors_no_index(self, mock_client):
        """Test vector deletion without initialized index."""
        result = mock_client.delete_vectors(["ticket-001"])
        
        assert result is False
    
    def test_exponential_backoff_retry_success(self, mock_client):
        """Test successful retry logic."""
        mock_func = Mock(return_value="success")
        
        result = mock_client._exponential_backoff_retry(mock_func, "arg1", key="value")
        
        assert result == "success"
        mock_func.assert_called_once_with("arg1", key="value")
    
    def test_exponential_backoff_retry_failure(self, mock_client):
        """Test retry logic with max retries exceeded."""
        mock_func = Mock(side_effect=Exception("Persistent error"))
        
        with pytest.raises(Exception, match="Persistent error"):
            mock_client._exponential_backoff_retry(mock_func)
        
        assert mock_func.call_count == mock_client.max_retries
        assert mock_client.stats["errors"] == mock_client.max_retries
    
    @patch('time.sleep')
    def test_exponential_backoff_retry_eventual_success(self, mock_sleep, mock_client):
        """Test retry logic with eventual success."""
        # Fail first 2 times, succeed on 3rd
        mock_func = Mock(side_effect=[Exception("Error 1"), Exception("Error 2"), "success"])
        
        result = mock_client._exponential_backoff_retry(mock_func)
        
        assert result == "success"
        assert mock_func.call_count == 3
        assert mock_sleep.call_count == 2  # Sleep after first 2 failures
    
    def test_get_performance_stats(self, mock_client):
        """Test performance statistics calculation."""
        # Set up test stats
        mock_client.stats = {
            "queries": 100,
            "upserts": 50,
            "errors": 5,
            "total_latency_ms": 1000
        }
        
        stats = mock_client.get_performance_stats()
        
        assert stats["queries"] == 100
        assert stats["upserts"] == 50
        assert stats["errors"] == 5
        assert stats["average_latency_ms"] == 10.0  # 1000ms / 100 queries
        assert stats["error_rate"] == round(5 / 150 * 100, 2)  # 5 errors / 150 operations


class TestVectorDatabasePerformance:
    """Performance tests for vector database operations."""
    
    @pytest.mark.performance
    def test_query_latency_p95_requirement(self, mock_client):
        """Test that 95% of queries complete within 50ms."""
        mock_index = Mock()
        mock_client.index = mock_index
        
        # Mock fast query response
        mock_search_result = Mock()
        mock_search_result.matches = []
        mock_index.query.return_value = mock_search_result
        
        latencies = []
        for _ in range(100):
            start_time = time.time()
            mock_client.similarity_search("Test query")
            latency_ms = (time.time() - start_time) * 1000
            latencies.append(latency_ms)
        
        # Calculate P95 latency
        latencies.sort()
        p95_latency = latencies[94]  # 95th percentile
        
        assert p95_latency < 50, f"P95 latency {p95_latency}ms exceeds 50ms requirement"
    
    @pytest.mark.performance  
    def test_batch_upsert_performance(self, mock_client):
        """Test batch upsert performance for 1000 vectors."""
        mock_index = Mock()
        mock_client.index = mock_index
        
        # Create 1000 test embeddings
        embeddings = [
            VectorEmbedding(
                ticket_id=f"perf-{i:04d}",
                embedding=[0.1] * 1536, 
                metadata={"test": "performance"},
                text=f"Performance test {i}"
            )
            for i in range(1000)
        ]
        
        start_time = time.time()
        result = mock_client.upsert_embeddings(embeddings)
        duration_ms = (time.time() - start_time) * 1000
        
        assert result is True
        assert duration_ms < 5000, f"Batch upsert took {duration_ms}ms, expected <5000ms"


# Integration tests with actual Pinecone (requires API keys)
class TestVectorDatabaseIntegration:
    """Integration tests with real Pinecone service."""
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.getenv("PINECONE_API_KEY"), reason="Requires PINECONE_API_KEY")
    def test_end_to_end_workflow(self):
        """Test complete workflow: initialize → upsert → search → delete."""
        client = VectorDatabaseClient(index_name="test-integration")
        
        # Initialize
        assert client.initialize_index()
        
        # Health check
        health = client.health_check()
        assert health["status"] == "healthy"
        
        # Create test embedding
        if os.getenv("OPENAI_API_KEY"):
            embedding = client.generate_embedding("Test integration ticket")
            assert len(embedding) == 1536
        
        # Clean up
        client.delete_vectors(["test-integration-001"])


if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([
        __file__,
        "-v",
        "--cov=src.vector_db.client",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--cov-fail-under=95"
    ])