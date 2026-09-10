# NetworkBuster Custom Domain Configuration Summary

**Date**: December 14, 2025  
**Status**: Ready to Configure  
**Primary Domain**: networkbuster.net

---

## Quick Start

Your domain `networkbuster.net` is configured in your package.json homepage. Here's what's been set up:

### Files Created
1. **CUSTOM-DOMAIN-SETUP.md** - Complete setup guide
2. **infra/custom-domain.bicep** - Azure infrastructure template
3. **configure-custom-domain.ps1** - Automated configuration script

---

## Current Status

| Service | Domain | Status |
|---------|--------|--------|
| **Vercel App** | networkbuster.net | Ready to configure |
| **Vercel WWW** | www.networkbuster.net | Ready to configure |
| **Azure API** | api.networkbuster.net | Ready to configure |
| **Azure Container App** | networkbuster-server | Deployed |
| **Key Vault** | networkbuster-kv | Registering |

---

## Configuration Checklist

### Vercel Setup (Recommended First)
- [ ] Verify domain ownership (networkbuster.net is registered)
- [ ] Login to Vercel Dashboard
- [ ] Go to Project Settings > Domains
- [ ] Add custom domain: `networkbuster.net`
- [ ] Configure DNS records with your registrar:
  - Option 1: Add A records (76.76.19.21, 76.76.20.21)
  - Option 2: Add CNAME to cname.vercel-dns.com
- [ ] Add www subdomain alias
- [ ] Wait for SSL certificate provisioning (automatic)
- [ ] Test: https://networkbuster.net

### Azure Container Apps Setup (Optional)
- [ ] Register Microsoft.KeyVault provider ✓ (In Progress)
- [ ] Upload or generate SSL certificate
- [ ] Store certificate in Key Vault: networkbuster-kv
- [ ] Add custom domain to Container App: api.networkbuster.net
- [ ] Configure DNS CNAME record for api subdomain
- [ ] Test: https://api.networkbuster.net

---

## DNS Records Reference

### For Vercel (Primary Domain)
```
Nameserver Update or DNS Records:
Root (@):  A 76.76.19.21 (Primary)
           A 76.76.20.21 (Secondary)
           AAAA 2606:4700:20::681c:1314 (IPv6)
           AAAA 2606:4700:20::681c:1415 (IPv6)
           OR CNAME cname.vercel-dns.com

www:       CNAME cname.vercel-dns.com
```

### For Azure Container Apps (API)
```
api:       CNAME networkbuster-server.eastus.azurecontainerapps.io
```

---

## SSL/TLS Certificates

### Current Status
- Vercel: **Automatic provisioning** (included with custom domain)
- Azure: **Manual upload required**

### Certificate Options for Azure

**Option 1: Let's Encrypt (Free, Recommended)**
```bash
certbot certonly --standalone \
  -d networkbuster.net \
  -d www.networkbuster.net \
  -d api.networkbuster.net
```

**Option 2: Purchase from Registrar**
- GoDaddy, Namecheap, or your domain registrar
- Buy standard or wildcard certificate
- Download certificate and private key
- Convert to PFX format if needed

**Option 3: Azure-managed Certificate**
- Use App Service managed certificate feature
- Limited to App Service tier (not Container Apps)

### Upload to Key Vault
```bash
az keyvault certificate import \
  --vault-name networkbuster-kv \
  --name networkbuster-cert \
  --file /path/to/certificate.pfx \
  --password your-cert-password
```

---

## Testing & Verification

### Check DNS Propagation
```bash
# Using nslookup
nslookup networkbuster.net
nslookup www.networkbuster.net
nslookup api.networkbuster.net

# Or use online tool
# https://www.whatsmydns.net
```

### Test HTTPS Connectivity
```bash
# Test main domain
curl -I https://networkbuster.net

# Test API domain
curl -I https://api.networkbuster.net

# Check certificate details
openssl s_client -connect networkbuster.net:443 -servername networkbuster.net
```

### Monitor in Vercel
1. Go to vercel.com
2. Select your project
3. Settings > Domains
4. Check domain status: "Valid", "Configuring", etc.

### Monitor in Azure
```bash
# Check container app ingress configuration
az containerapp show \
  --name networkbuster-server \
  --resource-group networkbuster-rg \
  --query properties.configuration.ingress

# Check certificate status
az keyvault certificate show \
  --vault-name networkbuster-kv \
  --name networkbuster-cert
```

---

## Troubleshooting

### DNS Not Resolving
- Check that DNS records are properly added to your registrar
- Wait 24-48 hours for global DNS propagation
- Use https://www.whatsmydns.net to check global propagation
- Clear local DNS cache: `ipconfig /flushdns` (Windows) or `sudo dscacheutil -flushcache` (macOS)

### SSL Certificate Errors
- Ensure certificate matches domain name
- Check certificate expiration date
- Verify certificate chain is complete
- For Azure: Upload to Key Vault before binding domain

### Vercel Domain Issues
1. Verify domain ownership in Vercel dashboard
2. Ensure DNS records match Vercel's requirements
3. Check firewall rules if blocking Vercel IP addresses
4. Contact Vercel support if issues persist

### Azure Container App Issues
- Container App may not have ingress enabled
- Check Network/Ingress configuration
- Ensure certificate is valid and uploaded
- Verify domain doesn't contain invalid characters

---

## Next Steps

1. **Immediate**: Verify domain registration with your registrar
2. **Short-term**: Configure DNS records for Vercel
3. **Mid-term**: Test domain accessibility
4. **Optional**: Set up Azure API domain with SSL certificate
5. **Ongoing**: Monitor certificate expiration dates

---

## Resources

- [Vercel Custom Domains Documentation](https://vercel.com/docs/concepts/projects/domains/add-domain)
- [Azure Container Apps Custom Domains](https://learn.microsoft.com/en-us/azure/container-apps/custom-domains-certificates)
- [Azure Key Vault Documentation](https://learn.microsoft.com/en-us/azure/key-vault/)
- [Let's Encrypt Free SSL](https://letsencrypt.org/)
- [DNS Propagation Checker](https://www.whatsmydns.net)

---

## Support

For issues or questions:
1. Check CUSTOM-DOMAIN-SETUP.md for detailed instructions
2. Review the troubleshooting section above
3. Check service-specific documentation links
4. Contact your domain registrar for DNS issues
5. Contact Vercel or Azure support for platform issues

---

**Tip**: Start with Vercel custom domain configuration since it's simpler and provides automatic SSL. Azure custom domain is optional for API endpoints.
