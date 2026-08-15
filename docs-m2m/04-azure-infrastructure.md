# Page 4: Azure Infrastructure

## ☁️ Complete Azure Deployment Architecture

---

## 📊 Resource Overview

**Deployment Status:** ✅ IN PROGRESS  
**Resource Group:** networkbuster-rg  
**Location:** eastus  
**Total Resources:** 3 (Base Infrastructure)

---

## 🗂️ Resource Hierarchy

```
Subscription: Azure subscription 1 (cdb580bc-e2e9-4866-aac2-aa86f0a25cb3)
│
└── Resource Group: networkbuster-rg (eastus)
    │
    ├── 📦 Container Registry
    │   ├── Name: networkbusterlo25gft5nqwzg
    │   ├── SKU: Basic
    │   ├── Type: Microsoft.ContainerRegistry/registries
    │   └── Status: Active
    │
    ├── 📊 Log Analytics Workspace
    │   ├── Name: networkbuster-logs
    │   ├── Retention: 30 days
    │   ├── Type: Microsoft.OperationalInsights/workspaces
    │   └── Status: Active
    │
    ├── 🎯 Container App Environment
    │   ├── Name: networkbuster-env
    │   ├── Type: Microsoft.App/managedEnvironments
    │   ├── Logging: Log Analytics integration
    │   └── Status: Active
    │
    ├── ⚙️ Container App: networkbuster-server (Pending)
    │   ├── Image: networkbuster-server:latest
    │   ├── CPU: 0.5 cores
    │   ├── Memory: 1Gi
    │   ├── Port: 3000
    │   ├── Replicas: 1-5 (autoscaled)
    │   └── Status: ⏳ Awaiting deployment
    │
    └── ⚙️ Container App: networkbuster-overlay (Pending)
        ├── Image: networkbuster-overlay:latest
        ├── CPU: 0.25 cores
        ├── Memory: 0.5Gi
        ├── Port: 3000
        ├── Replicas: 1-3 (autoscaled)
        └── Status: ⏳ Awaiting deployment
```

---

## 🏗️ Bicep Templates

### Main Template: `infra/main.bicep`

**Purpose:** Deploy base infrastructure

**Resources Created:**
1. **Container Registry**
   - Type: `Microsoft.ContainerRegistry/registries@2023-07-01`
   - SKU: Basic
   - Admin User: Enabled
   - Public Access: Enabled

2. **Log Analytics Workspace**
   - Type: `Microsoft.OperationalInsights/workspaces@2022-10-01`
   - SKU: PerGB2018
   - Retention: 30 days

3. **Container App Environment**
   - Type: `Microsoft.App/managedEnvironments@2023-11-02-preview`
   - Logging: Connected to Log Analytics

**Outputs:**
```
containerRegistryLoginServer: networkbusterlo25gft5nqwzg.azurecr.io
containerRegistryName: networkbusterlo25gft5nqwzg
containerAppEnvId: /subscriptions/.../networkbuster-env
containerAppEnvName: networkbuster-env
logAnalyticsId: /subscriptions/.../networkbuster-logs
resourceGroupName: networkbuster-rg
```

### Container Apps Template: `infra/container-apps.bicep`

**Purpose:** Deploy application containers

**Services:**

#### 1. Main Server Container App
```yaml
Name: networkbuster-server
Image: networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:latest
Resources:
  CPU: 0.5 cores
  Memory: 1Gi
Ingress:
  External: true
  Port: 3000
  HTTPS: Required
Scaling:
  Min Replicas: 1
  Max Replicas: 5
Environment Variables:
  NODE_ENV: production
  PORT: 3000
```

#### 2. Overlay UI Container App
```yaml
Name: networkbuster-overlay
Image: networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:latest
Resources:
  CPU: 0.25 cores
  Memory: 0.5Gi
Ingress:
  External: true
  Port: 3000
  HTTPS: Required
Scaling:
  Min Replicas: 1
  Max Replicas: 3
Environment Variables:
  NODE_ENV: production
  PORT: 3000
```

---

## 📋 Parameters Configuration

**File:** `infra/parameters.json`

```json
{
  "location": "eastus",
  "projectName": "networkbuster"
}
```

---

## 🚀 Deployment Workflow

### Step 1: Deploy Base Infrastructure
```powershell
az deployment group create `
  --resource-group networkbuster-rg `
  --template-file infra/main.bicep `
  --parameters infra/parameters.json
```

**Status:** ✅ COMPLETED

### Step 2: Build Docker Images
```bash
# Main Server
docker build -t networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:latest -f Dockerfile .

# Overlay UI
docker build -t networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:latest -f challengerepo/real-time-overlay/Dockerfile ./challengerepo/real-time-overlay
```

**Status:** ⏳ PENDING (Docker required)

### Step 3: Push Images to ACR
```bash
docker push networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:latest
docker push networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:latest
```

**Status:** ⏳ PENDING (After Step 2)

### Step 4: Deploy Container Apps
```powershell
az deployment group create `
  --resource-group networkbuster-rg `
  --template-file infra/container-apps.bicep `
  --parameters infra/parameters.json
```

**Status:** ⏳ PENDING (After image push)

---

## 📊 Resource Specifications

### Container Registry Specification
```
SKU: Basic (Lowest cost tier)
Storage: 10 GB included
Request Units: 100 per day

Limitations:
- No webhooks
- No tasks support
- No anonymous access
- No managed identities

Upgrade Path:
- Standard: 100 GB storage, auto-scale
- Premium: 500 GB, advanced features
```

### Log Analytics Workspace
```
SKU: PerGB2018 (Pay-as-you-go)
Retention: 30 days (default)

Data Types Captured:
- Container logs
- Event logs
- Performance metrics
- Network traces

Pricing Estimate:
- First 5GB/month: Free
- Additional: ~$2.30/GB
```

### Container App Environment
```
Managed Infrastructure:
- Auto-managed Kubernetes (hidden)
- VNet integration (optional)
- Private endpoints (optional)

Scaling:
- HTTP-based auto-scaling
- CPU/Memory-based scaling
- Custom metric scaling

Networking:
- Internal: Private communication
- External: Public ingress
- Environment-level DNS
```

---

## 🔐 Security Configuration

### Network Security
- ✅ Ingress: HTTPS only
- ✅ External traffic: Allowed
- ✅ Internal communication: Private VNet
- ✅ Health probes: Enabled

### Identity & Access
- ✅ System-assigned managed identity: Enabled
- ✅ Registry authentication: Admin user + secrets
- ✅ RBAC: Ready for configuration
- ✅ Key Vault: Ready for integration

### Monitoring
- ✅ Log Analytics: Connected
- ✅ Application Insights: Ready
- ✅ Diagnostics: Enabled
- ✅ Metrics: Available

---

## 💰 Cost Estimation

### Base Infrastructure (Monthly)
| Resource | Tier | Estimated Cost |
|----------|------|-----------------|
| Container Registry | Basic | $5.00 |
| Log Analytics | PerGB2018 | $2.30-10.00 |
| Container Apps | Pay-per-use | $10-30 |
| **Total** | | **$17-45** |

### With Full Load
| Resource | Configuration | Cost |
|----------|---------------|------|
| Main Server | 0.5 CPU, 1GB RAM | $20-25/month |
| Overlay UI | 0.25 CPU, 0.5GB RAM | $10-15/month |
| Registry Storage | 20GB images | $8/month |
| Log Analytics | 50GB/month data | $115/month |
| **Total** | **Full Production** | **$150-160/month** |

---

## 📈 Scaling & Performance

### Auto-scaling Configuration

**Main Server (networkbuster-server)**
```
Min Replicas: 1
Max Replicas: 5
Scale Trigger: HTTP requests > 1000 RPS
Scale-up Time: ~60 seconds
Scale-down Time: ~300 seconds
```

**Overlay UI (networkbuster-overlay)**
```
Min Replicas: 1
Max Replicas: 3
Scale Trigger: HTTP requests > 500 RPS
Scale-up Time: ~60 seconds
Scale-down Time: ~300 seconds
```

### Performance Targets
```
Main Server:
  Availability: 99.95%
  Response Time: <200ms (p95)
  Throughput: >1000 requests/sec

Overlay UI:
  Availability: 99.90%
  Response Time: <500ms (p95)
  Throughput: >500 requests/sec
```

---

## 🔄 Deployment Validation

### Pre-Deployment Checklist
- [x] Resource group created
- [x] Base infrastructure deployed
- [x] Registry configured
- [x] Log Analytics connected
- [x] Bicep templates validated
- [ ] Docker images built
- [ ] Images pushed to registry
- [ ] Container apps deployed
- [ ] Health checks passing
- [ ] Monitoring configured

### Post-Deployment Validation
- Endpoint connectivity
- Container health status
- Log collection verification
- Scaling behavior
- Security group rules
- DNS resolution

---

## 📝 Deployment Commands Reference

### Create Resource Group
```bash
az group create --name networkbuster-rg --location eastus
```

### Deploy Base Infrastructure
```bash
az deployment group create \
  --resource-group networkbuster-rg \
  --template-file infra/main.bicep \
  --parameters infra/parameters.json
```

### Build Docker Images
```bash
# Server
docker build -t networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:latest -f Dockerfile .

# Overlay
docker build -t networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:latest \
  -f challengerepo/real-time-overlay/Dockerfile \
  ./challengerepo/real-time-overlay
```

### Push to Registry
```bash
az acr login --name networkbusterlo25gft5nqwzg
docker push networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-server:latest
docker push networkbusterlo25gft5nqwzg.azurecr.io/networkbuster-overlay:latest
```

### Deploy Container Apps
```bash
az deployment group create \
  --resource-group networkbuster-rg \
  --template-file infra/container-apps.bicep \
  --parameters infra/parameters.json
```

---

**[← Back to Index](./00-index.md) | [Next: Page 5 →](./05-cicd-pipelines.md)**
