# NetworkBuster DNS Configuration - Updated

## Primary Domain: networkbuster.net

### A Records (DNS Configuration)
Add these records to your domain registrar DNS settings:

| Type | Name | Value | TTL | Purpose |
|------|------|-------|-----|---------|
| A | @ | 216.198.79.1 | 3600 | Primary domain |
| A | @ | (secondary - if needed) | 3600 | Backup/redundancy |
| AAAA | @ | (IPv6 if available) | 3600 | IPv6 support |
| CNAME | www | networkbuster.net | 3600 | WWW subdomain alias |

### Quick Reference
```
Domain:        networkbuster.net
A Record:      216.198.79.1
TTL:           3600 seconds (1 hour)
Type:          Standard DNS A Record
```

### Implementation Steps

#### Step 1: Log in to Your Domain Registrar
1. Go to your domain registrar (GoDaddy, Namecheap, Route53, etc.)
2. Find **DNS Settings** or **Manage DNS**
3. Locate DNS records section

#### Step 2: Add/Update A Record
1. **Type**: A Record
2. **Name/Host**: @ (or leave blank - represents root domain)
3. **Value/Points to**: 216.198.79.1
4. **TTL**: 3600 (or default)
5. Click **Save** or **Update**

#### Step 3: Add WWW Alias (Optional)
1. **Type**: CNAME
2. **Name**: www
3. **Value**: networkbuster.net
4. **TTL**: 3600
5. Click **Save**

#### Step 4: Verify Propagation
Wait 5-30 minutes, then test:

```bash
# Check DNS propagation
nslookup networkbuster.net
# Should return: 216.198.79.1

# Or check globally
# https://www.whatsmydns.net
```

### Complete DNS Configuration

If you want to add multiple A records for redundancy:

```
@ (root)       A  216.198.79.1
www            CNAME  networkbuster.net
blog           A  216.198.79.1
dashboard      A  216.198.79.1
api            A  216.198.79.1 (or different IP if hosted elsewhere)
```

### Verification Commands

```bash
# Test A record
nslookup networkbuster.net
dig networkbuster.net

# Test WWW
nslookup www.networkbuster.net

# Test with specific DNS server
nslookup networkbuster.net 8.8.8.8  # Google DNS

# Check all records
dig networkbuster.net ANY
```

### Expected Output
```
networkbuster.net has address 216.198.79.1
```

---

## DNS Propagation Timeline
- **Immediate**: Updates saved at registrar
- **5-30 minutes**: Most areas reflect changes
- **24-48 hours**: Global propagation complete

### Check Global Propagation
Use: https://www.whatsmydns.net
- Enter: networkbuster.net
- Select: A record
- Shows propagation status worldwide

---

## Important Notes
- ✅ Using standard A record (no CNAME for root domain)
- ✅ TTL of 3600 is standard
- ✅ IP: 216.198.79.1 is now primary
- ⏳ DNS changes take time to propagate
- 📋 Keep old DNS records as backup for 24-48 hours

---

## Troubleshooting

### DNS Not Updating
1. Clear local DNS cache
   ```bash
   # Windows
   ipconfig /flushdns
   
   # macOS
   sudo dscacheutil -flushcache
   
   # Linux
   sudo systemctl restart systemd-resolved
   ```

2. Wait 24-48 hours for full propagation
3. Check with multiple DNS servers:
   ```bash
   nslookup networkbuster.net 8.8.8.8     # Google
   nslookup networkbuster.net 1.1.1.1     # Cloudflare
   nslookup networkbuster.net 208.67.222.222  # OpenDNS
   ```

### Wrong IP Showing
1. Verify you saved changes at registrar
2. Check you used correct IP: **216.198.79.1**
3. Wait for cache to clear (10-30 min)
4. Try from different location/network

---

## Registrar-Specific Steps

### GoDaddy
1. DNS > Manage DNS
2. Edit A Record
3. Name: @ | Value: 216.198.79.1 | Save

### Namecheap
1. Dashboard > Manage > Nameservers
2. Go to Advanced DNS
3. Add A Record: 216.198.79.1

### Route53 (AWS)
1. Go to Hosted Zone
2. Create/Edit Record Set
3. Type: A | Name: networkbuster.net | Value: 216.198.79.1

### Cloudflare
1. DNS tab
2. Create A Record
3. Name: networkbuster.net | Content: 216.198.79.1 | TTL: Auto

---

## Status Checklist

- [ ] Log into domain registrar
- [ ] Find DNS settings
- [ ] Add A record: 216.198.79.1
- [ ] Add CNAME for www (optional)
- [ ] Save changes
- [ ] Wait 5-30 minutes
- [ ] Test with nslookup
- [ ] Verify: https://www.whatsmydns.net
- [ ] Test website: https://networkbuster.net

---

**You're all set!** Your domain networkbuster.net now points to 216.198.79.1
