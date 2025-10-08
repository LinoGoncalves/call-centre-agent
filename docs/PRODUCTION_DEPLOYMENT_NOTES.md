# Production Deployment Notes for Confidence-Based Routing System

## 🚀 Production Readiness Status

### ✅ Completed Epic 1.16-1.20 Components
- **Confidence-Based Router**: Intelligent caching with configurable thresholds
- **Historical Accuracy Tracker**: PostgreSQL-compatible accuracy validation  
- **Structured Routing Logger**: JSON logging for analytics platforms
- **Production Performance Monitor**: Real-time KPIs and alerting
- **Production Dashboard**: Grafana/CloudWatch compatible metrics

## 🔧 Production Deployment Requirements

### 1. Database Configuration
**Current**: Mock PostgreSQL simulation
**Production Required**: Real PostgreSQL database

```sql
-- Required tables for production deployment
CREATE TABLE routing_history (
    id SERIAL PRIMARY KEY,
    ticket_id VARCHAR(255) UNIQUE,
    department VARCHAR(100),
    confidence DECIMAL(3,2),
    method VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    actual_outcome VARCHAR(100),
    resolution_time_hours DECIMAL(5,2),
    customer_satisfaction DECIMAL(3,1)
);

CREATE TABLE routing_accuracy (
    id SERIAL PRIMARY KEY,
    department VARCHAR(100),
    total_predictions INTEGER DEFAULT 0,
    correct_predictions INTEGER DEFAULT 0,
    accuracy_rate DECIMAL(5,4),
    last_updated TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_routing_history_department ON routing_history(department);
CREATE INDEX idx_routing_history_created_at ON routing_history(created_at);
```

**Environment Variables**:
```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432
POSTGRES_DB=call_centre_routing
POSTGRES_USER=your-username
POSTGRES_PASSWORD=your-password
```

### 2. Monitoring System Integration

#### Grafana Dashboard Configuration
**Metrics Export**: JSON format compatible with Prometheus/Grafana
**Key Panels**:
- Cache Hit Rate (target: ≥25%)
- Average Processing Time (target: ≤2000ms)
- Routing Distribution (Cached vs RAG-LLM vs Fallback)
- Confidence Distribution (High/Medium/Low)
- Alert Status and Recent Notifications

#### CloudWatch Integration (AWS)
**Custom Metrics**:
```python
# Example CloudWatch metrics push
import boto3
cloudwatch = boto3.client('cloudwatch')

cloudwatch.put_metric_data(
    Namespace='CallCentre/Routing',
    MetricData=[
        {
            'MetricName': 'CacheHitRate',
            'Value': cache_hit_rate,
            'Unit': 'Percent'
        },
        {
            'MetricName': 'ProcessingTime',
            'Value': avg_processing_time,
            'Unit': 'Milliseconds'
        }
    ]
)
```

#### ELK Stack Integration
**Logstash Configuration**:
```ruby
input {
  file {
    path => "/var/log/routing_decisions.log"
    codec => json
  }
}

filter {
  if [event_type] == "routing_decision" {
    mutate {
      add_tag => ["routing"]
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "routing-decisions-%{+YYYY.MM.dd}"
  }
}
```

### 3. Performance Optimization

#### Pinecone Configuration
**Production Settings**:
```python
# Production Pinecone configuration
PINECONE_CONFIG = {
    "api_key": os.getenv("PINECONE_API_KEY"),
    "environment": os.getenv("PINECONE_ENV", "us-west1-gcp"),
    "index_name": "call-centre-tickets-prod",
    "dimension": 768,  # Based on embedding model
    "metric": "cosine",
    "replicas": 2,  # For high availability
    "shards": 1
}
```

#### Caching Strategy
**Redis Configuration** (recommended for production caching):
```python
REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": int(os.getenv("REDIS_PORT", 6379)),
    "db": int(os.getenv("REDIS_DB", 0)),
    "password": os.getenv("REDIS_PASSWORD"),
    "socket_timeout": 5,
    "socket_connect_timeout": 5,
    "retry_on_timeout": True
}

# Cache configuration
CACHE_TTL = 3600  # 1 hour for routing decisions
```

### 4. Security Considerations

#### API Key Management
```bash
# Required environment variables
GOOGLE_API_KEY=your-gemini-api-key
PINECONE_API_KEY=your-pinecone-api-key
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# Optional monitoring integration keys
GRAFANA_API_KEY=your-grafana-key
CLOUDWATCH_ACCESS_KEY=your-aws-key
CLOUDWATCH_SECRET_KEY=your-aws-secret
```

#### Input Validation and Sanitization
**Already Implemented**:
- HTML sanitization in Streamlit UI
- SQL injection protection through parameterized queries
- Input length validation and content filtering

### 5. Scalability Configuration

#### Load Balancing
**Recommended Setup**:
- Multiple application instances behind load balancer
- Database connection pooling (recommended: 10-20 connections per instance)
- Redis cluster for distributed caching
- Separate read replicas for analytics queries

#### Auto-scaling Triggers
**CloudWatch Alarms**:
- CPU usage > 70%
- Memory usage > 80% 
- Average response time > 5 seconds
- Queue depth > 100 tickets

### 6. Monitoring and Alerting

#### Critical Alerts (Immediate Response Required)
- Cache hit rate drops below 15%
- Average processing time exceeds 10 seconds
- Database connection failures
- Pinecone API errors > 5%
- Memory usage > 90%

#### Warning Alerts (Monitor and Investigate)
- Cache hit rate below 25%
- Processing time exceeds 5 seconds
- Confidence distribution shifts (>30% low confidence)
- Accuracy rate drops below 85%

### 7. Deployment Checklist

#### Pre-Deployment
- [ ] PostgreSQL database provisioned and configured
- [ ] Pinecone production index created with proper dimensions
- [ ] Redis cache cluster configured (optional but recommended)
- [ ] Monitoring systems configured (Grafana/CloudWatch/ELK)
- [ ] Environment variables set in production environment
- [ ] Load balancer and auto-scaling groups configured
- [ ] Backup and disaster recovery procedures tested

#### Post-Deployment Validation
- [ ] Health check endpoints responding
- [ ] Database connections successful
- [ ] Pinecone integration functional
- [ ] Logging pipeline operational
- [ ] Monitoring dashboards populated with data
- [ ] Alert notifications functioning
- [ ] Performance baselines established

### 8. Rollback Plan

#### Immediate Rollback Triggers
- System availability < 99%
- Average response time > 15 seconds
- Database corruption detected
- Security breach identified

#### Rollback Procedure
1. Switch traffic to previous stable version
2. Preserve routing decision logs for analysis
3. Maintain database consistency during rollback
4. Validate system functionality post-rollback
5. Investigate and document root cause

## 📊 Expected Production Performance

### Baseline Metrics (Post-Deployment)
- **Cache Hit Rate**: 25-35% (after system learns from real data)
- **Average Processing Time**: 1.5-3.0 seconds for cached, 5-8 seconds for RAG-LLM
- **Accuracy Rate**: ≥90% (validated against historical outcomes)
- **Throughput**: 100-200 tickets/minute per instance
- **Availability**: 99.9% uptime target

### Performance Improvement Timeline
- **Week 1-2**: System learns patterns, cache hit rate reaches 20-25%
- **Month 1**: Cache hit rate stabilizes at 30-35%, accuracy >90%
- **Month 3**: Optimal performance achieved, potential for threshold tuning
- **Month 6**: Historical accuracy data enables advanced optimization

## 🔄 Continuous Improvement

### A/B Testing Framework
**Implement after 1 month of baseline data**:
- Test different confidence thresholds (85% vs 90%)
- Compare accuracy thresholds (80% vs 85% vs 90%)
- Evaluate impact of different similarity measures
- Test alternative LLM models for routing decisions

### Machine Learning Enhancements
**Future Considerations**:
- Fine-tune embedding models on routing-specific data
- Implement reinforcement learning for dynamic threshold adjustment
- Add customer satisfaction feedback loop to accuracy calculations
- Develop specialized models for different ticket categories

---

**Last Updated**: 2024-10-08  
**Epic**: 1.16-1.20 Confidence-Based Routing  
**Status**: Production Ready  
**Next Review**: Post-deployment Week 1