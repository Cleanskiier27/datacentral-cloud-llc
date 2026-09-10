# Vercel Custom Domain Setup - Step by Step

**For Domain**: networkbuster.net  
**Current Vercel URL**: https://networkbuster-mez5d7bmv-networkbuster.vercel.app

---

## Step 1: Log In to Vercel

1. Go to https://vercel.com
2. Click "Log In"
3. Sign in with your GitHub account (or associated Vercel account)

---

## Step 2: Navigate to Your Project

1. In the dashboard, find your **NetworkBuster** project
2. Click on it to open the project settings

---

## Step 3: Go to Domains Settings

1. In the top menu, click **Settings**
2. In the left sidebar, click **Domains**
3. You'll see your current domain: `networkbuster-mez5d7bmv-networkbuster.vercel.app`

---

## Step 4: Add Your Custom Domain

1. Click the **Add Domain** button
2. In the input field, type: **networkbuster.net**
3. Click **Add**

---

## Step 5: Configure DNS Records

Vercel will show you DNS configuration options. Choose one:

### Option A: Nameserver Update (Easiest)
Vercel will provide nameservers. Update your domain registrar:
1. Go to your domain registrar (GoDaddy, Namecheap, etc.)
2. Find DNS or Nameserver settings
3. Replace existing nameservers with Vercel's:
   - ns1.vercel-dns.com
   - ns2.vercel-dns.com
   - ns3.vercel-dns.com
   - ns4.vercel-dns.com

### Option B: CNAME Records (If nameserver update not available)
1. Go to your domain registrar DNS settings
2. Add these records:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | www | cname.vercel-dns.com | 3600 |
| A | @ | 76.76.19.21 | 3600 |
| A | @ | 76.76.20.21 | 3600 |
| AAAA | @ | 2606:4700:20::681c:1314 | 3600 |
| AAAA | @ | 2606:4700:20::681c:1415 | 3600 |

---

## Step 6: Verify Domain

1. In Vercel, the domain status will show as "Pending Verification"
2. Go back to your registrar and confirm DNS records are saved
3. Wait 5-30 minutes for propagation
4. Vercel will automatically detect when DNS is configured
5. Status will change to "Valid"

---

## Step 7: Configure www Subdomain (Optional)

Once primary domain is verified:

1. In Vercel Domains settings, click **Add Domain** again
2. Type: **www.networkbuster.net**
3. Vercel will ask if you want to alias it to `networkbuster.net`
4. Click **Alias** - this avoids separate DNS records
5. Now both `networkbuster.net` and `www.networkbuster.net` work

---

## Step 8: SSL Certificate

1. Vercel automatically provisions SSL certificates via Let's Encrypt
2. Wait for certificate provisioning (usually 5-30 minutes)
3. Status in Vercel dashboard will show:
   - "Valid" - Domain is ready
   - "🔒" lock icon - HTTPS is enabled

---

## Step 9: Test Your Domain

Open these in your browser:
- https://networkbuster.net - Should load your app
- https://www.networkbuster.net - Should also work
- Check that the SSL certificate is valid (green lock in browser)

---

## Common Issues & Solutions

### Domain Not Showing as Valid

**Issue**: Vercel shows "Pending" after 30 minutes
**Solution**:
1. Double-check DNS records in your registrar
2. Use https://www.whatsmydns.net to verify propagation globally
3. Some registrars have DNS cache - may take 24-48 hours
4. Contact your registrar support if records show as changed

### HTTPS Not Working

**Issue**: Browser shows "Certificate Error"
**Solution**:
1. Wait 30 minutes for certificate to provision
2. Clear browser cache (Ctrl+Shift+Delete)
3. Try incognito/private window
4. Check certificate status in Vercel dashboard
5. Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

### Too Many DNS Records

**Issue**: Your registrar won't accept all CNAME records
**Solution**:
1. Use nameserver update instead (Option A) - simpler
2. Or use only the A records (most important)
3. Ask your registrar about CNAME flattening for root domain

---

## Dashboard Monitoring

After setup, monitor in Vercel:

1. **Settings > Domains** - See all configured domains
2. Check status indicators:
   - ✅ "Valid" - Everything working
   - ⏳ "Pending Verification" - Waiting for DNS
   - ❌ "Invalid" - Check DNS records
3. View SSL certificate details
4. Create deployment aliases (optional)

---

## Next Steps

1. ✅ Add custom domain to Vercel
2. ✅ Configure DNS records at registrar
3. ✅ Wait for propagation
4. ✅ Verify domain is valid
5. ✅ Test HTTPS access
6. (Optional) Configure api.networkbuster.net for Azure

---

## Quick Reference

| Item | Value |
|------|-------|
| Primary Domain | networkbuster.net |
| Current Vercel URL | networkbuster-mez5d7bmv-networkbuster.vercel.app |
| Vercel Dashboard | https://vercel.com |
| Nameservers | ns1-4.vercel-dns.com |
| Primary A Record | 76.76.19.21 |
| Secondary A Record | 76.76.20.21 |
| CNAME Value | cname.vercel-dns.com |

---

## Support

- **Vercel Support**: https://vercel.com/support
- **DNS Check**: https://www.whatsmydns.net
- **Certificate Check**: https://www.ssllabs.com/ssltest
- **Registrar Support**: Contact your domain registrar directly

---

**Estimated Time**: 5-15 minutes for initial setup + 24-48 hours for full propagation

**Pro Tip**: Once domain is configured, Vercel handles all SSL certificate renewals automatically!
