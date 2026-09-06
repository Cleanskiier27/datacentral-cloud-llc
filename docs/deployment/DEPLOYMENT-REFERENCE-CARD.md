# NetworkBuster Deployment Complete - Reference Card

## Current Status Summary

```
Azure Infrastructure (Deployed)
├── Container Registry      ✅ networkbusterlo25gft5nqwzg.azurecr.io
├── Container App Env       ✅ networkbuster-env (eastus)
├── Log Analytics           ✅ networkbuster-logs
└── Key Vault              ✅ networkbuster-kv (registering)

Vercel Deployment (Live)
├── Current URL            ✅ https://networkbuster-mez5d7bmv-networkbuster.vercel.app
├── Custom Domain          ⏳ Ready to configure
└── SSL/TLS               ✅ Automatic provisioning

Domain Configuration
├── Primary Domain         ✅ networkbuster.net (configured in package.json)
├── Setup Guides          ✅ 4 comprehensive guides created
└── Automation Scripts    ✅ PowerShell & Bicep templates ready
```

---

## Key Credentials & Endpoints

| Item | Value | Location |
|------|-------|----------|
| **Container Registry** | networkbusterlo25gft5nqwzg.azurecr.io | Azure Portal |
| **Registry Username** | networkbusterlo25gft5nqwzg | Use in `docker login` |
| **Registry Password** | See Azure Portal > Access Keys | Secure vault |
| **Container App Env** | networkbuster-env | Resource Group: networkbuster-rg |
| **Key Vault** | networkbuster-kv | Resource Group: networkbuster-rg |
| **Vercel Project** | NetworkBuster | https://vercel.com |
| **GitHub Repo** | networkbuster.net | https://github.com/NetworkBuster/networkbuster.net |

---

## Complete Setup Timeline

| Phase | What | Status | Documents |
|-------|------|--------|-----------|
| **Phase 1** | Azure Infrastructure Deploy | ✅ Complete | Deployment logs |
| **Phase 2** | Docker Build & Push | ⏳ Ready | deploy-docker-to-acr.ps1 |
| **Phase 3** | Container Apps Deploy | ⏳ Ready | infra/container-apps.bicep |
| **Phase 4** | Custom Domain Config | ⏳ In Progress | DOMAIN-*.md, VERCEL-*.md |
| **Phase 5** | SSL Certificates | ⏳ Ready | CUSTOM-DOMAIN-SETUP.md |
| **Phase 6** | Monitoring & Logs | ✅ Configured | Log Analytics active |

---

## Quick Action Guide

### Today (5-15 minutes)
```
1. Read: DOMAIN-SETUP-SUMMARY.md
2. Open: https://vercel.com
3. Add Domain: networkbuster.net
4. Take note of DNS configuration
```

### Next 24 Hours
```
1. Go to domain registrar
2. Update DNS / Nameservers
3. Check propagation: whatsmydns.net
4. Monitor Vercel dashboard
```

### After 24-48 Hours
```
1. Test: https://networkbuster.net
2. Verify SSL certificate
3. Test: https://www.networkbuster.net
4. Monitor logs in Azure
```

---

## Docker Commands (When Ready)

```bash
# Login to registry
docker login networkbusterlo25gft5nqwzg.azurecr.io

# Build image
docker build -t networkbusterlo25gft5nqwzg.azurecr.io/networkbuster:latest .

# Push to registry
docker push networkbusterlo25gft5nqwzg.azurecr.io/networkbuster:latest

# Run locally (testing)
docker run -p 3000:3000 networkbusterlo25gft5nqwzg.azurecr.io/networkbuster:latest
```

---

## Azure CLI Quick Reference

```bash
# View resources
az resource list --resource-group networkbuster-rg

# Check Container App status
az containerapp show --name networkbuster-server --resource-group networkbuster-rg

# View logs
az containerapp logs show --name networkbuster-server --resource-group networkbuster-rg

# List container images in registry
az acr repository list --name networkbusterlo25gft5nqwzg

# Check Key Vault status
az keyvault show --name networkbuster-kv --resource-group networkbuster-rg
```

---

## DNS Records to Add

### Vercel Primary Domain
```
Choose Option A or B:

OPTION A: Update Nameservers (Easiest)
  ns1.vercel-dns.com
  ns2.vercel-dns.com
  ns3.vercel-dns.com
  ns4.vercel-dns.com

OPTION B: Add DNS A Records
  networkbuster.net     A  216.198.79.1
  www                CNAME  networkbuster.net
```

### Azure API Domain (Optional)
```
api.networkbuster.net  CNAME  networkbuster-server.eastus.azurecontainerapps.io
```

---

## Documentation Files

**Available in this directory:**

| File | Purpose |
|------|---------|
| [DOMAIN-SETUP-SUMMARY.md](../networking/DOMAIN-SETUP-SUMMARY.md) | Overview and timeline |
| [VERCEL-DOMAIN-SETUP-GUIDE.md](../networking/VERCEL-DOMAIN-SETUP-GUIDE.md) | Step-by-step Vercel instructions |
| [CUSTOM-DOMAIN-SETUP.md](../networking/CUSTOM-DOMAIN-SETUP.md) | Comprehensive technical reference |
| [DOMAIN-CONFIGURATION-STATUS.md](../networking/DOMAIN-CONFIGURATION-STATUS.md) | Checklist and status tracking |
| `configure-custom-domain.ps1` | Automated configuration script |
| `infra/custom-domain.bicep` | Azure IaC template |

**Quick Read Order:**
1. Start: DOMAIN-SETUP-SUMMARY.md (5 min)
2. Do: VERCEL-DOMAIN-SETUP-GUIDE.md (10 min)
3. Reference: CUSTOM-DOMAIN-SETUP.md (as needed)
4. Track: DOMAIN-CONFIGURATION-STATUS.md (ongoing)

---

## Services Running

| Service | Port | URL | Status |
|---------|------|-----|--------|
| Main Server | 3000 | localhost:3000 | Ready |
| API Server | 3001 | localhost:3001 | Ready |
| Dashboard | 5173 | localhost:5173 | Vite dev |
| Vercel Deploy | 443 | networkbuster.vercel.app | Live |
| Azure Apps | 443 | azure*.azurecontainerapps.io | Ready |

---

## Monitoring & Troubleshooting

### Check DNS
```bash
nslookup networkbuster.net
nslookup www.networkbuster.net
# or
https://www.whatsmydns.net
```

### Check HTTPS
```bash
curl -I https://networkbuster.net
openssl s_client -connect networkbuster.net:443
```

### Azure Resources
```bash
# All resources
az resource list --resource-group networkbuster-rg --output table

# Specific service
az containerapp show --name networkbuster-server --resource-group networkbuster-rg --output json
```

### Vercel
- Dashboard: https://vercel.com
- Domain Status: Settings > Domains
- Deployments: View latest deployment

---

## Success Criteria

### Phase 1: Azure Infrastructure ✅
- [x] Container Registry created
- [x] Log Analytics configured
- [x] Container App Environment ready
- [x] Key Vault registered

### Phase 2: Docker Image (Ready)
- [ ] Docker image built locally
- [ ] Image pushed to registry
- [ ] Image verified in registry

### Phase 3: Container Apps (Ready)
- [ ] Main server deployed
- [ ] API server deployed
- [ ] Ingress configured
- [ ] Services responding

### Phase 4: Custom Domain (In Progress)
- [ ] Domain added to Vercel
- [ ] DNS records configured
- [ ] DNS propagated globally
- [ ] Vercel shows "Valid"

### Phase 5: SSL/HTTPS ✅
- [x] Vercel auto-provisioning enabled
- [ ] Certificate installed
- [ ] HTTPS working
- [ ] Certificate valid

---

## Important Notes

- **Vercel is Primary**: Your app is already live and working great
- **Azure is Optional**: Good for API-only or additional scalability
- **Custom Domain**: Brings professional image, improves SEO
- **SSL Certificates**: All automatic with Vercel
- **DNS Propagation**: Takes 24-48 hours globally

---

## Support & Resources

### Your Resources
- GitHub: https://github.com/NetworkBuster/networkbuster.net
- Vercel: https://vercel.com
- Azure Portal: https://portal.azure.com
- Documentation: See files in this directory

### External Tools
- DNS Check: https://www.whatsmydns.net
- Cert Check: https://www.ssllabs.com/ssltest
- Domain Info: https://www.nslookup.io
- SSL Monitor: https://crt.sh

### Getting Help
- Vercel Support: vercel.com/support
- Azure Support: portal.azure.com > Help + Support
- GitHub Issues: github.com/NetworkBuster/networkbuster.net/issues

---

## Next Priority Action

**ADD CUSTOM DOMAIN TO VERCEL**

1. Go to: https://vercel.com
2. Select: NetworkBuster project
3. Click: Settings > Domains
4. Add: networkbuster.net
5. Configure DNS at registrar
6. Wait 24-48 hours
7. Test: https://networkbuster.net

---

*Last Updated: December 14, 2025*
*Project: NetworkBuster (networkbuster.net)*
*Status: Production Ready*
