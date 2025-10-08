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
    timestamp: datetime
    uptime_seconds: Optional[float] = None
    version: str = "1.0.0"
    environment: Optional[str] = None
    

class DetailedHealthResponse(HealthResponse):
    """Extended health response with database details"""
    vector_db: Dict[str, Any]
    performance: Dict[str, Any]
    

class VectorDBStats(BaseModel):
    """Vector database statistics model"""
    total_vectors: int
    dimension: int
    index_fullness: float
    namespaces: Dict[str, Any]
    last_updated: datetime


# Global state for health monitoring
class HealthMonitor:
    """Centralized health monitoring state"""
    
    def __init__(self):
        self.start_time = time.time()
        self.last_health_check = 0
        self.cached_health_status = VectorDBHealth.UNKNOWN
        self.health_check_count = 0
        self.error_count = 0
        
    def get_uptime(self) -> float:
        """Get service uptime in seconds"""
        return time.time() - self.start_time
    
    def record_health_check(self, status: VectorDBHealth):
        """Record health check result"""
        self.last_health_check = time.time()
        self.cached_health_status = status
        self.health_check_count += 1
        
        if status == VectorDBHealth.UNHEALTHY:
            self.error_count += 1


# Global monitor instance
health_monitor = HealthMonitor()


# Dependency injection for Pinecone client
async def get_vector_client() -> PineconeClient:
    """Dependency to get initialized Pinecone client"""
    try:
        config = PineconeConfig()
        client = PineconeClient(config)
        await client.initialize_index(create_if_not_exists=False)  # Don't auto-create in health checks
        return client
    except Exception as e:
        logger.error(f"Failed to initialize vector client: {e}")
        raise HTTPException(
            status_code=503, 
            detail=f"Vector database unavailable: {str(e)}"
        )


# Health check endpoints
app = FastAPI(
    title="Call Centre Agent - Vector DB Health API",
    description="Health monitoring and metrics for vector database infrastructure",
    version="1.0.0"
)


@app.get("/vector-db/health", response_model=HealthResponse)
async def basic_health_check(
    background_tasks: BackgroundTasks,
    client: PineconeClient = Depends(get_vector_client)
) -> HealthResponse:
    """
    Basic health check endpoint.
    
    Returns simple status for load balancers and monitoring systems.
    Designed to respond quickly (< 100ms) for high-frequency checks.
    """
    try:
        # Quick health check with caching
        health_status = await client.health_check(force_check=False)
        
        # Record health check in background
        background_tasks.add_task(
            health_monitor.record_health_check, 
            health_status
        )
        
        # Map health status to HTTP status
        if health_status == VectorDBHealth.HEALTHY:
            status_code = 200
            status_text = "healthy"
        elif health_status == VectorDBHealth.DEGRADED:
            status_code = 200  # Still serving traffic but with warnings
            status_text = "degraded"
        else:  # UNHEALTHY or UNKNOWN
            status_code = 503
            status_text = "unhealthy"
            
        response = HealthResponse(
            status=status_text,
            timestamp=datetime.now(UTC),
            uptime_seconds=health_monitor.get_uptime(),
            environment=client.config.environment
        )
        
        return JSONResponse(
            content=response.dict(),
            status_code=status_code
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        
        error_response = HealthResponse(
            status="unhealthy",
            timestamp=datetime.now(UTC),
            uptime_seconds=health_monitor.get_uptime()
        )
        
        return JSONResponse(
            content=error_response.dict(),
            status_code=503
        )


@app.get("/vector-db/health/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check(
    client: PineconeClient = Depends(get_vector_client)
) -> DetailedHealthResponse:
    """
    Detailed health check with comprehensive diagnostics.
    
    Includes database statistics, performance metrics, and diagnostic information.
    May take longer to respond (< 5s) - use for monitoring dashboards.
    """
    start_time = time.time()
    
    try:
        # Force fresh health check
        health_status = await client.health_check(force_check=True)
        
        # Get detailed statistics
        index_stats = await client.get_index_stats()
        
        # Calculate performance metrics
        response_time = time.time() - start_time
        
        # Map health status
        if health_status == VectorDBHealth.HEALTHY:
            status_text = "healthy"
        elif health_status == VectorDBHealth.DEGRADED:
            status_text = "degraded"
        else:
            status_text = "unhealthy"
        
        # Build comprehensive response
        response = DetailedHealthResponse(
            status=status_text,
            timestamp=datetime.now(timezone.utc),
            uptime_seconds=health_monitor.get_uptime(),
            environment=client.config.environment,
            vector_db={
                "provider": "pinecone",
                "index_name": client.config.index_name,
                "total_vectors": index_stats.get("total_vector_count", 0),
                "dimension": index_stats.get("dimension", client.config.dimension),
                "index_fullness": index_stats.get("index_fullness", 0.0),
                "metric": client.config.metric,
                "cloud": client.config.cloud,
                "region": client.config.region
            },
            performance={
                "health_check_response_time_ms": round(response_time * 1000, 2),
                "total_health_checks": health_monitor.health_check_count,
                "error_rate": round(health_monitor.error_count / max(health_monitor.health_check_count, 1), 3),
                "last_check_timestamp": health_monitor.last_health_check,
                "cache_hit": not (response_time > 1.0)  # Assume cache miss if slow
            }
        )
        
        # Update monitoring state
        health_monitor.record_health_check(health_status)
        
        return response
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        
        error_response = DetailedHealthResponse(
            status="unhealthy",
            timestamp=datetime.now(timezone.utc),
            uptime_seconds=health_monitor.get_uptime(),
            vector_db={"error": str(e)},
            performance={
                "health_check_response_time_ms": round((time.time() - start_time) * 1000, 2),
                "error": True
            }
        )
        
        raise HTTPException(
            status_code=503,
            detail=error_response.dict()
        )


@app.get("/vector-db/stats", response_model=VectorDBStats)
async def get_vector_db_stats(
    client: PineconeClient = Depends(get_vector_client)
) -> VectorDBStats:
    """
    Get current vector database statistics.
    
    Returns operational metrics for monitoring and capacity planning.
    """
    try:
        stats = await client.get_index_stats()
        
        return VectorDBStats(
            total_vectors=stats.get("total_vector_count", 0),
            dimension=stats.get("dimension", client.config.dimension),
            index_fullness=stats.get("index_fullness", 0.0),
            namespaces=stats.get("namespaces", {}),
            last_updated=datetime.now(timezone.utc)
        )
        
    except Exception as e:
        logger.error(f"Failed to get vector DB stats: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Unable to retrieve vector database statistics: {str(e)}"
        )


@app.get("/vector-db/metrics")
async def get_prometheus_metrics(
    client: PineconeClient = Depends(get_vector_client)
) -> str:
    """
    Prometheus-compatible metrics endpoint.
    
    Returns metrics in Prometheus text format for scraping by monitoring systems.
    """
    try:
        health_status = await client.health_check(force_check=False)
        stats = await client.get_index_stats()
        
        # Convert health status to numeric
        health_numeric = {
            VectorDBHealth.HEALTHY: 1,
            VectorDBHealth.DEGRADED: 0.5,
            VectorDBHealth.UNHEALTHY: 0,
            VectorDBHealth.UNKNOWN: -1
        }.get(health_status, -1)
        
        # Format Prometheus metrics
        metrics = [
            f'# HELP vector_db_health_status Vector database health status (1=healthy, 0.5=degraded, 0=unhealthy, -1=unknown)',
            f'# TYPE vector_db_health_status gauge',
            f'vector_db_health_status{{index="{client.config.index_name}",environment="{client.config.environment}"}} {health_numeric}',
            '',
            f'# HELP vector_db_total_vectors Total number of vectors in the database',
            f'# TYPE vector_db_total_vectors gauge',
            f'vector_db_total_vectors{{index="{client.config.index_name}"}} {stats.get("total_vector_count", 0)}',
            '',
            f'# HELP vector_db_index_fullness Index capacity utilization (0.0-1.0)',
            f'# TYPE vector_db_index_fullness gauge',
            f'vector_db_index_fullness{{index="{client.config.index_name}"}} {stats.get("index_fullness", 0.0)}',
            '',
            f'# HELP vector_db_health_checks_total Total number of health checks performed',
            f'# TYPE vector_db_health_checks_total counter',
            f'vector_db_health_checks_total {{index="{client.config.index_name}"}} {health_monitor.health_check_count}',
            '',
            f'# HELP vector_db_errors_total Total number of health check errors',
            f'# TYPE vector_db_errors_total counter',
            f'vector_db_errors_total{{index="{client.config.index_name}"}} {health_monitor.error_count}',
            '',
            f'# HELP vector_db_uptime_seconds Service uptime in seconds',
            f'# TYPE vector_db_uptime_seconds counter',
            f'vector_db_uptime_seconds {{index="{client.config.index_name}"}} {health_monitor.get_uptime()}'
        ]
        
        return '\n'.join(metrics)
        
    except Exception as e:
        logger.error(f"Failed to generate metrics: {e}")
        # Return error metric
        return f'vector_db_health_status{{error="true"}} -1'


# Add CORS middleware for frontend access
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    
    # Run the health check API
    uvicorn.run(
        "src.api.vector_health:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )