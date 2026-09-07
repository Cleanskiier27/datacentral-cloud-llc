# 📖 NetworkBuster - Master Project Index & Quick Navigation

**Complete Reference Guide**

> Adapted from the source `DOCS-m2m` documentation set. Links below point to
> the subset of documents migrated into this repository under `docs/`. Items
> not migrated (e.g. cost/budget breakdowns, KQL query catalogs, and other
> point-in-time reports) are noted as such and were intentionally excluded —
> see the migration plan for rationale.

---

## 🎯 Quick Start (5 Minutes)

### For Developers
1. Read: [DEPLOYMENT_DASHBOARD.md](../deployment/DEPLOYMENT_DASHBOARD.md) - System overview
2. Deploy: see [deployment guides](../deployment/)

### For Operations/DevOps
1. Read: [AZURE_STORAGE_SETUP.md](../deployment/AZURE_STORAGE_SETUP.md) - Infrastructure
2. See: [AZURE_STORAGE_READY.md](../deployment/AZURE_STORAGE_READY.md) - Quick reference

## 📚 Complete Documentation Map

### 📊 Strategic Docs

| Document | Purpose | Audience |
|----------|---------|----------|
| [DEPLOYMENT_DASHBOARD.md](../deployment/DEPLOYMENT_DASHBOARD.md) | System overview, capabilities, roadmap | All stakeholders |
| [PROJECT-SUMMARY.md](PROJECT-SUMMARY.md) | Project vision & key achievements | Leadership |

### 🏗️ Infrastructure & DevOps Docs

| Document | Purpose | Audience |
|----------|---------|----------|
| [AZURE_STORAGE_SETUP.md](../deployment/AZURE_STORAGE_SETUP.md) | Azure Storage deployment guide | DevOps, Backend |
| [AZURE_STORAGE_READY.md](../deployment/AZURE_STORAGE_READY.md) | Quick reference for storage setup | DevOps |
| [DEPLOYMENT-REFERENCE-CARD.md](../deployment/DEPLOYMENT-REFERENCE-CARD.md) | Deployment quick reference | DevOps |
| [DEPLOYMENT_READINESS_MANIFEST.md](../deployment/DEPLOYMENT_READINESS_MANIFEST.md) | Readiness checklist | DevOps |
| [HYPERV-LINUX-SETUP.md](../deployment/HYPERV-LINUX-SETUP.md) | Hyper-V on Linux setup | DevOps |
| [HYPERV-QUICK-START.md](../deployment/HYPERV-QUICK-START.md) | Hyper-V quick start | DevOps |
| [DOCKER-TROUBLESHOOTING.md](../deployment/DOCKER-TROUBLESHOOTING.md) | Docker troubleshooting | DevOps |

### 🌐 Networking Docs

| Document | Purpose | Audience |
|----------|---------|----------|
| [DNS-A-RECORD-SETUP.md](../networking/DNS-A-RECORD-SETUP.md) | DNS A record setup | DevOps |
| [CUSTOM-DOMAIN-SETUP.md](../networking/CUSTOM-DOMAIN-SETUP.md) | Custom domain setup | DevOps |
| [DOMAIN-CONFIGURATION-STATUS.md](../networking/DOMAIN-CONFIGURATION-STATUS.md) | Domain configuration status | DevOps |
| [DOMAIN-SETUP-SUMMARY.md](../networking/DOMAIN-SETUP-SUMMARY.md) | Domain setup summary | DevOps |
| [VERCEL-DOMAIN-SETUP-GUIDE.md](../networking/VERCEL-DOMAIN-SETUP-GUIDE.md) | Vercel domain setup | DevOps |
| [DUAL-ROUTER-SETUP-GUIDE.md](../networking/DUAL-ROUTER-SETUP-GUIDE.md) | Dual-router networking | Networking |
| [NETWORK_PROXY_GUIDE.md](../networking/NETWORK_PROXY_GUIDE.md) | Network proxy configuration | Networking |

### 🤖 AI/ML & Feature Docs

| Document | Purpose | Audience |
|----------|---------|----------|
| [AI_TRAINING_PIPELINE_SETUP.md](../AI_TRAINING_PIPELINE_SETUP.md) | Complete ML infrastructure guide | Data Scientists, Backend |
| [AUDIO-STREAMING-GUIDE.md](../AUDIO-STREAMING-GUIDE.md) | Audio streaming feature guide | Frontend |
| [MOBILE_SETUP.md](../MOBILE_SETUP.md) | Mobile setup guide | Mobile/Frontend |

### 🔧 Reference Docs

| Document | Purpose | Audience |
|----------|---------|----------|
| [DEPENDENCIES.md](DEPENDENCIES.md) | Installation & dependency reference | All developers |
| [DEV_ENVIRONMENT.md](DEV_ENVIRONMENT.md) | Unified development environment guide | All developers |
| [WORKSPACE_GUIDE.md](WORKSPACE_GUIDE.md) | Workspace/project structure guide | All developers |

> **Not migrated** (point-in-time reports, cost/budget breakdowns, and
> analytics query catalogs specific to the source project — see the
> migration plan for full exclusion rationale): `BUDGET_AND_DETAILS.md`,
> `KQL_ANALYTICS_QUERIES.md`, `IMMERSIVE_READER_INTEGRATION.md`,
> `DATA_STORAGE_AND_VISITOR_TRACKING.md`, `D_DRIVE_BACKUP_SUMMARY.md`,
> `PUSH-DATACENTRA.md`.

---

## 🗂️ Documentation Directory Layout (this repository)

```
docs/
├── deployment/     # Deployment & infrastructure setup guides
├── networking/     # Domain / DNS / networking guides
├── reference/      # Core architecture / project reference (this file, DEPENDENCIES.md, DEV_ENVIRONMENT.md, WORKSPACE_GUIDE.md, PROJECT-SUMMARY.md)
├── AI_TRAINING_PIPELINE_SETUP.md
├── AUDIO-STREAMING-GUIDE.md
├── MOBILE_SETUP.md
└── ... (existing repository docs, e.g. matrix-arch-linux.md, moonbase-alpha/)
```

---

**Master Index Version**: 1.0 (migrated)
**Source**: `Cleanskiier27/DOCS-m2m`
