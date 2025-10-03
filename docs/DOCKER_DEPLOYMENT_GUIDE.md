# Docker Deployment Guide

## Overview

This guide covers building, running, and deploying the Call Centre AI Agent using Docker containers.

## Security Improvements (Latest Update)

The Dockerfile has been enhanced with the following security best practices:

✅ **Specific Base Image**: `python:3.13.1-slim-bookworm` (was `python:3.13-slim`)
- Uses Debian 12 (Bookworm) for better security patching
- Specific version tag prevents unexpected changes

✅ **Security Hardening**:
- Runs as non-root user (`appuser:1000`)
- Minimal system dependencies
- Automatic security updates during build
- No shell access for app user (`/sbin/nologin`)

✅ **Build Optimization**:
- Multi-layer caching for faster builds
- Removed build dependencies after installation
- `.dockerignore` file prevents sensitive data leakage

✅ **Production-Ready Configuration**:
- Health checks every 30s
- Proper signal handling (exec form CMD)
- Proxy headers for reverse proxy compatibility
- Logging configuration

## Prerequisites

- Docker Desktop 4.0+ or Docker Engine 20.10+
- Docker Compose 2.0+ (optional)
- `.env` file with `GOOGLE_API_KEY`

## Quick Start

### 1. Build the Docker Image

```bash
# Build with default tag
docker build -t call-centre-agent:latest .

# Build with specific version
docker build -t call-centre-agent:1.0.0 .

# Build with build args (if needed)
docker build --build-arg PYTHON_VERSION=3.13.1 -t call-centre-agent:latest .
```

### 2. Run the Container

#### Basic Run
```bash
docker run -d \
  --name call-centre-api \
  -p 8000:8000 \
  -e GOOGLE_API_KEY="your-api-key-here" \
  call-centre-agent:latest
```

#### Run with Environment File
```bash
docker run -d \
  --name call-centre-api \
  -p 8000:8000 \
  --env-file .env \
  call-centre-agent:latest
```

#### Run with Volume Mounts (Development)
```bash
docker run -d \
  --name call-centre-api \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/models:/app/models:ro \
  -v $(pwd)/data:/app/data:ro \
  -v $(pwd)/logs:/app/logs \
  call-centre-agent:latest
```

### 3. Using Docker Compose

#### Start All Services
```bash
# Start in background
docker compose up -d

# Start with logs
docker compose up

# Build and start
docker compose up --build
```

#### Stop Services
```bash
# Stop containers
docker compose stop

# Stop and remove containers
docker compose down

# Stop and remove volumes
docker compose down -v
```

## Development Workflow

### 1. Local Development with Hot Reload

```bash
# Override CMD for development
docker run -it \
  --name call-centre-dev \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/src:/app/src \
  call-centre-agent:latest \
  uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Interactive Shell Access

```bash
# Get shell in running container
docker exec -it call-centre-api /bin/bash

# Run one-off command
docker exec call-centre-api python -c "import sys; print(sys.version)"
```

### 3. View Logs

```bash
# Follow logs
docker logs -f call-centre-api

# Last 100 lines
docker logs --tail 100 call-centre-api

# With timestamps
docker logs -t call-centre-api
```

### 4. Health Checks

```bash
# Check container health status
docker inspect --format='{{.State.Health.Status}}' call-centre-api

# Manual health check
curl http://localhost:8000/health
```

## Production Deployment

### 1. Multi-Stage Build (Future Enhancement)

For smaller production images, consider multi-stage builds:

```dockerfile
# Builder stage
FROM python:3.13.1-slim-bookworm AS builder
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --user -e .

# Runtime stage
FROM python:3.13.1-slim-bookworm
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "src.api.main:app"]
```

### 2. Container Registry

#### Push to Docker Hub
```bash
# Tag image
docker tag call-centre-agent:latest yourusername/call-centre-agent:1.0.0

# Login
docker login

# Push
docker push yourusername/call-centre-agent:1.0.0
```

#### Push to Azure Container Registry (ACR)
```bash
# Login to ACR
az acr login --name yourregistry

# Tag for ACR
docker tag call-centre-agent:latest yourregistry.azurecr.io/call-centre-agent:1.0.0

# Push
docker push yourregistry.azurecr.io/call-centre-agent:1.0.0
```

### 3. Kubernetes Deployment (Q3 2026 Roadmap)

See `BACKLOG.md` Epic 6 for full AKS deployment plan.

Basic Kubernetes manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: call-centre-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: call-centre-api
  template:
    metadata:
      labels:
        app: call-centre-api
    spec:
      containers:
      - name: api
        image: yourregistry.azurecr.io/call-centre-agent:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: GOOGLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: google-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 40
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs call-centre-api

# Inspect container
docker inspect call-centre-api

# Check if port is already in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac
```

### Permission Errors

```bash
# Ensure files are readable (on Linux/Mac)
chmod -R 755 src/ models/ data/

# Check container user
docker exec call-centre-api whoami
```

### Out of Memory

```bash
# Check resource usage
docker stats call-centre-api

# Increase memory limit
docker run -m 2g call-centre-agent:latest
```

### Image Too Large

```bash
# Check image size
docker images call-centre-agent

# View image layers
docker history call-centre-agent:latest

# Remove build cache
docker builder prune
```

## Security Best Practices

1. ✅ **Never commit `.env` files** - Use secrets management
2. ✅ **Scan images regularly** - Use `docker scan call-centre-agent:latest`
3. ✅ **Keep base images updated** - Rebuild monthly for security patches
4. ✅ **Use specific version tags** - Avoid `latest` in production
5. ✅ **Run as non-root** - Already configured in Dockerfile
6. ✅ **Minimize attack surface** - Use slim base images
7. ✅ **Enable Docker Content Trust** - `export DOCKER_CONTENT_TRUST=1`

## Performance Optimization

### Build Cache Optimization
```bash
# Use BuildKit for better caching
DOCKER_BUILDKIT=1 docker build -t call-centre-agent:latest .
```

### Runtime Performance
```bash
# Limit resources
docker run -d \
  --cpus="2.0" \
  --memory="2g" \
  --memory-swap="2g" \
  call-centre-agent:latest
```

### Network Optimization
```bash
# Use host network (Linux only, faster but less isolation)
docker run --network host call-centre-agent:latest
```

## Monitoring and Observability

### Prometheus Metrics
```bash
# Access metrics endpoint
curl http://localhost:8000/metrics
```

### Container Stats
```bash
# Real-time stats
docker stats call-centre-api

# Export stats
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

## References

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Python Docker Official Images](https://hub.docker.com/_/python)
- [Azure Container Registry](https://azure.microsoft.com/en-us/services/container-registry/)
- Project ROADMAP.md - Epic 6: Cloud Deployment & Scaling
- Project BACKLOG.md - Kubernetes deployment tasks

## Next Steps

1. Review `ROADMAP.md` for production deployment timeline
2. Set up CI/CD pipeline (GitHub Actions) for automated builds
3. Configure Azure Container Registry
4. Plan AKS cluster setup (Q3 2026)
5. Implement canary deployments (BACKLOG task 3.15)

---

**Last Updated**: October 2025  
**Docker Version**: 24.0+  
**Base Image**: python:3.13.1-slim-bookworm
