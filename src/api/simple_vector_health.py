"""
Simplified Vector Database Health Check API

This module provides basic health monitoring for the vector database infrastructure.
Designed for stepwise implementation with minimal dependencies.
"""

import asyncio
import time
from datetime import datetime, UTC
from typing import Dict, Any
import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    uptime_seconds: float
    environment: str
    

class VectorDBStats(BaseModel):
    """Vector database statistics model"""
    provider: str
    index_name: str
    total_vectors: int
    dimension: int
    index_fullness: float
    

# Global health monitor state
class HealthMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.last_check = 0
        self.check_count = 0
        self.error_count = 0
    
    def get_uptime(self) -> float:
        return time.time() - self.start_time
    
    def record_check(self, success: bool = True):
        self.last_check = time.time()
        self.check_count += 1
        if not success:
            self.error_count += 1


# Global monitor instance
health_monitor = HealthMonitor()

# FastAPI app
app = FastAPI(
    title="Vector DB Health Monitor", 
    version="1.0.0",
    description="Health monitoring for call centre vector database"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Streamlit default
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


async def get_vector_client():
    """Create and initialize vector client"""
    try:
        from src.vector_db.pinecone_client import PineconeClient, PineconeConfig
        
        # Create config from environment
        config = PineconeConfig(
            api_key=os.getenv("PINECONE_API_KEY", ""),
            environment=os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp"),
            index_name=os.getenv("PINECONE_INDEX_NAME", "call-centre-tickets")
        )
        
        # Initialize client
        client = PineconeClient(config)
        await client.initialize_index(create_if_not_exists=False)
        return client
        
    except Exception as e:
        logger.error(f"Failed to create vector client: {e}")
        raise HTTPException(status_code=503, detail=f"Vector DB unavailable: {str(e)}")


@app.get("/health", response_model=HealthResponse)
async def basic_health_check():
    """
    Basic health check endpoint - fast response for load balancers.
    """
    try:
        # Quick environment check
        has_api_key = bool(os.getenv("PINECONE_API_KEY"))
        
        if not has_api_key:
            status = "unhealthy"
            status_code = 503
        else:
            # Try to create client (without full initialization)
            try:
                client = await get_vector_client()
                await client.close()
                status = "healthy"
                status_code = 200
                health_monitor.record_check(True)
            except Exception:
                status = "degraded" 
                status_code = 200  # Still serving but with issues
                health_monitor.record_check(False)
        
        response = HealthResponse(
            status=status,
            timestamp=datetime.now(UTC).isoformat(),
            uptime_seconds=health_monitor.get_uptime(),
            environment=os.getenv("PINECONE_ENVIRONMENT", "unknown")
        )
        
        return JSONResponse(content=response.dict(), status_code=status_code)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        health_monitor.record_check(False)
        
        error_response = HealthResponse(
            status="unhealthy",
            timestamp=datetime.now(UTC).isoformat(),
            uptime_seconds=health_monitor.get_uptime(),
            environment="error"
        )
        
        return JSONResponse(content=error_response.dict(), status_code=503)


@app.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check with full diagnostics.
    """
    start_time = time.time()
    
    try:
        client = await get_vector_client()
        
        # Run comprehensive health check
        health_status = await client.health_check(force_check=True)
        stats = await client.get_index_stats()
        
        # Calculate performance
        response_time_ms = round((time.time() - start_time) * 1000, 2)
        
        # Build detailed response
        response = {
            "status": health_status.value,
            "timestamp": datetime.now(UTC).isoformat(),
            "uptime_seconds": health_monitor.get_uptime(),
            "response_time_ms": response_time_ms,
            "vector_db": {
                "provider": "pinecone",
                "index_name": client.config.index_name,
                "total_vectors": stats.get("total_vector_count", 0),
                "dimension": stats.get("dimension", 1536),
                "index_fullness": stats.get("index_fullness", 0.0),
                "cloud": client.config.cloud,
                "region": client.config.region
            },
            "monitoring": {
                "total_checks": health_monitor.check_count,
                "error_count": health_monitor.error_count,
                "error_rate": round(health_monitor.error_count / max(health_monitor.check_count, 1), 3),
                "last_check": health_monitor.last_check
            }
        }
        
        await client.close()
        health_monitor.record_check(True)
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        health_monitor.record_check(False)
        
        error_response = {
            "status": "unhealthy",
            "timestamp": datetime.now(UTC).isoformat(),
            "uptime_seconds": health_monitor.get_uptime(),
            "response_time_ms": round((time.time() - start_time) * 1000, 2),
            "error": str(e)
        }
        
        return JSONResponse(content=error_response, status_code=503)


@app.get("/stats", response_model=VectorDBStats)  
async def get_stats():
    """
    Get current vector database statistics.
    """
    try:
        client = await get_vector_client()
        stats = await client.get_index_stats()
        
        response = VectorDBStats(
            provider="pinecone",
            index_name=client.config.index_name,
            total_vectors=stats.get("total_vector_count", 0),
            dimension=stats.get("dimension", 1536),
            index_fullness=stats.get("index_fullness", 0.0)
        )
        
        await client.close()
        return response
        
    except Exception as e:
        logger.error(f"Stats request failed: {e}")
        raise HTTPException(status_code=503, detail=f"Unable to get stats: {str(e)}")


@app.get("/metrics", response_class=PlainTextResponse)
async def prometheus_metrics():
    """
    Prometheus-compatible metrics endpoint.
    """
    try:
        client = await get_vector_client()
        health_status = await client.health_check()
        stats = await client.get_index_stats()
        
        # Convert health to numeric
        health_numeric = {"healthy": 1, "degraded": 0.5, "unhealthy": 0}.get(health_status.value, -1)
        
        metrics = [
            f'# HELP vector_db_health Vector database health (1=healthy, 0.5=degraded, 0=unhealthy)',
            f'vector_db_health{{index="{client.config.index_name}"}} {health_numeric}',
            f'# HELP vector_db_vectors Total vectors',
            f'vector_db_vectors{{index="{client.config.index_name}"}} {stats.get("total_vector_count", 0)}',
            f'# HELP vector_db_fullness Index fullness (0-1)',  
            f'vector_db_fullness{{index="{client.config.index_name}"}} {stats.get("index_fullness", 0.0)}',
            f'# HELP vector_db_checks_total Total health checks',
            f'vector_db_checks_total {health_monitor.check_count}',
            f'# HELP vector_db_errors_total Total errors',
            f'vector_db_errors_total {health_monitor.error_count}',
            f'# HELP vector_db_uptime_seconds Service uptime',
            f'vector_db_uptime_seconds {health_monitor.get_uptime()}'
        ]
        
        await client.close()
        return '\n'.join(metrics)
        
    except Exception as e:
        logger.error(f"Metrics request failed: {e}")
        return f'vector_db_health{{error="true"}} -1'


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")