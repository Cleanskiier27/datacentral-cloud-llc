# Custom Domain Configuration - Complete Setup

**Status**: ✅ Ready for Implementation  
**Domain**: networkbuster.net  
**Date**: December 14, 2025

---

## What's Been Set Up

### Documentation Created
✅ **VERCEL-DOMAIN-SETUP-GUIDE.md** - Step-by-step Vercel configuration  
✅ **CUSTOM-DOMAIN-SETUP.md** - Comprehensive technical guide  
✅ **DOMAIN-CONFIGURATION-STATUS.md** - Progress tracking checklist  
✅ **configure-custom-domain.ps1** - Automated setup script  
✅ **infra/custom-domain.bicep** - Azure infrastructure template  

### Infrastructure Deployed
✅ Azure Key Vault registered (networkbuster-kv)  
✅ Container Registry ready (networkbusterlo25gft5nqwzg.azurecr.io)  
✅ Container App Environment active (networkbuster-env)  
✅ Log Analytics monitoring configured (networkbuster-logs)  

---

## Quick Start (5 Minutes)

### For Vercel (Main Domain)
1. Go to https://vercel.com
2. Click on your NetworkBuster project
3. Settings > Domains
4. Add domain: **networkbuster.net**
5. Follow DNS configuration (see VERCEL-DOMAIN-SETUP-GUIDE.md)
6. Wait 24-48 hours for DNS propagation
7. Done! Vercel provides free SSL certificate

### For Azure (API Domain - Optional)
1. Generate SSL certificate (Let's Encrypt or purchase)
2. Upload to Key Vault: networkbuster-kv
3. In Azure Portal, bind to Container App
4. Configure DNS: api.networkbuster.net

---

## Domain Structure

```
networkbuster.net
├── Main app (Vercel)
├── www.networkbuster.net (Alias to main)
├── api.networkbuster.net (Azure API - optional)
├── docs.networkbuster.net (Documentation - optional)
└── blog.networkbuster.net (Blog - optional)
```

---

## DNS Configuration Reference

### Vercel (Primary)
```
Option A: Update Nameservers
  ns1.vercel-dns.com
  ns2.vercel-dns.com
  ns3.vercel-dns.com
  ns4.vercel-dns.com

Option B: Add A/CNAME Records
  @ (root):     A 76.76.19.21 or A 76.76.20.21
  www:          CNAME cname.vercel-dns.com
  IPv6 (optional): AAAA 2606:4700:20::681c:1314
```

### Azure (API - Optional)
```
api:  CNAME networkbuster-server.eastus.azurecontainerapps.io
```

---

## SSL/TLS Certificates

### Vercel
- **Automatic**: Let's Encrypt
- **No action needed**: Vercel handles everything
- **Renewal**: Automatic annual renewal

### Azure
- **Option 1**: Let's Encrypt (free)
  ```bash
  certbot certonly -d api.networkbuster.net
  az keyvault certificate import --vault-name networkbuster-kv --name cert
  ```
- **Option 2**: Purchase (GoDaddy, Namecheap, etc.)
- **Option 3**: Azure-managed (App Service only)

---

## Verification Commands

```bash
# Check DNS propagation
nslookup networkbuster.net
nslookup www.networkbuster.net
nslookup api.networkbuster.net

# Check global propagation
# Use: https://www.whatsmydns.net

# Test HTTPS
curl -I https://networkbuster.net
curl -I https://api.networkbuster.net

# Check certificate
openssl s_client -connect networkbuster.net:443 -servername networkbuster.net

# Azure Container App status
az containerapp show --name networkbuster-server --resource-group networkbuster-rg --query properties.configuration.ingress
```

---

## Documentation Index

| Document | Purpose | Time |
|----------|---------|------|
| [VERCEL-DOMAIN-SETUP-GUIDE.md](VERCEL-DOMAIN-SETUP-GUIDE.md) | Vercel configuration steps | 5-15 min |
| [CUSTOM-DOMAIN-SETUP.md](CUSTOM-DOMAIN-SETUP.md) | Complete technical reference | Reference |
| [DOMAIN-CONFIGURATION-STATUS.md](DOMAIN-CONFIGURATION-STATUS.md) | Progress checklist | Tracking |
| `configure-custom-domain.ps1` | Automated script | Run once |
| `infra/custom-domain.bicep` | Azure IaC template | Optional |

---

## Current Deployment Status

| Service | Status | URL |
|---------|--------|-----|
| Vercel App | ✅ Live | https://networkbuster-mez5d7bmv-networkbuster.vercel.app |
| Azure Infra | ✅ Deployed | regionname.azurecontainerapps.io |
| Container Registry | ✅ Active | networkbusterlo25gft5nqwzg.azurecr.io |
| Key Vault | ✅ Ready | networkbuster-kv (registering) |
| Log Analytics | ✅ Active | networkbuster-logs |

---

## Timeline

| Step | Status | Time | Effort |
|------|--------|------|--------|
| 1. Vercel domain setup | Ready | 5-15 min | Low |
| 2. DNS propagation | Waiting | 24-48 hrs | Passive |
| 3. SSL provisioning | Automatic | 5-30 min | None |
| 4. Azure API setup | Optional | 30-60 min | Medium |
| 5. Full verification | Ready | 10 min | Low |

---

## Next Actions

### Immediate (Do Now)
- [ ] Open VERCEL-DOMAIN-SETUP-GUIDE.md
- [ ] Log in to Vercel
- [ ] Add custom domain

### Short Term (Next 24 hrs)
- [ ] Configure DNS at registrar
- [ ] Monitor DNS propagation at whatsmydns.net
- [ ] Verify domain in Vercel

### Medium Term (Optional)
- [ ] Generate SSL certificate for Azure
- [ ] Configure api.networkbuster.net
- [ ] Set up custom domains for docs/blog

### Long Term
- [ ] Monitor certificate expiration dates
- [ ] Review access logs in Log Analytics
- [ ] Optimize CDN caching on Vercel

---

## Key Contacts & Resources

**Domain Registrar**  
- Update your domain registrar nameservers or DNS records
- Contact registrar support if issues

**Vercel Support**  
- Dashboard: https://vercel.com
- Docs: https://vercel.com/docs
- Help: vercel.com/support

**Azure Support**  
- Portal: https://portal.azure.com
- Docs: https://learn.microsoft.com/azure/
- Support: Azure Portal > Help + Support

**DNS Verification**  
- https://www.whatsmydns.net
- https://www.nslookup.io
- https://mxtoolbox.com

**Certificate Check**  
- https://www.ssllabs.com/ssltest
- https://crt.sh
- https://certificatemonitor.org

---

## Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| DNS not resolving | See "Domain Not Resolving" in CUSTOM-DOMAIN-SETUP.md |
| SSL error | See "SSL Certificate Issues" in CUSTOM-DOMAIN-SETUP.md |
| Vercel not detecting | See "Vercel Custom Domain Issues" in CUSTOM-DOMAIN-SETUP.md |
| Azure API issues | See "Azure Container App Issues" in CUSTOM-DOMAIN-SETUP.md |

---

## Summary

Your infrastructure is ready! You have:
- ✅ Live Vercel deployment
- ✅ Azure resources configured
- ✅ SSL certificate automation set up
- ✅ Monitoring and logging enabled
- ✅ Custom domain guides created

**Next Step**: Follow VERCEL-DOMAIN-SETUP-GUIDE.md to add your custom domain to Vercel.

**Estimated time to full custom domain**: 24-48 hours (mostly waiting for DNS)

---

*For detailed instructions, see the documentation files created above.*
