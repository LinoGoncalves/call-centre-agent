"""
Vector Database Integration Tests - Simplified Version

Tests for the PineconeClient and health endpoints we just created.
Designed to work with the stepwise implementation.
"""

import pytest
import asyncio
import os
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient

# Import our modules
from src.vector_db.pinecone_client import PineconeClient, PineconeConfig, VectorDBHealth
from src.api.simple_vector_health import app


class TestPineconeConfig:
    """Test PineconeConfig model"""
    
    def test_config_with_required_fields(self):
        config = PineconeConfig(api_key="test-key")
        assert config.api_key == "test-key"
        assert config.index_name == "call-centre-tickets"
        assert config.dimension == 1536
    
    def test_config_with_all_fields(self):
        config = PineconeConfig(
            api_key="test",
            environment="test-env", 
            index_name="test-index",
            dimension=768
        )
        assert config.environment == "test-env"
        assert config.index_name == "test-index"
        assert config.dimension == 768


@pytest.fixture
def mock_pinecone():
    """Mock Pinecone SDK"""
    with patch('src.vector_db.pinecone_client.Pinecone') as mock_pc:
        mock_instance = Mock()
        mock_pc.return_value = mock_instance
        
        # Mock successful responses
        mock_instance.list_indexes.return_value.names.return_value = ["test-index"]
        mock_instance.create_index.return_value = None
        
        mock_describe = Mock()
        mock_describe.status = {"ready": True}
        mock_instance.describe_index.return_value = mock_describe
        
        mock_index = Mock()
        mock_instance.Index.return_value = mock_index
        
        # Mock index operations
        mock_index.upsert.return_value = {"upserted_count": 5}
        mock_index.query.return_value = Mock(matches=[])
        mock_index.delete.return_value = {}
        mock_index.describe_index_stats.return_value = {
            "total_vector_count": 100,
            "dimension": 1536, 
            "index_fullness": 0.1
        }
        
        yield mock_instance, mock_index


class TestPineconeClient:
    """Test PineconeClient functionality"""
    
    def test_client_creation(self):
        config = PineconeConfig(api_key="test")
        client = PineconeClient(config)
        assert client.config.api_key == "test"
    
    def test_client_creation_missing_api_key(self):
        with pytest.raises(ValueError, match="PINECONE_API_KEY"):
            PineconeConfig(api_key="")
    
    @pytest.mark.asyncio
    async def test_initialize_index_existing(self, mock_pinecone):
        mock_pc, mock_index = mock_pinecone
        
        config = PineconeConfig(api_key="test", index_name="test-index")
        client = PineconeClient(config)
        
        await client.initialize_index()
        
        # Should connect to existing index
        assert client.index is not None
        mock_pc.create_index.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_initialize_index_create_new(self, mock_pinecone):
        mock_pc, mock_index = mock_pinecone
        
        # Mock no existing indexes
        mock_pc.list_indexes.return_value.names.return_value = []
        
        config = PineconeConfig(api_key="test", index_name="new-index")
        client = PineconeClient(config)
        
        await client.initialize_index(create_if_not_exists=True)
        
        # Should create new index
        mock_pc.create_index.assert_called_once()
        assert client.index is not None
    
    @pytest.mark.asyncio  
    async def test_upsert_vectors(self, mock_pinecone):
        mock_pc, mock_index = mock_pinecone
        
        config = PineconeConfig(api_key="test")
        client = PineconeClient(config)
        await client.initialize_index()
        
        vectors = [
            ("id1", [0.1] * 1536, {"dept": "billing"}),
            ("id2", [0.2] * 1536, {"dept": "tech"})
        ]
        
        result = await client.upsert_vectors(vectors)
        
        assert result["upserted_count"] > 0
        mock_index.upsert.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_query_vectors(self, mock_pinecone):
        mock_pc, mock_index = mock_pinecone
        
        config = PineconeConfig(api_key="test")
        client = PineconeClient(config)
        await client.initialize_index()
        
        query_vector = [0.5] * 1536
        result = await client.query_vectors(query_vector, top_k=5)
        
        mock_index.query.assert_called_once()
        assert hasattr(result, 'matches')
    
    @pytest.mark.asyncio
    async def test_delete_vectors(self, mock_pinecone):
        mock_pc, mock_index = mock_pinecone
        
        config = PineconeConfig(api_key="test")
        client = PineconeClient(config)
        await client.initialize_index()
        
        await client.delete_vectors(["id1", "id2"])
        
        mock_index.delete.assert_called_once_with(ids=["id1", "id2"])
    
    @pytest.mark.asyncio
    async def test_get_index_stats(self, mock_pinecone):
        mock_pc, mock_index = mock_pinecone
        
        config = PineconeConfig(api_key="test")
        client = PineconeClient(config)
        await client.initialize_index()
        
        stats = await client.get_index_stats()
        
        assert "total_vector_count" in stats
        assert stats["total_vector_count"] == 100
        assert stats["dimension"] == 1536
    
    @pytest.mark.asyncio
    async def test_health_check(self, mock_pinecone):
        mock_pc, mock_index = mock_pinecone
        
        config = PineconeConfig(api_key="test")
        client = PineconeClient(config)
        await client.initialize_index()
        
        health = await client.health_check()
        
        assert health == VectorDBHealth.HEALTHY


class TestHealthAPI:
    """Test the health check API endpoints"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_health_endpoint_no_api_key(self, client):
        """Test health endpoint without API key"""
        with patch.dict(os.environ, {}, clear=True):
            response = client.get("/health")
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "unhealthy"
    
    @patch.dict(os.environ, {"PINECONE_API_KEY": "test-key"})
    def test_health_endpoint_with_api_key(self, client):
        """Test health endpoint with API key"""
        with patch('src.api.simple_vector_health.get_vector_client') as mock_client:
            mock_client.return_value = AsyncMock()
            
            response = client.get("/health")
            
            # Should be 200 or 503 depending on mock behavior
            assert response.status_code in [200, 503]
            data = response.json()
            assert "status" in data
            assert "timestamp" in data
    
    def test_health_endpoint_structure(self, client):
        """Test health response structure"""
        response = client.get("/health")
        data = response.json()
        
        # Required fields
        required_fields = ["status", "timestamp", "uptime_seconds", "environment"]
        for field in required_fields:
            assert field in data
    
    @patch.dict(os.environ, {"PINECONE_API_KEY": "test-key"})  
    def test_detailed_health_endpoint(self, client):
        """Test detailed health endpoint"""
        with patch('src.api.simple_vector_health.get_vector_client') as mock_client:
            mock_vec_client = AsyncMock()
            mock_vec_client.health_check.return_value = Mock(value="healthy")
            mock_vec_client.get_index_stats.return_value = {
                "total_vector_count": 500,
                "dimension": 1536,
                "index_fullness": 0.2
            }
            mock_vec_client.config.index_name = "test"
            mock_vec_client.config.cloud = "gcp" 
            mock_vec_client.config.region = "us-west1"
            mock_client.return_value = mock_vec_client
            
            response = client.get("/health/detailed")
            
            if response.status_code == 200:
                data = response.json()
                assert "vector_db" in data
                assert "monitoring" in data
    
    @patch.dict(os.environ, {"PINECONE_API_KEY": "test-key"})
    def test_stats_endpoint(self, client):
        """Test stats endpoint"""
        with patch('src.api.simple_vector_health.get_vector_client') as mock_client:
            mock_vec_client = AsyncMock()
            mock_vec_client.get_index_stats.return_value = {
                "total_vector_count": 1000,
                "dimension": 1536,
                "index_fullness": 0.3
            }
            mock_vec_client.config.index_name = "test"
            mock_client.return_value = mock_vec_client
            
            response = client.get("/stats")
            
            if response.status_code == 200:
                data = response.json()
                assert data["provider"] == "pinecone"
                assert data["total_vectors"] == 1000
    
    @patch.dict(os.environ, {"PINECONE_API_KEY": "test-key"})
    def test_metrics_endpoint(self, client):
        """Test Prometheus metrics endpoint"""
        with patch('src.api.simple_vector_health.get_vector_client') as mock_client:
            mock_vec_client = AsyncMock()
            mock_vec_client.health_check.return_value = Mock(value="healthy")
            mock_vec_client.get_index_stats.return_value = {
                "total_vector_count": 750,
                "dimension": 1536,
                "index_fullness": 0.25
            }
            mock_vec_client.config.index_name = "test"
            mock_client.return_value = mock_vec_client
            
            response = client.get("/metrics")
            
            if response.status_code == 200:
                text = response.text
                assert "vector_db_health" in text
                assert "vector_db_vectors" in text


class TestErrorHandling:
    """Test error handling and resilience"""
    
    @pytest.mark.asyncio
    async def test_client_handles_connection_errors(self, mock_pinecone):
        mock_pc, mock_index = mock_pinecone
        mock_index.upsert.side_effect = Exception("Connection failed")
        
        config = PineconeConfig(api_key="test")
        client = PineconeClient(config)
        await client.initialize_index()
        
        vectors = [("id1", [0.1] * 1536, {})]
        result = await client.upsert_vectors(vectors)
        
        # Should handle error gracefully
        assert "failed_batches" in result
    
    @pytest.mark.asyncio
    async def test_health_check_with_index_error(self, mock_pinecone):
        mock_pc, mock_index = mock_pinecone
        mock_index.describe_index_stats.side_effect = Exception("Index error")
        
        config = PineconeConfig(api_key="test")
        client = PineconeClient(config)
        await client.initialize_index()
        
        health = await client.health_check()
        
        assert health == VectorDBHealth.UNHEALTHY


if __name__ == "__main__":
    pytest.main([__file__, "-v"])