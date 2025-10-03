# Dockerfile for Telco Call Centre Ticket Classification API
# Using specific version tag for security and reproducibility
FROM python:3.13.1-slim-bookworm

# Set metadata labels
LABEL maintainer="Call Centre Team"
LABEL version="1.0"
LABEL description="AI-powered ticket classification and routing system"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies and security updates
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create non-root user early for better security
RUN groupadd -r appuser --gid=1000 && \
    useradd -r -g appuser --uid=1000 --home-dir=/app --shell=/sbin/nologin appuser

# Copy requirements first for better layer caching
COPY --chown=appuser:appuser pyproject.toml ./
COPY --chown=appuser:appuser requirements.txt* ./

# Install Python dependencies with security flags
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -e . && \
    # Remove build dependencies to reduce image size
    apt-get purge -y --auto-remove build-essential

# Copy application code with proper ownership
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser models/ ./models/
COPY --chown=appuser:appuser data/ ./data/

# Switch to non-root user
USER appuser

# Health check with more robust configuration
HEALTHCHECK --interval=30s \
    --timeout=10s \
    --start-period=40s \
    --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port (documentation only, actual binding happens at runtime)
EXPOSE 8000

# Use exec form for proper signal handling
CMD ["uvicorn", "src.api.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--log-level", "info", \
     "--access-log", \
     "--proxy-headers", \
     "--forwarded-allow-ips", "*"]
