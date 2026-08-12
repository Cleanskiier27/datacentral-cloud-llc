# NetworkBuster Custom Domain Configuration

## Domain Information
- **Primary Domain**: networkbuster.net
- **Status**: Active
- **Registrar**: (Update with your registrar)
- **Current Deployment**: Vercel
- **Azure Backup**: Ready

## Vercel Custom Domain Setup

### Current Configuration
```json
{
  "buildCommand": "npm run build:all || npm run build || true",
  "devCommand": "npm start",
  "installCommand": "npm ci --legacy-peer-deps || npm install",
  "env": {
    "NODE_ENV": "production",
    "VERCEL_ENV": "production"
  },
  "domains": [
    {
      "domain": "networkbuster.net",
      "type": "primary"
    },
    {
      "domain": "www.networkbuster.net",
      "type": "alias"
    }
  ]
}
```

### Vercel DNS Records Required
Add these records to your DNS provider:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | www | cname.vercel-dns.com | 3600 |
| A | @ | 76.76.19.21 | 3600 |
| AAAA | @ | 2606:4700:20::681c:1314 | 3600 |
| A | @ | 76.76.20.21 | 3600 |
| AAAA | @ | 2606:4700:20::681c:1415 | 3600 |

OR simply set CNAME for root and www:
| Type | Name | Value |
|------|------|-------|
| CNAME | www | cname.vercel-dns.com |

## Azure Container Apps Custom Domain

### Prerequisites
1. Certificate from issuer (Let's Encrypt, DigiCert, etc.)
2. Private key for the certificate
3. Certificate thumbprint

### Azure CLI Commands

```bash
# Get container app name
az containerapp list --resource-group networkbuster-rg --query "[].name" -o table

# Bind custom domain to Container App
az containerapp hostname bind \
  --resource-group networkbuster-rg \
  --container-app-name networkbuster-server \
  --hostname api.networkbuster.net \
  --certificate-name networkbuster-cert

# For TLS certificate
az containerapp env certificate upload \
  --resource-group networkbuster-rg \
  --environment networkbuster-env \
  --certificate-name networkbuster-cert \
  --certificate-path /path/to/cert.pfx \
  --password your-certificate-password
```

### Azure DNS Records for API
| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | api | networkbuster-server.eastus.azurecontainerapps.io | 3600 |

## Recommended Domain Structure

```
networkbuster.net              -> Vercel (main app, Vite dashboards)
www.networkbuster.net          -> Vercel (alias)
api.networkbuster.net          -> Azure Container Apps (API server)
docs.networkbuster.net         -> Vercel (documentation)
blog.networkbuster.net         -> Vercel (blog content)
```

## SSL/TLS Certificate Management

### Option A: Let's Encrypt (Free)
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-dns-azure

# Generate certificate
certbot certonly \
  --dns-azure \
  -d networkbuster.net \
  -d www.networkbuster.net \
  -d api.networkbuster.net
```

### Option B: Purchase Certificate
1. Go to your domain registrar
2. Purchase wildcard certificate: *.networkbuster.net
3. Get certificate and private key files
4. Upload to Azure Key Vault (recommended)

## Azure Key Vault Integration

Store certificates securely in Key Vault:

```bash
# Create Key Vault (if not exists)
az keyvault create \
  --name networkbuster-kv \
  --resource-group networkbuster-rg \
  --location eastus

# Import certificate
az keyvault certificate import \
  --vault-name networkbuster-kv \
  --name networkbuster-cert \
  --file /path/to/cert.pfx \
  --password your-password
```

## DNS Provider Configuration

### For your domain registrar:
1. **Login** to your domain registrar (GoDaddy, Namecheap, Route53, etc.)
2. **Go to DNS Settings**
3. **Add Records** (see Vercel DNS Records section above)
4. **Wait** for propagation (typically 24-48 hours)

### Test DNS:
```bash
# Check DNS propagation
nslookup networkbuster.net
nslookup www.networkbuster.net
nslookup api.networkbuster.net

# Or use dig
dig networkbuster.net +short
```

## Monitoring Custom Domains

### Vercel Dashboard
1. Go to vercel.com
2. Select your project
3. Go to Settings > Domains
4. Check domain status and SSL certificate validity

### Azure
```bash
# Check container app domains
az containerapp show \
  --name networkbuster-server \
  --resource-group networkbuster-rg \
  --query properties.configuration.ingress

# Check certificate status
az keyvault certificate show \
  --vault-name networkbuster-kv \
  --name networkbuster-cert
```

## Troubleshooting

### Domain Not Resolving
```bash
# Check DNS propagation globally
# Use https://www.whatsmydns.net
# Look for nameservers
nslookup networkbuster.net NS
```

### SSL Certificate Issues
```bash
# Check certificate expiration
openssl x509 -in cert.pem -noout -dates

# Verify certificate chain
openssl verify -CAfile chain.pem cert.pem
```

### Vercel Custom Domain Issues
1. Check domain ownership verification
2. Ensure DNS records are correct
3. Wait 24-48 hours for full propagation
4. Check Vercel console for error messages

## Next Steps

1. [ ] Verify networkbuster.net is registered
2. [ ] Add DNS records to your registrar
3. [ ] Test DNS propagation with nslookup
4. [ ] Verify Vercel custom domain in dashboard
5. [ ] (Optional) Set up Azure Container Apps custom domain
6. [ ] Configure SSL certificates in Key Vault
7. [ ] Test all endpoints with https

## References
- [Vercel Custom Domains](https://vercel.com/docs/concepts/projects/domains/add-domain)
- [Azure Container Apps Custom Domains](https://learn.microsoft.com/en-us/azure/container-apps/custom-domains-certificates)
- [Azure Key Vault Certificates](https://learn.microsoft.com/en-us/azure/key-vault/certificates/)
