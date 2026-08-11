# Page 6: Docker Configuration

## 🐳 Container Images & Configuration

---

## 📋 Docker Overview

**Total Dockerfiles:** 2  
**Base Images:** Alpine Node.js 24  
**Registry:** Azure Container Registry  
**Build Strategy:** Multi-stage (optimized)

---

## 1️⃣ Main Server Dockerfile

**Location:** `Dockerfile` (Root)  
**Purpose:** Express.js API server containerization

### File Contents
```dockerfile
# Build stage
FROM node:24-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:24-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Security: Non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
RUN chown -R nodejs:nodejs /app
USER nodejs

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

CMD ["node", "server.js"]
```

### Specifications
```
Base Image: node:24-alpine
Build Type: Multi-stage
Final Size: ~200MB (estimated)
User: nodejs (UID 1001)
Port: 3000
Health Check: Every 30 seconds
```

### Environment
```
NODE_ENV: production
PORT: 3000
```

### Build Command
```bash
docker build -t networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:latest -f Dockerfile .
```

### Run Command (Local Testing)
```bash
docker run -p 3000:3000 \
  -e NODE_ENV=production \
  networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:latest
```

### Health Check URL
```
http://localhost:3000/health
Expected Response: 200 OK
```

---

## 2️⃣ Overlay UI Dockerfile

**Location:** `challengerepo/real-time-overlay/Dockerfile`  
**Purpose:** React + Vite application containerization

### File Contents
```dockerfile
# Build stage
FROM node:24-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:24-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist

# Security: Non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["serve", "-s", "dist", "-l", "3000"]
```

### Specifications
```
Base Image: node:24-alpine
Build Type: Multi-stage
Build Tool: Vite
Final Size: ~150MB (estimated)
User: nodejs (UID 1001)
Port: 3000
Health Check: Every 30 seconds
Serve Tool: serve package (global)
```

### Build Command
```bash
docker build -t networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:latest \
  -f Dockerfile \
  ./challengerepo/real-time-overlay
```

### Run Command (Local Testing)
```bash
docker run -p 3000:3000 \
  networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:latest
```

### Health Check URL
```
http://localhost:3000/
Expected Response: 200 OK (HTML content)
```

---

## 📦 .dockerignore File

**Purpose:** Exclude files from Docker build context

### Recommended Content
```
.git
.gitignore
node_modules
dist
build
npm-debug.log
.env
.env.local
.DS_Store
coverage
.vscode
.idea
*.log
docs
README.md
```

### Build Optimization
- Reduces context size by ~80%
- Faster builds
- Smaller layer sizes
- Security: Excludes sensitive files

---

## 🔐 Image Security

### Alpine Base Image Benefits
- **Size:** ~50MB vs 500MB+ for full Node
- **Attack Surface:** Minimal
- **Scanning:** Limited CVEs
- **Performance:** Fast startup
- **Cost:** Smaller deployments

### Security Best Practices Implemented
- [x] Non-root user (nodejs:1001)
- [x] Multi-stage build (production-only dependencies)
- [x] Health checks configured
- [x] Read-only where possible
- [x] No secrets in image
- [x] Minimal base image

### Security Improvements Needed
- [ ] Image scanning (Trivy)
- [ ] Vulnerability assessment
- [ ] Registry scanning enabled
- [ ] Signed images
- [ ] Private repository

---

## 🏗️ Image Build Workflow

### Step 1: Build Locally
```bash
# Main Server
docker build -t networkbuster-server:latest -f Dockerfile .

# Overlay UI
docker build -t networkbuster-overlay:latest \
  -f challengerepo/real-time-overlay/Dockerfile \
  ./challengerepo/real-time-overlay
```

### Step 2: Tag for Registry
```bash
docker tag networkbuster-server:latest \
  networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:latest

docker tag networkbuster-server:latest \
  networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:v1.0.0

docker tag networkbuster-overlay:latest \
  networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:latest

docker tag networkbuster-overlay:latest \
  networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:v1.0.0
```

### Step 3: Login to ACR
```bash
az acr login --name networkbusterlo25gft5nqwzg
```

### Step 4: Push to Registry
```bash
docker push networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:latest
docker push networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:v1.0.0

docker push networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:latest
docker push networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:v1.0.0
```

### Step 5: Verify in Registry
```bash
az acr repository list --name networkbusterlo25gft5nqwzg
az acr repository show-tags --name networkbusterlo25gft5nqwzg --repository networkbuster-server
az acr repository show-tags --name networkbusterlo25gft5nqwzg --repository networkbuster-overlay
```

---

## 📊 Image Specifications

### Main Server Image
```
Name: networkbuster-server
Tags: latest, v1.0.0, {git-sha}
Repository: networkbusterlo25gft5nqwzg.azurecr.io
Size: ~200MB
Layers: 8-10
Compression: Alpine optimization
Base: node:24-alpine
Entrypoint: node server.js
Healthcheck: /health endpoint
```

### Overlay UI Image
```
Name: networkbuster-overlay
Tags: latest, v1.0.0, {git-sha}
Repository: networkbusterlo25gft5nqwzg.azurecr.io
Size: ~150MB
Layers: 9-11
Compression: Alpine optimization
Base: node:24-alpine
Entrypoint: serve dist
Healthcheck: Root path GET
```

---

## 🔄 Local Testing

### Test Main Server
```bash
# Build
docker build -t test-server -f Dockerfile .

# Run
docker run --rm -p 3000:3000 test-server

# Test
curl http://localhost:3000/health
curl http://localhost:3000/api
```

### Test Overlay UI
```bash
# Build
docker build -t test-overlay -f challengerepo/real-time-overlay/Dockerfile challengerepo/real-time-overlay

# Run
docker run --rm -p 3000:3000 test-overlay

# Test
curl http://localhost:3000
```

### Docker Compose (Optional)
```yaml
version: '3.8'
services:
  server:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
  
  overlay:
    build:
      context: ./challengerepo/real-time-overlay
      dockerfile: Dockerfile
    ports:
      - "3001:3000"
    environment:
      NODE_ENV: production
```

---

## 📈 Image Analysis

### Layer Breakdown (Server)
```
Layer 1: Alpine base        (~50MB)
Layer 2: Node.js            (~150MB)
Layer 3: npm dependencies   (~40MB)
Layer 4: App code           (~10MB)
Layer 5: Security setup     (<1MB)
Total: ~250MB
```

### Optimization Opportunities
- [ ] Use distroless base (save ~100MB)
- [ ] Minify application code
- [ ] Remove dev dependencies early
- [ ] Use cache mount for npm
- [ ] Parallel layer downloads

---

## 🚀 Deployment in Azure

### Container Apps Configuration
```yaml
Main Server:
  Image: networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:latest
  CPU: 0.5 cores
  Memory: 1Gi
  Port: 3000
  Replicas: 1-5

Overlay UI:
  Image: networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:latest
  CPU: 0.25 cores
  Memory: 0.5Gi
  Port: 3000
  Replicas: 1-3
```

### Image Pull Policy
- Always: Latest version on each start
- IfNotPresent: Use cached version
- Never: Use only cached

### Registry Authentication
```
Registry: networkbusterlo25gft5nqwzg.azurecr.io
Username: networkbusterlo25gft5nqwzg
Password: [Managed secret]
Auth Method: Admin user (not recommended for production)
```

---

## 📝 Registry Management

### List Images
```bash
az acr repository list --name networkbusterlo25gft5nqwzg
```

### Delete Images
```bash
az acr repository delete --name networkbusterlo25gft5nqwzg --image networkbuster-server:old-tag
```

### Get Image Details
```bash
az acr repository show --name networkbusterlo25gft5nqwzg --image networkbuster-server:latest
```

### Purge Old Images
```bash
az acr purge --name networkbusterlo25gft5nqwzg --filter 'networkbuster-server:.*' --ago 30d
```

---

**[← Back to Index](./00-index.md) | [Next: Page 7 →](./07-git-hooks.md)**
