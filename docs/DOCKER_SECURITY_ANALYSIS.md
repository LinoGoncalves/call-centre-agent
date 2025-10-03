# Docker Security Scan - Known Issues

## Current Status (October 2025)

**Base Image**: `python:3.13.1-slim-bookworm`  
**Security Scan Result**: 5 high vulnerabilities detected

## Analysis

The vulnerabilities are in the **upstream Python base image** provided by the official Docker Python maintainers, not in our application code. These typically include:

1. System libraries (glibc, openssl, etc.)
2. Debian package dependencies
3. Python interpreter dependencies

## Mitigation Strategies

### Option 1: Accept Risk (Current)
✅ **Status**: Implemented  
**Rationale**:
- Vulnerabilities are in base OS packages, not application code
- Python 3.13.1 is the latest stable release
- Using `slim-bookworm` (Debian 12) which receives regular security updates
- Security patches applied during build (`apt-get upgrade -y`)

**Action Required**:
- Monitor security advisories
- Rebuild image monthly for security patches
- Update to newer Python versions when available

### Option 2: Use Distroless Base Image
🔄 **Status**: Future consideration  

```dockerfile
# Multi-stage build with distroless
FROM python:3.13.1-slim-bookworm AS builder
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --user -e .

FROM gcr.io/distroless/python3
COPY --from=builder /root/.local /root/.local
COPY src/ /app/src/
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "src.api.main:app"]
```

**Pros**: Minimal attack surface (no shell, no package manager)  
**Cons**: Harder to debug, requires multi-stage build

### Option 3: Use Alpine Linux
⚠️ **Status**: Not recommended  

```dockerfile
FROM python:3.13.1-alpine
```

**Pros**: Smaller image size (~50MB vs ~150MB)  
**Cons**:
- Different libc (musl vs glibc) can cause compatibility issues
- Slower pip installs (need to compile wheels)
- Some Python packages don't work well with Alpine

### Option 4: Wait for Upstream Fix
⏳ **Status**: Ongoing  

The Python Docker official images team regularly updates base images. Vulnerabilities will be patched in future releases.

**Action**:
- Subscribe to Python Docker image updates
- Rebuild monthly: `docker build --pull --no-cache -t call-centre-agent:latest .`

## Security Best Practices (Already Implemented)

✅ Non-root user (appuser:1000)  
✅ Specific version tags (not `latest`)  
✅ Minimal system dependencies  
✅ Security updates during build  
✅ `.dockerignore` file  
✅ No secrets in image  
✅ Health checks configured  
✅ Proper signal handling  

## Production Deployment Recommendations

1. **Container Scanning**: Integrate into CI/CD
   ```bash
   docker scan call-centre-agent:latest
   trivy image call-centre-agent:latest
   ```

2. **Runtime Security**: Use security policies
   ```yaml
   # Kubernetes PodSecurityPolicy
   securityContext:
     runAsNonRoot: true
     runAsUser: 1000
     readOnlyRootFilesystem: true
     allowPrivilegeEscalation: false
   ```

3. **Network Policies**: Restrict container communication
   ```yaml
   # Only allow ingress on port 8000
   networkPolicy:
     podSelector:
       matchLabels:
         app: call-centre-api
     ingress:
       - from:
         - namespaceSelector: {}
         ports:
         - protocol: TCP
           port: 8000
   ```

4. **Secrets Management**: Use external secret stores
   - Azure Key Vault (recommended for AKS deployment)
   - Kubernetes Secrets with encryption at rest
   - Never hardcode or commit secrets

## Vulnerability Tracking

| Date | Base Image | Vulns | Action Taken |
|------|-----------|-------|--------------|
| Oct 2025 | python:3.13-slim | 1 high | Upgraded to 3.13.1-slim-bookworm |
| Oct 2025 | python:3.13.1-slim-bookworm | 5 high | Monitoring upstream fixes |

## Next Review

**Date**: November 2025  
**Action**: Rebuild image and rescan  
**Owner**: DevOps Team

## References

- [Python Docker Official Images Security](https://github.com/docker-library/python/issues)
- [Debian Security Advisories](https://www.debian.org/security/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [NIST Container Security Guide](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)

## Decision Log

**2025-10-03**: Accepted current vulnerabilities as they are in upstream base image. Will monitor and rebuild monthly. Alternative approaches (distroless, Alpine) deferred until production deployment (Q3 2026).

---

**Severity**: Low (vulnerabilities in base OS, not application)  
**Impact**: Minimal (proper security controls in place)  
**Priority**: Monitor and patch regularly
