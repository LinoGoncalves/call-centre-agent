"""
🏥 Vector Database Health Check API Endpoint
FastAPI endpoint for monitoring vector database health and performance

Features:
1. Real-time health status monitoring
2. Performance metrics and statistics
3. Latency tracking and error rates
4. Integration with Prometheus metrics

Author: Master Agent Orchestrator  
Date: October 7, 2025
Purpose: Epic 1.4 - Health Check Endpoint Implementation
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import time

from .client import VectorDatabaseClient

# Setup logging
logger = logging.getLogger(__name__)

# Health check models
class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str  # "healthy" | "degraded" | "unhealthy"
    timestamp: str
    latency_ms: float
    vector_count: Optional[int] = None
    error_message: Optional[str] = None
    performance_stats: Optional[Dict[str, Any]] = None

class PerformanceStats(BaseModel):
    """Performance statistics model."""
    queries_total: int
    upserts_total: int  
    errors_total: int
    average_latency_ms: float
    error_rate_percent: float
    uptime_hours: float

# Dependency injection for vector client
def get_vector_client() -> VectorDatabaseClient:
    """Get vector database client instance."""
    try:
        client = VectorDatabaseClient()
        if not client.initialize_index():
            raise HTTPException(status_code=503, detail="Vector database initialization failed")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize vector client: {e}")
        raise HTTPException(status_code=503, detail=f"Vector database unavailable: {str(e)}")

# FastAPI app for health checks
app = FastAPI(title="Vector DB Health Monitor", version="1.0.0")

@app.get("/vector-db/health", response_model=HealthCheckResponse)
async def vector_db_health_check(client: VectorDatabaseClient = Depends(get_vector_client)):
    """
    Comprehensive health check for vector database.
    
    Returns:
        HealthCheckResponse with status, latency, and performance metrics
    """
    try:
        start_time = time.time()
        
        # Perform health check
        health_result = client.health_check()
        
        # Determine status based on latency and errors
        status = "healthy"
        if health_result["latency_ms"] > 200:  # P95 target: <50ms, warning at 200ms
            status = "degraded"
        if health_result["status"] == "unhealthy":
            status = "unhealthy"
        
        # Get performance statistics
        perf_stats = client.get_performance_stats()
        
        return HealthCheckResponse(
            status=status,
            timestamp=datetime.now().isoformat(),
            latency_ms=health_result["latency_ms"],
            vector_count=health_result.get("vector_count"),
            error_message=health_result.get("error"),
            performance_stats=perf_stats
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            latency_ms=0.0,
            error_message=str(e)
        )

@app.get("/vector-db/stats", response_model=PerformanceStats) 
async def get_performance_statistics(client: VectorDatabaseClient = Depends(get_vector_client)):
    """
    Get detailed performance statistics.
    
    Returns:
        PerformanceStats with comprehensive metrics
    """
    try:
        stats = client.get_performance_stats()
        
        return PerformanceStats(
            queries_total=stats["queries"],
            upserts_total=stats["upserts"],
            errors_total=stats["errors"],
            average_latency_ms=stats["average_latency_ms"],
            error_rate_percent=stats["error_rate"],
            uptime_hours=0.0  # TODO: Track actual uptime
        )
        
    except Exception as e:
        logger.error(f"Failed to get performance stats: {e}")
        raise HTTPException(status_code=500, detail=f"Stats unavailable: {str(e)}")

@app.get("/vector-db/ping")
async def ping_vector_db(client: VectorDatabaseClient = Depends(get_vector_client)):
    """
    Simple ping endpoint for basic connectivity check.
    
    Returns:
        Simple status response for load balancer health checks
    """
    try:
        start_time = time.time()
        health = client.health_check()
        latency = (time.time() - start_time) * 1000
        
        if health["status"] == "healthy" and latency < 500:  # 500ms timeout
            return {"status": "ok", "latency_ms": round(latency, 2)}
        else:
            raise HTTPException(status_code=503, detail="Service unavailable")
            
    except Exception as e:
        logger.error(f"Ping failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

# Prometheus metrics endpoint
@app.get("/metrics")
async def prometheus_metrics(client: VectorDatabaseClient = Depends(get_vector_client)):
    """
    Prometheus-compatible metrics endpoint.
    
    Returns:
        Metrics in Prometheus text format
    """
    try:
        stats = client.get_performance_stats()
        health = client.health_check()
        
        # Format metrics for Prometheus
        metrics = f"""# HELP vector_db_queries_total Total number of vector database queries
# TYPE vector_db_queries_total counter
vector_db_queries_total {stats["queries"]}

# HELP vector_db_upserts_total Total number of vector upsert operations  
# TYPE vector_db_upserts_total counter
vector_db_upserts_total {stats["upserts"]}

# HELP vector_db_errors_total Total number of vector database errors
# TYPE vector_db_errors_total counter  
vector_db_errors_total {stats["errors"]}

# HELP vector_db_latency_ms Average query latency in milliseconds
# TYPE vector_db_latency_ms gauge
vector_db_latency_ms {stats["average_latency_ms"]}

# HELP vector_db_vector_count Total number of vectors stored
# TYPE vector_db_vector_count gauge
vector_db_vector_count {health.get("vector_count", 0)}

# HELP vector_db_health_status Health status (1=healthy, 0.5=degraded, 0=unhealthy)
# TYPE vector_db_health_status gauge
vector_db_health_status {1 if health["status"] == "healthy" else 0.5 if health["status"] == "degraded" else 0}
"""
        
        return metrics
        
    except Exception as e:
        logger.error(f"Metrics generation failed: {e}")
        raise HTTPException(status_code=500, detail="Metrics unavailable")

if __name__ == "__main__":
    import uvicorn
    
    # Run health check server
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001, 
        log_level="info"
    )