# NetworkBuster Kubernetes Training

Complete Kubernetes training environment with all NetworkBuster applications containerized and ready for deployment.

## 🎯 Overview

This directory contains all NetworkBuster applications configured for Kubernetes deployment, including:
- Containerized microservices
- Kubernetes manifests
- Helm charts
- CI/CD pipelines
- Monitoring and logging configurations

## 🔑 Security

- **PIN**: drew2
- **Access**: Unlimited
- **Authorization**: Personal use license

## 📁 Directory Structure

```
kubernetes-training/
├── nb-apps/                    # All NetworkBuster applications
│   ├── services-manager/       # Services management tool
│   ├── robot-recycling/        # Robot recycling app
│   ├── sudo-manager/           # Sudo permission manager
│   ├── status-dashboard/       # System status dashboard
│   ├── token-manager/          # Token management
│   └── license-manager/        # License management
├── manifests/                  # Kubernetes YAML manifests
│   ├── deployments/
│   ├── services/
│   ├── ingress/
│   └── configmaps/
├── helm-charts/                # Helm chart packages
├── ci-cd/                      # CI/CD pipeline configs
├── monitoring/                 # Prometheus, Grafana configs
└── docs/                       # Training documentation
```

## 🚀 Quick Start

### Prerequisites
- MicroK8s v1.32.9 installed
- kubectl configured
- Docker for containerization

### Deploy All Apps
```bash
cd kubernetes-training
kubectl apply -f manifests/
```

### Deploy via Docker Compose (amd64 + arm64, desktop launcher)
```bash
cd kubernetes-training/nb-apps
chmod +x install.sh
./install.sh
```
Builds all 6 services for `linux/amd64` and `linux/arm64`, starts the stack with
the `nginx` reverse proxy on plain HTTP (port 80, suitable for local/private
network hosting), and installs a `networkbuster.desktop` launcher pointing at it.

### Deploy Individual App
```bash
kubectl apply -f manifests/deployments/services-manager.yaml
```

## 📚 Training Modules

### Module 1: Basics
- Understanding Pods and Containers
- Deployments and ReplicaSets
- Services and Networking

### Module 2: Configuration
- ConfigMaps and Secrets
- Environment Variables
- Volume Mounts

### Module 3: Advanced
- StatefulSets
- DaemonSets
- Jobs and CronJobs

### Module 4: Production
- Ingress Controllers
- Monitoring with Prometheus
- Logging with ELK Stack
- Autoscaling (HPA/VPA)

## 🔧 NetworkBuster Apps

### 1. Services Manager (services-manager)
- **Description**: Real-time service monitoring
- **Port**: 8080
- **Type**: Web UI
- **Path**: `/nb-apps/services-manager`

### 2. Robot Recycling (robot-recycling)
- **Description**: Robot management system
- **Port**: 5000
- **Type**: Flask API
- **Path**: `/nb-apps/robot-recycling`

### 3. Sudo Manager (sudo-manager)
- **Description**: Permission management
- **Port**: 8081
- **Type**: Security Service
- **Path**: `/nb-apps/sudo-manager`

### 4. Status Dashboard (status-dashboard)
- **Description**: System monitoring
- **Port**: 8082
- **Type**: Dashboard UI
- **Path**: `/nb-apps/status-dashboard`

### 5. Token Manager (token-manager)
- **Description**: Authentication tokens
- **Port**: 8083
- **Type**: Security API
- **Path**: `/nb-apps/token-manager`

### 6. License Manager (license-manager)
- **Description**: Personal licensing
- **Port**: 8084
- **Type**: Security Service
- **Path**: `/nb-apps/license-manager`

## 🐳 Docker Commands

### Build All Images
```bash
cd kubernetes-training/nb-apps
docker-compose build
```

### Push to Registry
```bash
docker tag nb-services-manager:latest registry.local/nb-services-manager:latest
docker push registry.local/nb-services-manager:latest
```

## ☸️ Kubernetes Commands

### View All Pods
```bash
kubectl get pods -n networkbuster
```

### View Services
```bash
kubectl get svc -n networkbuster
```

### View Logs
```bash
kubectl logs -f deployment/services-manager -n networkbuster
```

### Scale Deployment
```bash
kubectl scale deployment/services-manager --replicas=3 -n networkbuster
```

## 🔍 Monitoring

### Prometheus
- **URL**: http://localhost:9090
- **Metrics**: All NB apps exposed on `/metrics`

### Grafana
- **URL**: http://localhost:3000
- **Dashboards**: Pre-configured for all apps

## 📖 Documentation

- [Kubernetes Official Docs](https://kubernetes.io/docs/)
- [MicroK8s Documentation](https://microk8s.io/docs)
- [Helm Documentation](https://helm.sh/docs/)

## 🔐 Security Best Practices

1. Use Secrets for sensitive data
2. Enable RBAC (Role-Based Access Control)
3. Network Policies for pod isolation
4. Regular security scans with tools like Trivy
5. Keep images updated and minimal

## 📝 Notes

- All applications are configured with health checks
- Auto-restart policies enabled
- Resource limits defined for production use
- PIN-based authentication: **drew2**

## 🆘 Support

For issues or questions:
- Review logs: `kubectl logs <pod-name>`
- Check events: `kubectl get events`
- Describe resources: `kubectl describe <resource> <name>`

---

**NetworkBuster Cloud Management System**  
*Unlimited Access | Personal Use License*  
🔑 PIN: drew2
