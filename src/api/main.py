"""
FastAPI Model Serving Application
Production-ready API for call centre ticket classification
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
import time
import uuid
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.ticket_classifier import TicketClassificationPipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Telkom Call Centre Ticket Classification API",
    description="Automated ticket classification system for call centre operations",
    version="1.0.0",
    contact={
        "name": "Call Centre AI Team",
        "email": "ai-team@telkom.co.za"
    }
)

# Global model instance
model_pipeline: Optional[TicketClassificationPipeline] = None
model_loaded_at: Optional[datetime] = None

# Request/Response Models
class TicketClassificationRequest(BaseModel):
    """Request model for single ticket classification."""
    ticket_text: str = Field(
        ..., 
        description="The ticket text to classify",
        min_length=10,
        max_length=1000,
        example="My internet has been slow for the past week, speeds are under 10Mbps"
    )
    ticket_id: Optional[str] = Field(
        None,
        description="Optional ticket ID for tracking",
        example="TCK12345"
    )
    priority: Optional[str] = Field(
        None,
        description="Ticket priority level",
        example="HIGH"
    )

class BatchClassificationRequest(BaseModel):
    """Request model for batch ticket classification."""
    tickets: List[TicketClassificationRequest] = Field(
        ...,
        description="List of tickets to classify",
        max_items=100  # Rate limiting
    )

class ClassificationResponse(BaseModel):
    """Response model for ticket classification."""
    ticket_id: Optional[str]
    predicted_category: str = Field(
        description="Predicted ticket category"
    )
    confidence: float = Field(
        description="Prediction confidence score (0-1)"
    )
    processing_time_ms: float = Field(
        description="Processing time in milliseconds"
    )
    timestamp: datetime = Field(
        description="Prediction timestamp"
    )

class BatchClassificationResponse(BaseModel):
    """Response model for batch classification."""
    results: List[ClassificationResponse]
    total_tickets: int
    successful_classifications: int
    total_processing_time_ms: float

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    model_loaded: bool
    model_loaded_at: Optional[datetime]
    uptime_seconds: float

class MetricsResponse(BaseModel):
    """API metrics response model."""
    total_requests: int
    average_response_time_ms: float
    model_accuracy: Optional[float]
    uptime_seconds: float

# Global metrics tracking
request_count = 0
total_response_time = 0.0
start_time = time.time()

@app.on_event("startup")
async def load_model():
    """Load the trained model on startup."""
    global model_pipeline, model_loaded_at
    
    logger.info("🚀 Starting Telkom Ticket Classification API...")
    
    try:
        # Initialize model pipeline
        model_pipeline = TicketClassificationPipeline()
        
        # Try to load pre-trained model
        model_path = "models/ticket_classifier_model.pkl"
        if os.path.exists(model_path):
            model_pipeline.load_model(model_path)
            model_loaded_at = datetime.now()
            logger.info(f"✅ Pre-trained model loaded from {model_path}")
        else:
            logger.warning(f"⚠️ No pre-trained model found at {model_path}")
            logger.info("🔧 Model will need to be trained before first use")
            
    except Exception as e:
        logger.error(f"❌ Failed to load model: {str(e)}")
        model_pipeline = None

@app.middleware("http")
async def track_requests(request: Request, call_next):
    """Middleware to track request metrics."""
    global request_count, total_response_time
    
    start_time_req = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time_req
    
    request_count += 1
    total_response_time += process_time
    
    return response

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    uptime = time.time() - start_time
    
    return HealthResponse(
        status="healthy" if model_pipeline is not None else "unhealthy",
        model_loaded=model_pipeline is not None,
        model_loaded_at=model_loaded_at,
        uptime_seconds=uptime
    )

@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get API performance metrics."""
    uptime = time.time() - start_time
    avg_response_time = (total_response_time / request_count * 1000) if request_count > 0 else 0
    
    return MetricsResponse(
        total_requests=request_count,
        average_response_time_ms=avg_response_time,
        model_accuracy=None,  # Would be populated from model monitoring
        uptime_seconds=uptime
    )

@app.post("/classify", response_model=ClassificationResponse)
async def classify_ticket(request: TicketClassificationRequest):
    """Classify a single ticket."""
    if model_pipeline is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded. Please ensure the model is trained and available."
        )
    
    try:
        # Record processing start time
        start_time_proc = time.time()
        
        # Make prediction
        prediction = model_pipeline.predict([request.ticket_text])[0]
        probabilities = model_pipeline.predict_proba([request.ticket_text])[0]
        confidence = float(max(probabilities))
        
        # Calculate processing time
        processing_time = (time.time() - start_time_proc) * 1000
        
        # Generate ticket ID if not provided
        ticket_id = request.ticket_id or str(uuid.uuid4())
        
        logger.info(f"📊 Classified ticket {ticket_id}: {prediction} (confidence: {confidence:.3f})")
        
        return ClassificationResponse(
            ticket_id=ticket_id,
            predicted_category=prediction,
            confidence=confidence,
            processing_time_ms=processing_time,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"❌ Classification error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.post("/classify/batch", response_model=BatchClassificationResponse)
async def classify_tickets_batch(request: BatchClassificationRequest):
    """Classify multiple tickets in batch."""
    if model_pipeline is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded. Please ensure the model is trained and available."
        )
    
    if len(request.tickets) > 100:
        raise HTTPException(
            status_code=400,
            detail="Batch size too large. Maximum 100 tickets per batch."
        )
    
    try:
        start_time_batch = time.time()
        
        # Extract text from all tickets
        ticket_texts = [ticket.ticket_text for ticket in request.tickets]
        
        # Batch prediction
        predictions = model_pipeline.predict(ticket_texts)
        probabilities = model_pipeline.predict_proba(ticket_texts)
        
        # Process results
        results = []
        successful_count = 0
        
        for i, ticket_request in enumerate(request.tickets):
            try:
                ticket_id = ticket_request.ticket_id or str(uuid.uuid4())
                confidence = float(max(probabilities[i]))
                
                result = ClassificationResponse(
                    ticket_id=ticket_id,
                    predicted_category=predictions[i],
                    confidence=confidence,
                    processing_time_ms=0,  # Individual timing not tracked in batch
                    timestamp=datetime.now()
                )
                results.append(result)
                successful_count += 1
                
            except Exception as e:
                logger.error(f"❌ Error processing ticket {i}: {str(e)}")
                continue
        
        total_processing_time = (time.time() - start_time_batch) * 1000
        
        logger.info(f"📊 Batch classified {successful_count}/{len(request.tickets)} tickets")
        
        return BatchClassificationResponse(
            results=results,
            total_tickets=len(request.tickets),
            successful_classifications=successful_count,
            total_processing_time_ms=total_processing_time
        )
        
    except Exception as e:
        logger.error(f"❌ Batch classification error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch classification failed: {str(e)}")

@app.get("/categories")
async def get_supported_categories():
    """Get list of supported ticket categories."""
    categories = {
        "BILLING": "Account, payment, and billing issues",
        "TECHNICAL": "Network, connectivity, service problems",
        "SALES": "New services, upgrades, product inquiries", 
        "COMPLAINTS": "Service complaints, escalations",
        "NETWORK": "Infrastructure and network-related issues",
        "ACCOUNT": "Account management, profile changes"
    }
    
    return {
        "categories": categories,
        "total_categories": len(categories)
    }

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )