# Docker Image Pull Fix Guide
# Client troubleshooting for PostgreSQL image error

## Error: unable to get image 'postgres:15-alpine': unexpected end of JSON input

### Quick Fix Steps (Run these in order):

## Step 1: Clean Docker Cache
```bash
# Stop all containers first
docker-compose -f docker-compose.secure.yml down

# Clean Docker system
docker system prune -a -f

# Remove any corrupted images
docker rmi postgres:15-alpine 2>/dev/null || echo "Image not found locally"

# Clear Docker build cache
docker builder prune -a -f
```

## Step 2: Test Docker Hub Connectivity
```bash
# Test if Docker Hub is accessible
docker pull hello-world

# If this fails, you have network/proxy issues
# If this succeeds, try pulling PostgreSQL manually
docker pull postgres:15-alpine
```

## Step 3: Alternative PostgreSQL Image (if Step 2 fails)

### AUTOMATED FIX (RECOMMENDED):
```bash
# Run the automated fix script
fix-postgres-error.bat
```
This script will:
- Test multiple PostgreSQL images automatically
- Create a working docker-compose file
- Start your services with the working image

### MANUAL FIX:
```bash
# Try different PostgreSQL image tags
docker pull postgres:15
docker pull postgres:14-alpine
docker pull postgres:13-alpine
```

Then use the backup configurations in `docker-compose-postgres-alternatives.yml`

## Step 4: Rebuild with Clean State
```bash
# Start fresh with no cache
docker-compose -f docker-compose.secure.yml build --no-cache --pull

# Then start services
docker-compose -f docker-compose.secure.yml up
```

## Alternative Solution: Use Different PostgreSQL Version

If postgres:15-alpine continues to fail, we can modify the configuration:

### Option A: Use postgres:15 (without alpine)
1. Edit docker-compose.secure.yml
2. Change: `image: postgres:15-alpine`
3. To: `image: postgres:15`

### Option B: Use postgres:14-alpine
1. Edit docker-compose.secure.yml  
2. Change: `image: postgres:15-alpine`
3. To: `image: postgres:14-alpine`

Both alternatives provide the same functionality with different base images.

## Corporate Network Solutions

If you're behind a corporate firewall:

### Configure Docker Proxy
```bash
# Create or edit ~/.docker/config.json
{
  "proxies": {
    "default": {
      "httpProxy": "http://your-proxy:port",
      "httpsProxy": "http://your-proxy:port"
    }
  }
}
```

### Use Internal Registry (if available)
Ask your IT team if there's an internal Docker registry with PostgreSQL images.

## Verification Steps
```bash
# After fixing, verify all images can be pulled:
docker pull python:3.13.1-slim-bookworm
docker pull redis:7-alpine  
docker pull postgres:15-alpine

# If all succeed, run the build:
docker-compose -f docker-compose.secure.yml up --build
```