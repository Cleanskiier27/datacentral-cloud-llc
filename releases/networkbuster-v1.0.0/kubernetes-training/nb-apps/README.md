# NetworkBuster Applications

All NetworkBuster applications containerized and ready for Kubernetes deployment.

## 🔑 Security
**PIN**: drew2  
**Access Level**: Unlimited

## 📦 Applications

### 1. Services Manager (Port 8080)
Real-time Windows service monitoring and management tool with web UI.

**Features:**
- View all system services
- Start/Stop/Restart services
- Filter by status (Running/Stopped/Critical)
- Real-time statistics dashboard

**Endpoints:**
- `/` - Main dashboard
- `/api/services` - List all services
- `/api/services/{name}/start` - Start service
- `/api/services/{name}/stop` - Stop service
- `/api/services/{name}/restart` - Restart service
- `/health` - Health check

### 2. Robot Recycling (Port 5000)
Flask-based robot recycling management system with inventory tracking.

**Features:**
- Robot inventory management
- Task assignment system
- Material recycling tracking
- Dashboard with statistics

**Endpoints:**
- `/` - Web dashboard
- `/api/robots` - Robot CRUD operations
- `/api/tasks` - Task management
- `/api/inventory` - Inventory tracking
- `/health` - Health check

### 3. Sudo Manager (Port 8081)
PIN-based sudo permission lock/unlock system for WSL.

**Features:**
- Lock/unlock sudo permissions
- PIN verification (drew2)
- Security audit logging
- Emergency unlock functionality

**Endpoints:**
- `/api/lock` - Lock sudo permissions
- `/api/unlock` - Unlock sudo permissions
- `/api/status` - Check lock status
- `/api/logs` - View security logs
- `/health` - Health check

### 4. Status Dashboard (Port 8082)
Comprehensive system status monitoring with real-time metrics.

**Features:**
- CPU, Memory, Disk monitoring
- Network statistics
- Running services count
- Container status (if Docker available)

**Endpoints:**
- `/` - Dashboard UI
- `/api/system` - System metrics
- `/api/services` - Services status
- `/api/network` - Network info
- `/health` - Health check

### 5. Token Manager (Port 8083)
Authentication token generation and management system.

**Features:**
- JWT token generation
- Token validation and refresh
- Token revocation
- Secure storage

**Endpoints:**
- `/api/token/generate` - Generate new token
- `/api/token/validate` - Validate token
- `/api/token/refresh` - Refresh token
- `/api/token/revoke` - Revoke token
- `/health` - Health check

### 6. License Manager (Port 8084)
Personal use license management and verification.

**Features:**
- License generation
- Machine ID verification
- License validation
- Usage tracking

**Endpoints:**
- `/api/license/generate` - Generate license
- `/api/license/validate` - Validate license
- `/api/license/info` - License information
- `/health` - Health check

## 🐳 Docker Usage

### Build All Containers
```bash
cd E:\datacentral-cloud-llc\kubernetes-training\nb-apps
docker-compose build
```

### Start All Services
```bash
docker-compose up -d
```

### Stop All Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f services-manager
```

### Check Status
```bash
docker-compose ps
```

## ☸️ Kubernetes Deployment

### Deploy All Apps
```bash
kubectl apply -f ../manifests/namespace.yaml
kubectl apply -f ../manifests/deployments/
kubectl apply -f ../manifests/services/
```

### Check Deployment Status
```bash
kubectl get pods -n networkbuster
kubectl get svc -n networkbuster
```

### Access Services
```bash
# Port forward to access locally
kubectl port-forward svc/services-manager 8080:8080 -n networkbuster
kubectl port-forward svc/robot-recycling 5000:5000 -n networkbuster
```

## 🌐 Service URLs

When running with Docker Compose:
- **Services Manager**: http://localhost:8080
- **Robot Recycling**: http://localhost:5000
- **Sudo Manager**: http://localhost:8081
- **Status Dashboard**: http://localhost:8082
- **Token Manager**: http://localhost:8083
- **License Manager**: http://localhost:8084
- **Nginx Proxy**: http://localhost

## 🔧 Configuration

All services use environment variables for configuration:

```bash
SECURITY_PIN=drew2
APP_NAME=<service-name>
LOG_LEVEL=INFO
```

## 📊 Monitoring

All services expose metrics on `/metrics` endpoint for Prometheus scraping.

### Prometheus Configuration
```yaml
scrape_configs:
  - job_name: 'networkbuster-apps'
    static_configs:
      - targets:
        - 'services-manager:8080'
        - 'robot-recycling:5000'
        - 'sudo-manager:8081'
        - 'status-dashboard:8082'
        - 'token-manager:8083'
        - 'license-manager:8084'
```

## 🔐 Security Notes

- All services require PIN authentication: **drew2**
- HTTPS enabled via Nginx proxy
- Secrets stored in Kubernetes secrets
- Non-root containers
- Read-only root filesystems where possible

## 🚀 Quick Commands

```bash
# Build and start all
docker-compose up -d --build

# Restart specific service
docker-compose restart services-manager

# Scale service (Kubernetes)
kubectl scale deployment services-manager --replicas=3 -n networkbuster

# View logs (Docker)
docker-compose logs -f services-manager

# View logs (Kubernetes)
kubectl logs -f deployment/services-manager -n networkbuster
```

## 📝 Development

Each app directory contains:
- `Dockerfile` - Container build instructions
- `requirements.txt` or `package.json` - Dependencies
- `config/` - Configuration files
- `src/` - Source code
- `tests/` - Unit tests

## 🔄 Updates

To update an app:
1. Make code changes in app directory
2. Rebuild container: `docker-compose build <service-name>`
3. Restart service: `docker-compose up -d <service-name>`
4. For Kubernetes: `kubectl rollout restart deployment/<service-name> -n networkbuster`

---

**NetworkBuster Cloud Management System**  
*All Apps | Kubernetes Ready | PIN: drew2*
