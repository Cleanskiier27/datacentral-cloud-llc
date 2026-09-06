# Dual Router Setup Guide: WiFi 7 Mesh + NetworkBuster.net

**Setup Date:** January 3, 2026  
**Configuration Type:** Cascaded Dual Router with Custom Domain

---

## Network Topology Overview

```
Internet → WiFi 7 Mesh Router (Primary) → NetworkBuster Router (Secondary)
              192.168.1.1                    192.168.1.100 or 192.168.2.1
```

---

## Option A: Same Subnet (Simpler Setup)

### WiFi 7 Mesh Router (Primary Gateway)

**IP Configuration:**
- **Router IP:** `192.168.1.1`
- **Subnet Mask:** `255.255.255.0`
- **DHCP Range:** `192.168.1.10` to `192.168.1.99`
- **DNS Primary:** `8.8.8.8` (Google)
- **DNS Secondary:** `1.1.1.1` (Cloudflare)

**WiFi 7 Settings:**
- **Network Name (SSID):** `YourNetwork-WiFi7`
- **Security:** WPA3-Personal
- **Password:** [Your secure password]
- **Band:** 2.4GHz + 5GHz + 6GHz (tri-band mesh)

### NetworkBuster Router (Secondary)

**IP Configuration:**
- **Router IP:** `192.168.1.100` (static, outside DHCP range)
- **Subnet Mask:** `255.255.255.0`
- **Gateway:** `192.168.1.1` (points to WiFi 7 mesh)
- **DHCP:** **DISABLED** (WiFi 7 handles DHCP)
- **DNS:** `192.168.1.1` (forwards to WiFi 7 router)

**Connection:**
- **Cable:** Connect WiFi 7 mesh LAN port → NetworkBuster WAN/LAN port
- **Mode:** Bridge/AP mode (disable NAT on NetworkBuster)

---

## Option B: Separate Subnet (Advanced - Better Isolation)

### WiFi 7 Mesh Router (Primary Gateway)

**IP Configuration:**
- **Router IP:** `192.168.1.1`
- **Subnet Mask:** `255.255.255.0`
- **DHCP Range:** `192.168.1.10` to `192.168.1.254`
- **DNS Primary:** `8.8.8.8`
- **DNS Secondary:** `1.1.1.1`

### NetworkBuster Router (Secondary Subnet)

**IP Configuration:**
- **Router IP:** `192.168.2.1`
- **Subnet Mask:** `255.255.255.0`
- **Gateway:** `192.168.1.1`
- **DHCP Range:** `192.168.2.10` to `192.168.2.254`
- **DNS:** `192.168.1.1` or `8.8.8.8`

**Connection:**
- **Cable:** WiFi 7 mesh LAN → NetworkBuster WAN port
- **Mode:** Router mode (NAT enabled for subnet isolation)

**Static Route on WiFi 7 Router:**
```
Destination: 192.168.2.0/24
Gateway: 192.168.2.1
```

---

## NetworkBuster.net Domain Setup

### Local DNS Configuration (Internal Network)

**On WiFi 7 Mesh Router:**

**Add DNS Host Entries:**
```
networkbuster.net          → 192.168.1.100 (Option A) or 192.168.2.1 (Option B)
www.networkbuster.net      → 192.168.1.100 or 192.168.2.1
mission.networkbuster.net  → 192.168.1.100 or 192.168.2.1
api.networkbuster.net      → 192.168.1.100 or 192.168.2.1
```

**Alternative: Edit Hosts File on All Devices**
- **Windows:** `C:\Windows\System32\drivers\etc\hosts`
- **macOS/Linux:** `/etc/hosts`

```
192.168.1.100    networkbuster.net www.networkbuster.net
192.168.1.100    mission.networkbuster.net
192.168.1.100    api.networkbuster.net
```

### External DNS (Public Internet Access)

**If You Own networkbuster.net Domain:**

**DNS A Records (at your domain registrar):**
```
Type    Name        Value                   TTL
A       @           [Your Public IP]        3600
A       www         [Your Public IP]        3600
A       mission     [Your Public IP]        3600
A       api         [Your Public IP]        3600
```

**Dynamic DNS (DDNS) Setup:**
- **Service:** No-IP, DuckDNS, or your router's built-in DDNS
- **Update Interval:** Every 5 minutes
- **Domain:** `yourname.ddns.net` (free) or `networkbuster.net` (owned domain)

---

## Port Forwarding Configuration

**Configure on WiFi 7 Mesh Router:**

| Service             | External Port | Internal IP       | Internal Port | Protocol |
|---------------------|---------------|-------------------|---------------|----------|
| Web Server          | 3000          | 192.168.1.100     | 3000          | TCP      |
| API Server          | 3001          | 192.168.1.100     | 3001          | TCP      |
| Audio Stream        | 3002          | 192.168.1.100     | 3002          | TCP      |
| NASA Mission Control| 5000          | 192.168.1.100     | 5000          | TCP      |
| HTTP (Web)          | 80            | 192.168.1.100     | 3000          | TCP      |
| HTTPS (Secure)      | 443           | 192.168.1.100     | 443           | TCP      |

**If Using Option B (Separate Subnet):**
- Change Internal IP to `192.168.2.1` in all port forwarding rules

---

## Windows Firewall Rules (NetworkBuster Device)

**Already Configured:**
```powershell
# Verify existing rules
Get-NetFirewallRule -DisplayName "NetworkBuster*" | Select-Object DisplayName, Enabled
```

**Add Mission Control Port:**
```powershell
New-NetFirewallRule -DisplayName "NetworkBuster-MissionControl" `
    -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

---

## Step-by-Step Setup Process

### Step 1: Configure WiFi 7 Mesh Router
1. Connect to WiFi 7 router at `192.168.1.1`
2. Login to admin panel
3. Set router IP to `192.168.1.1`
4. Enable DHCP: `192.168.1.10` - `192.168.1.99` (Option A) or `192.168.1.10` - `192.168.1.254` (Option B)
5. Set DNS servers: `8.8.8.8` and `1.1.1.1`
6. Enable WiFi 7 (6GHz band)
7. Set WPA3 security

### Step 2: Configure NetworkBuster Router
1. Connect NetworkBuster to computer temporarily
2. Access router at default IP (usually `192.168.0.1` or `192.168.1.1`)
3. Change router IP to:
   - **Option A:** `192.168.1.100`
   - **Option B:** `192.168.2.1`
4. Set subnet mask: `255.255.255.0`
5. **Option A:** Disable DHCP server, enable Bridge/AP mode
6. **Option B:** Enable DHCP (`192.168.2.10` - `192.168.2.254`)
7. Save and reboot

### Step 3: Physical Connection
1. Power off both routers
2. Connect Ethernet cable:
   - WiFi 7 LAN port → NetworkBuster WAN port (or LAN port for Option A)
3. Power on WiFi 7 mesh router first (wait 2 minutes)
4. Power on NetworkBuster router (wait 2 minutes)

### Step 4: Verify Connection
```powershell
# Test connectivity
ping 192.168.1.1          # WiFi 7 router
ping 192.168.1.100        # NetworkBuster (Option A)
ping 8.8.8.8              # Internet

# Test domain resolution
ping networkbuster.net
```

### Step 5: Configure Port Forwarding
1. Login to WiFi 7 router (`192.168.1.1`)
2. Navigate to Port Forwarding / Virtual Servers
3. Add all port forwarding rules from table above
4. Save and apply

### Step 6: Add Local DNS Entries
1. In WiFi 7 router, find DNS/Hostname settings
2. Add custom hosts:
   - `networkbuster.net` → `192.168.1.100`
   - `www.networkbuster.net` → `192.168.1.100`
   - `mission.networkbuster.net` → `192.168.1.100`

### Step 7: Test Services
```powershell
# From any device on network
Invoke-WebRequest -Uri "http://networkbuster.net:3000"
Invoke-WebRequest -Uri "http://networkbuster.net:5000"
Invoke-WebRequest -Uri "http://mission.networkbuster.net:5000"
```

---

## Access URLs (Internal Network)

**Direct IP Access:**
- Web Server: `http://192.168.1.100:3000`
- API Server: `http://192.168.1.100:3001`
- Audio Stream: `http://192.168.1.100:3002`
- NASA Mission Control: `http://192.168.1.100:5000`

**Domain Access (After DNS Setup):**
- Web: `http://networkbuster.net:3000`
- Web: `http://www.networkbuster.net:3000`
- Mission Control: `http://mission.networkbuster.net:5000`
- API: `http://api.networkbuster.net:3001`

**External Access (After Port Forwarding):**
- Web: `http://[YOUR_PUBLIC_IP]:3000`
- Mission Control: `http://[YOUR_PUBLIC_IP]:5000`

---

## Troubleshooting

### Can't Access NetworkBuster Router
```powershell
# Find router IP
arp -a | Select-String "192.168"

# Verify route
route print
```

### Port Not Accessible
```powershell
# Check if port is listening
Get-NetTCPConnection -LocalPort 3000 -State Listen

# Test firewall rule
Test-NetConnection -ComputerName 192.168.1.100 -Port 3000
```

### Domain Not Resolving
```powershell
# Check DNS resolution
nslookup networkbuster.net

# Flush DNS cache
ipconfig /flushdns

# Test direct IP
ping 192.168.1.100
```

### No Internet on NetworkBuster Subnet
```powershell
# Check gateway
ipconfig | Select-String "Gateway"

# Add static route on WiFi 7 router
# Destination: 192.168.2.0/24 → Gateway: 192.168.2.1
```

---

## Security Recommendations

1. **Change Default Passwords:**
   - WiFi 7 router admin password
   - NetworkBuster router admin password
   - WiFi network password

2. **Enable WPA3:** On WiFi 7 mesh for maximum encryption

3. **Disable WPS:** On both routers (security risk)

4. **Enable Firewall:** On both routers

5. **Update Firmware:** Keep both routers updated

6. **Guest Network:** Use WiFi 7 guest network for IoT devices

7. **VPN:** Consider VPN for external access instead of port forwarding

---

## Recommended Configuration

**For Best Performance:** Use **Option A** (Same Subnet)
- Simpler setup
- No double NAT issues
- NetworkBuster acts as WiFi access point
- Easier port forwarding

**For Better Security:** Use **Option B** (Separate Subnet)
- Network isolation
- Separate traffic control
- Better for multiple services
- Easier firewall rules per subnet

---

## Quick Reference

**WiFi 7 Mesh Router:** `192.168.1.1`  
**NetworkBuster Router:** `192.168.1.100` (Option A) or `192.168.2.1` (Option B)  
**Domain:** `networkbuster.net`  
**Services:** Ports 3000, 3001, 3002, 5000  

**DNS Servers:** `8.8.8.8` (Primary), `1.1.1.1` (Secondary)  
**Subnet Mask:** `255.255.255.0`  
**DHCP Range:** `192.168.1.10` - `192.168.1.99` (WiFi 7 only)

---

**Setup Complete!** Your WiFi 7 mesh router and NetworkBuster are now configured for optimal performance with custom domain support.
