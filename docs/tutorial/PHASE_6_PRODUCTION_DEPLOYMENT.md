# Phase 6: Production Deployment & Operations

**Estimated Time**: 8-10 hours  
**Prerequisites**: Phases 1-5 completed, tested system  
**File References**:
- `Dockerfile` (52 lines)
- `docker-compose.yml` (91 lines)
- `.env.example`

---

## Overview

Phase 6 covers **production deployment** strategies for ML systems. This goes beyond "getting it running"—we cover containerization, cloud deployment, monitoring, logging, scaling, security hardening, and operational procedures for a production-grade AI system.

### What You'll Learn

- Docker containerization for ML applications
- Multi-stage builds for optimized images
- Cloud deployment (Azure, AWS, GCP)
- Kubernetes orchestration patterns
- CI/CD pipelines for ML systems
- Monitoring and observability (Prometheus, Grafana)
- Logging strategies (structured logging, centralized aggregation)
- Security hardening (secrets management, network policies)
- Scaling strategies (horizontal/vertical, auto-scaling)
- Operational procedures (rollbacks, blue-green deployments)

---

## Containerization with Docker

### Why Containerization for ML?

**Traditional Deployment Challenges:**
- "Works on my machine" syndrome
- Dependency conflicts (Python packages, system libraries)
- Environment drift between dev/staging/prod
- Difficult rollbacks
- Inconsistent configurations

**Container Benefits:**
- Immutable infrastructure (same container everywhere)
- Isolated dependencies (no conflicts)
- Fast deployments (pull image, run)
- Easy rollbacks (switch to previous image tag)
- Resource limits (CPU, memory constraints)

---

### Dockerfile Deep Dive

**File**: `Dockerfile` (52 lines)

#### Base Image Selection

**Line 2**:
```dockerfile
FROM python:3.13-slim
```

**Design Decision: `slim` vs `full` vs `alpine`**

| Image Type | Size | Use Case | Trade-offs |
|------------|------|----------|------------|
| `python:3.13` | ~1GB | Development, debugging | Includes gcc, many tools |
| `python:3.13-slim` | ~150MB | Production (our choice) | Minimal tools, faster builds |
| `python:3.13-alpine` | ~50MB | Ultra-minimal | Incompatible with some ML libraries |

**Why `slim`?**
- scikit-learn, pandas need compiled extensions (incompatible with alpine's musl libc)
- 150MB is acceptable for production
- Faster pull times than full image
- Includes essential tools

#### Working Directory and Environment

**Lines 5-11**:
```dockerfile
WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```

**Environment Variables Explained:**

**`PYTHONPATH=/app`**:
- Tells Python where to find modules
- Allows `from src.models import classifier` to work
- Alternative: Install as package with `pip install -e .`

**`PYTHONDONTWRITEBYTECODE=1`**:
- Prevents `.pyc` file generation
- Reduces container size
- `.pyc` files are build-time artifacts, not needed at runtime

**`PYTHONUNBUFFERED=1`**:
- Forces stdout/stderr to be unbuffered
- **Critical for logging**: See logs immediately, not buffered
- Without this, logs might be lost if container crashes

#### Layer Optimization

**Lines 18-23**:
```dockerfile
# Copy requirements first for better caching
COPY pyproject.toml ./
COPY requirements.txt* ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .
```

**Docker Layer Caching Strategy:**

Docker caches each instruction. If a layer hasn't changed, it reuses the cached version.

**Order Matters:**
1. Copy `pyproject.toml` first (changes rarely)
2. Install dependencies (expensive, ~2-3 minutes)
3. Copy application code last (changes frequently)

**Result:** Code changes don't trigger dependency reinstall. Builds drop from 3 minutes to 10 seconds.

**Alternative Pattern** (explicit requirements):
```dockerfile
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

**`--no-cache-dir` Explanation:**
- pip normally caches downloaded packages in `~/.cache/pip`
- In containers, this cache is wasted space (never reused)
- Saves ~200MB in image size

#### Security: Non-Root User

**Lines 26-33**:
```dockerfile
# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy application code
COPY src/ ./src/
COPY models/ ./models/

# Set proper permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser
```

**Why Not Run as Root?**

**Security Principle**: Least Privilege

If container is compromised:
- **Root container**: Attacker can install packages, modify system files, potentially escape container
- **Non-root container**: Attacker limited to application permissions

**Real-World Impact:**
- Many Kubernetes clusters **enforce** non-root policies (PodSecurityPolicy)
- Security scanners flag root containers as high-risk
- Compliance requirements (PCI-DSS, HIPAA) often mandate non-root

**Commands Explained:**
- `groupadd -r appuser`: Create system group (`-r` = system account, no login)
- `useradd -r -g appuser appuser`: Create system user in that group
- `chown -R appuser:appuser /app`: Give ownership of `/app` to appuser
- `USER appuser`: Switch to non-root user for remaining commands

#### Health Checks

**Lines 36-38**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

**Health Check Pattern:**

Kubernetes/Docker uses health checks to determine if container is healthy.

**Parameters:**
- `--interval=30s`: Check every 30 seconds
- `--timeout=30s`: Health check must complete in 30s
- `--start-period=5s`: Wait 5s before first check (app startup time)
- `--retries=3`: Mark unhealthy after 3 consecutive failures

**Why This Matters:**
- Unhealthy containers are automatically restarted
- Load balancers stop sending traffic to unhealthy instances
- Monitoring systems alert on health check failures

**Health Endpoint Requirements:**
```python
# src/api/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration."""
    try:
        # Verify model loads
        from src.models.enhanced_classifier import GeminiEnhancedClassifier
        classifier = GeminiEnhancedClassifier()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )
```

#### Multi-Stage Build Pattern

**Advanced Optimization** (not in current Dockerfile, but production-ready):

```dockerfile
# Build stage
FROM python:3.13-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy and install dependencies
COPY pyproject.toml ./
RUN pip install --user --no-cache-dir -e .

# Runtime stage
FROM python:3.13-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY models/ ./models/

# Add .local/bin to PATH
ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Benefits:**
- Build dependencies (gcc, make) not in final image
- Reduces image size by ~300MB
- Faster deployments (smaller image to pull)
- More secure (fewer attack surfaces)

---

### Docker Compose for Local Development

**File**: `docker-compose.yml` (91 lines)

#### Service Architecture

**Lines 6-30**: Main API service
```yaml
services:
  ticket-classifier-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: telco-ticket-classifier
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
      - LOG_LEVEL=info
      - MODEL_PATH=/app/models/ticket_classifier_model.pkl
    volumes:
      - ./models:/app/models:ro
      - ./data:/app/data:ro
      - ./logs:/app/logs
```

**Volume Mounts Explained:**

**`./models:/app/models:ro`**:
- Mount host `./models` to container `/app/models`
- `:ro` = read-only (security best practice)
- **Why**: Allows model updates without rebuilding image
- **Production**: Use cloud storage (S3, Azure Blob) instead

**`./logs:/app/logs`**:
- Mount logs directory for persistence
- Logs survive container restarts
- **Production**: Use log aggregation (CloudWatch, Stackdriver)

**Port Mapping**: `8000:8000`
- Host port 8000 maps to container port 8000
- Access API at `http://localhost:8000`

#### Redis Caching Service

**Lines 33-43**:
```yaml
redis-cache:
  image: redis:7-alpine
  container_name: telco-ticket-redis
  ports:
    - "6379:6379"
  networks:
    - ticket-classifier-network
  restart: unless-stopped
  command: redis-server --appendonly yes
  volumes:
    - redis-data:/data
```

**Why Redis for ML API?**

**Use Case: Response Caching**

Same ticket classified multiple times = wasted API calls to Gemini.

**Cache Strategy:**
```python
import redis
import hashlib
import json

class CachedClassifier:
    def __init__(self):
        self.classifier = GeminiEnhancedClassifier()
        self.cache = redis.Redis(host='redis-cache', port=6379, db=0)
        self.ttl = 3600  # 1 hour cache
    
    def classify_ticket(self, ticket_text: str):
        # Generate cache key
        cache_key = f"classify:{hashlib.sha256(ticket_text.encode()).hexdigest()}"
        
        # Check cache
        cached = self.cache.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # Cache miss - classify
        result = self.classifier.classify_ticket(ticket_text)
        
        # Store in cache
        self.cache.setex(cache_key, self.ttl, json.dumps(result.dict()))
        
        return result
```

**Benefits:**
- Reduces Gemini API costs (fewer calls)
- Faster response times (cache hit: <5ms vs API call: 1-2s)
- Handles duplicate requests efficiently

**Redis Configuration:**
- `--appendonly yes`: Enables persistence (AOF mode)
- Survives container restarts
- Trade-off: Slightly slower writes for durability

#### Networking

**Docker Networks** allow containers to communicate:

```yaml
networks:
  ticket-classifier-network:
    driver: bridge
```

**Service Discovery:**
- Container `ticket-classifier-api` can reach Redis at `redis-cache:6379`
- Docker DNS resolves service names to container IPs
- Isolated from host network (security)

---

## Cloud Deployment Strategies

### Azure Deployment

#### Azure Container Instances (Simplest)

**Step 1: Build and Push Image**
```bash
# Login to Azure Container Registry
az acr login --name telcoclassifier

# Build image
docker build -t telcoclassifier.azurecr.io/ticket-classifier:v1.0 .

# Push to registry
docker push telcoclassifier.azurecr.io/ticket-classifier:v1.0
```

**Step 2: Deploy Container Instance**
```bash
az container create \
  --resource-group telco-rg \
  --name ticket-classifier \
  --image telcoclassifier.azurecr.io/ticket-classifier:v1.0 \
  --cpu 2 \
  --memory 4 \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label telco-classifier \
  --ports 8000 \
  --environment-variables \
    GOOGLE_API_KEY=$GOOGLE_API_KEY \
    LOG_LEVEL=info
```

**Benefits:**
- Simple deployment (single command)
- Pay-per-second pricing
- Fast startup (<30s)

**Limitations:**
- No auto-scaling
- No load balancing (single instance)
- Not suitable for high-traffic production

#### Azure Kubernetes Service (Production)

**Kubernetes Deployment Manifest** (`k8s/deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ticket-classifier
  labels:
    app: ticket-classifier
spec:
  replicas: 3  # Run 3 pods for high availability
  selector:
    matchLabels:
      app: ticket-classifier
  template:
    metadata:
      labels:
        app: ticket-classifier
    spec:
      containers:
      - name: classifier
        image: telcoclassifier.azurecr.io/ticket-classifier:v1.0
        ports:
        - containerPort: 8000
        env:
        - name: GOOGLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: gemini-api-key
              key: api-key
        - name: LOG_LEVEL
          value: "info"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"  # 1 CPU core
          limits:
            memory: "4Gi"
            cpu: "2000m"  # 2 CPU cores max
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ticket-classifier-service
spec:
  selector:
    app: ticket-classifier
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ticket-classifier-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ticket-classifier
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**Kubernetes Concepts Explained:**

**Deployment**:
- Manages pod lifecycle
- Handles rolling updates
- Ensures desired replica count

**Service**:
- Load balances traffic across pods
- Provides stable endpoint (even as pods restart)
- Type `LoadBalancer` creates cloud load balancer

**HorizontalPodAutoscaler (HPA)**:
- Automatically scales pods based on metrics
- CPU > 70% or Memory > 80% → add pods
- Traffic drops → remove pods (down to 3 minimum)

**Resource Requests vs Limits**:
- **Requests**: Guaranteed resources (Kubernetes schedules based on this)
- **Limits**: Maximum allowed (pod killed if exceeded)

**Deploy to AKS:**
```bash
# Create AKS cluster
az aks create \
  --resource-group telco-rg \
  --name telco-aks \
  --node-count 3 \
  --enable-managed-identity \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group telco-rg --name telco-aks

# Create secret for API key
kubectl create secret generic gemini-api-key \
  --from-literal=api-key=$GOOGLE_API_KEY

# Deploy application
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods
kubectl get services
kubectl logs -f deployment/ticket-classifier
```

---

### AWS Deployment

#### ECS Fargate (Serverless Containers)

**Task Definition** (`ecs-task-definition.json`):

```json
{
  "family": "ticket-classifier",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "classifier",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/ticket-classifier:v1.0",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "LOG_LEVEL",
          "value": "info"
        }
      ],
      "secrets": [
        {
          "name": "GOOGLE_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:gemini-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ticket-classifier",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "classifier"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

**Deploy to ECS:**
```bash
# Create ECR repository
aws ecr create-repository --repository-name ticket-classifier

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Build and push image
docker build -t ticket-classifier:v1.0 .
docker tag ticket-classifier:v1.0 123456789.dkr.ecr.us-east-1.amazonaws.com/ticket-classifier:v1.0
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ticket-classifier:v1.0

# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Create ECS service
aws ecs create-service \
  --cluster telco-cluster \
  --service-name ticket-classifier-service \
  --task-definition ticket-classifier \
  --desired-count 3 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-abc123],securityGroups=[sg-abc123],assignPublicIp=ENABLED}"
```

---

## Monitoring and Observability

### Prometheus Metrics

**Instrument Application** (`src/api/main.py`):

```python
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import FastAPI, Response
import time

app = FastAPI()

# Metrics
classification_counter = Counter(
    'ticket_classifications_total',
    'Total number of ticket classifications',
    ['category', 'sentiment']
)

classification_latency = Histogram(
    'ticket_classification_duration_seconds',
    'Time spent classifying tickets',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

gemini_api_calls = Counter(
    'gemini_api_calls_total',
    'Total calls to Gemini API',
    ['status']  # success, error, timeout
)

@app.post("/classify")
async def classify_ticket(ticket: TicketRequest):
    """Classify a support ticket with metrics."""
    start_time = time.time()
    
    try:
        result = classifier.classify_ticket(ticket.text)
        
        # Record metrics
        classification_counter.labels(
            category=result.predicted_category,
            sentiment=result.sentiment_label
        ).inc()
        
        gemini_api_calls.labels(status='success').inc()
        
        return result
    
    except Exception as e:
        gemini_api_calls.labels(status='error').inc()
        raise
    
    finally:
        # Record latency
        duration = time.time() - start_time
        classification_latency.observe(duration)

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type="text/plain")
```

**Prometheus Configuration** (`prometheus.yml`):

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'ticket-classifier'
    static_configs:
      - targets: ['ticket-classifier-api:8000']
    metrics_path: '/metrics'
```

**Grafana Dashboard**:

Key visualizations:
- **Request rate**: Classifications per minute
- **Latency percentiles**: p50, p95, p99
- **Error rate**: Failed classifications
- **Category distribution**: BILLING, TECHNICAL, etc.
- **Sentiment distribution**: POSITIVE, NEGATIVE, CRITICAL
- **Gemini API health**: Success rate, latency

---

### Structured Logging

**Logging Configuration** (`src/utils/logging_config.py`):

```python
import logging
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields."""
    
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        # Add standard fields
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        
        # Add context if available
        if hasattr(record, 'ticket_id'):
            log_record['ticket_id'] = record.ticket_id
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id

def setup_logging():
    """Configure structured logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Console handler with JSON format
    handler = logging.StreamHandler()
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(logger)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Usage
logger = setup_logging()

@app.post("/classify")
async def classify_ticket(ticket: TicketRequest):
    """Classify ticket with structured logging."""
    ticket_id = generate_ticket_id()
    
    logger.info(
        "Classification started",
        extra={
            'ticket_id': ticket_id,
            'ticket_length': len(ticket.text),
            'user_id': ticket.user_id
        }
    )
    
    try:
        result = classifier.classify_ticket(ticket.text)
        
        logger.info(
            "Classification completed",
            extra={
                'ticket_id': ticket_id,
                'category': result.predicted_category,
                'confidence': result.confidence,
                'processing_time_ms': result.processing_time_ms
            }
        )
        
        return result
    
    except Exception as e:
        logger.error(
            "Classification failed",
            extra={
                'ticket_id': ticket_id,
                'error': str(e),
                'error_type': type(e).__name__
            },
            exc_info=True
        )
        raise
```

**Benefits of Structured Logging:**
- Machine-readable (easy to parse, search, aggregate)
- Consistent format across services
- Rich context (ticket_id, user_id, timing)
- Cloud-native (CloudWatch, Stackdriver parse JSON natively)

---

## Security Hardening

### Secrets Management

**Never Hardcode Secrets:**

❌ **Bad**:
```python
GOOGLE_API_KEY = "AIzaSyC..."  # NEVER DO THIS
```

✅ **Good** (Environment Variables):
```python
import os
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")
```

✅ **Better** (Cloud Secrets Manager):

**Azure Key Vault:**
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://telco-keyvault.vault.azure.net/", credential=credential)

GOOGLE_API_KEY = client.get_secret("gemini-api-key").value
```

**AWS Secrets Manager:**
```python
import boto3

client = boto3.client('secretsmanager', region_name='us-east-1')
response = client.get_secret_value(SecretId='gemini-api-key')
GOOGLE_API_KEY = response['SecretString']
```

### Network Security

**Kubernetes Network Policies** (`k8s/network-policy.yaml`):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ticket-classifier-netpol
spec:
  podSelector:
    matchLabels:
      app: ticket-classifier
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: api-gateway
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: redis-cache
    ports:
    - protocol: TCP
      port: 6379
  - to:  # Allow Gemini API calls
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
```

**What This Does:**
- Only API Gateway can connect to classifier (ingress)
- Classifier can only connect to Redis and external HTTPS (egress)
- Prevents lateral movement in cluster

---

## Operational Procedures

### Rolling Updates (Zero-Downtime)

**Kubernetes Deployment Strategy:**

```yaml
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Create 1 extra pod during update
      maxUnavailable: 0  # Never have fewer than 3 pods
```

**Update Process:**
1. Build new image: `v1.1`
2. Update deployment: `kubectl set image deployment/ticket-classifier classifier=image:v1.1`
3. Kubernetes creates 1 new pod (v1.1)
4. Once healthy, terminates 1 old pod (v1.0)
5. Repeats until all pods updated

**Result**: Always 3-4 pods running, zero downtime.

### Blue-Green Deployment

**Setup:**
1. Deploy v2 (green) alongside v1 (blue)
2. Test green environment
3. Switch traffic: update Service selector from `version: blue` to `version: green`
4. Monitor for issues
5. If problems: instant rollback (switch back to blue)

**Kubernetes Manifests:**

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ticket-classifier-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ticket-classifier
      version: blue
  template:
    metadata:
      labels:
        app: ticket-classifier
        version: blue
    spec:
      containers:
      - name: classifier
        image: telcoclassifier.azurecr.io/ticket-classifier:v1.0
---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ticket-classifier-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ticket-classifier
      version: green
  template:
    metadata:
      labels:
        app: ticket-classifier
        version: green
    spec:
      containers:
      - name: classifier
        image: telcoclassifier.azurecr.io/ticket-classifier:v2.0
---
# Service (controls traffic routing)
apiVersion: v1
kind: Service
metadata:
  name: ticket-classifier-service
spec:
  selector:
    app: ticket-classifier
    version: blue  # Change to 'green' to switch traffic
  ports:
  - port: 80
    targetPort: 8000
```

**Switch Traffic:**
```bash
kubectl patch service ticket-classifier-service -p '{"spec":{"selector":{"version":"green"}}}'
```

**Rollback:**
```bash
kubectl patch service ticket-classifier-service -p '{"spec":{"selector":{"version":"blue"}}}'
```

---

## Validation Checkpoint

Before considering Phase 6 complete, verify:

- [ ] Dockerfile builds successfully
- [ ] Docker Compose stack runs locally
- [ ] Health check endpoint returns 200 OK
- [ ] Container runs as non-root user
- [ ] Image size under 500MB (reasonable for ML)
- [ ] Cloud deployment successful (AKS or ECS)
- [ ] Kubernetes HPA scales pods correctly
- [ ] Prometheus metrics being collected
- [ ] Structured logs visible in cloud logging
- [ ] Secrets managed via cloud service (not env vars)
- [ ] Network policies restrict traffic
- [ ] Rolling update completes without downtime
- [ ] Blue-green deployment switches successfully
- [ ] Load balancer distributes traffic evenly
- [ ] Auto-scaling triggers on load

---

## Key Takeaways

1. **Containerization** provides consistency across environments
2. **Multi-stage builds** reduce image size significantly
3. **Non-root containers** are critical for security
4. **Health checks** enable self-healing infrastructure
5. **Kubernetes** provides production-grade orchestration
6. **HPA** automatically scales based on demand
7. **Prometheus metrics** enable observability
8. **Structured logging** makes debugging possible at scale
9. **Secrets management** prevents credential leaks
10. **Blue-green deployments** enable risk-free updates

Production deployment isn't about getting the code running—it's about building reliable, secure, scalable infrastructure that can handle real-world load, failures, and change.

**System Complete!** You now have a production-ready AI classification system deployed with enterprise-grade infrastructure.
