# 🚀 Hyper-V Linux Setup - Quick Start

## Prerequisites Check
- Windows 10/11 Pro/Enterprise (Home edition doesn't have Hyper-V)
- At least 8GB RAM
- Virtualization enabled in BIOS

---

## One-Command Setup (PowerShell as Admin)

```powershell
# 1. ENABLE HYPER-V (requires restart)
Enable-WindowsOptionalFeature -FeatureName Hyper-V -Online -All

# After restart, create VM manually (see HYPERV-LINUX-SETUP.md)
# Then run the Upgrade script:
.\scripts\provision-hyperv-vm.ps1 -VMName "NetworkBuster-Linux" -EnableGPU -EnableNetworkAcceleration
```

---

## Quick Ubuntu VM Creation

1. Open **Hyper-V Manager** (Admin)
2. Click **Action → New → Virtual Machine**
3. **Name:** `NetworkBuster-Linux`
4. **Generation:** 2
5. **Memory:** 4096 MB
6. **Network:** Default Switch
7. **Disk:** 50 GB
8. **ISO:** Download from https://ubuntu.com/download/server
   - Choose: **Ubuntu Server 24.04 LTS**

---

## After Ubuntu Install

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 24.x LTS
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs git ethtool

# Clone project
git clone https://github.com/NetworkBuster/networkbuster.net.git
cd networkbuster.net && git checkout bigtree

# Install dependencies
npm install

# Test servers
node server-universal.js    # Terminal 1
node api/server-universal.js  # Terminal 2

# From Windows: Find VM IP
# ip addr show | grep "inet "
# Then: curl http://192.168.x.x:3000/api/health
```

---

## PowerShell VM Commands

```powershell
# Start VM
Start-VM -Name "NetworkBuster-Linux"

# Stop VM gracefully
Stop-VM -Name "NetworkBuster-Linux"

# Connect to VM console
vmconnect localhost "NetworkBuster-Linux"

# List all VMs
Get-VM
```

---

## Test Endpoints from Windows

```powershell
# Get VM IP (from Ubuntu: ip addr show)
$vmIP = "192.168.x.x"  # Replace with actual IP

# Test main server
curl http://$vmIP:3000/api/health
curl http://$vmIP:3000/control-panel

# Test API server
curl http://$vmIP:3001/api/health
curl http://$vmIP:3001/api/specs
```

---

## Files Referenced

- 📄 [HYPERV-LINUX-SETUP.md](HYPERV-LINUX-SETUP.md) - Complete detailed guide
- 📄 `HYPERV-QUICK-START.md` - This quick reference

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| PowerShell "requires elevation" | Run as Administrator |
| Can't enable Hyper-V | Check Windows edition (needs Pro+) |
| VM not starting | Enable virtualization in BIOS (F12/Del on boot) |
| No network in VM | Use "Default Switch" in Hyper-V settings |
| Node not found in VM | Restart terminal after install |

---

## Next: Test Your Servers

Once Linux VM is running with servers started:

✅ Windows: Open `http://192.168.x.x:3000` (replace with VM IP)
✅ Both servers showing health checks
✅ Control panel accessible
✅ All tests passing on Linux

You now have **multi-OS testing environment!**
