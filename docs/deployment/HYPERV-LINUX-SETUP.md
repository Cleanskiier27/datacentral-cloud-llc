# 🖥️ Hyper-V & Linux Ubuntu VM Setup Guide

## Step 1: Enable Hyper-V on Windows

### Method A: PowerShell (Admin Required)
```powershell
# Run PowerShell as Administrator, then:
Enable-WindowsOptionalFeature -FeatureName Hyper-V -Online -All

# Restart your computer
Restart-Computer -Force
```

### Method B: Settings GUI
1. Press `Windows Key + R` → type `optionalfeatures` → Enter
2. Check the box: "Hyper-V"
3. Click "OK" and restart

### Verify Hyper-V is Enabled
```powershell
# After restart, run this in PowerShell (Admin):
Get-VM
# Should show no VMs or existing ones
```

---

## Step 2: Download Ubuntu ISO

### Option A: Download directly
- Go to: https://ubuntu.com/download/server
- Download **Ubuntu Server 24.04 LTS** (latest stable)
- Save to your Downloads folder, e.g. `ubuntu-24.04-live-server-amd64.iso`

### Option B: Using PowerShell
```powershell
$uri = "https://releases.ubuntu.com/24.04.1/ubuntu-24.04.1-live-server-amd64.iso"
$output = "$env:USERPROFILE\Downloads\ubuntu-24.04-live-server-amd64.iso"
Invoke-WebRequest -Uri $uri -OutFile $output
```

---

## Step 3: Create Ubuntu VM in Hyper-V Manager

### Launch Hyper-V Manager
```powershell
# Run as Administrator
hyperv.msc
```

Or search "Hyper-V Manager" in Windows Start menu

### Create New Virtual Machine

**In Hyper-V Manager:**

1. **Action → New → Virtual Machine**
   
2. **Name and Location:**
   - Name: `NetworkBuster-Linux`
   - Location: `C:\Hyper-V\NetworkBuster-Linux`

3. **Generation:**
   - Select: **Generation 2** (modern, faster)

4. **Memory:**
   - RAM: **4096 MB** (4GB recommended)
   - ✓ Use dynamic memory

5. **Networking:**
   - Virtual switch: **Default Switch** (or create new)

6. **Virtual Hard Disk:**
   - Create a virtual hard disk
   - Size: **50 GB** (for project + dependencies)
   - Location: `C:\Hyper-V\NetworkBuster-Linux\disk.vhdx`

7. **Installation Options:**
   - Select: "Install an operating system from a bootable image file"
   - Browse to your downloaded Ubuntu ISO

8. **Summary:** Click "Finish"

### Step 3.1: GPU Partitioning (Pro Upgrade)
For optimal AI Gateway performance, allow the VM to access your host GPU (GPU-PV).

Run this in PowerShell (Admin) after creating the VM:
```powershell
# Assign GPU to VM
.\scripts\provision-hyperv-vm.ps1 -VMName "NetworkBuster-Linux" -EnableGPU -EnableNetworkAcceleration
```

---

## Step 4: Start VM and Install Ubuntu

### Start the VM
```powershell
# In Hyper-V Manager, right-click VM → Connect
# Or in PowerShell:
Start-VM -Name "NetworkBuster-Linux"
```

### Install Ubuntu (in VM console)

1. **Language:** Select English
2. **Keyboard:** Select your layout
3. **Network:** Choose automatic DHCP
4. **Storage:** Use default (entire disk)
5. **Profile:** 
   - Your name: `ubuntu`
   - Username: `ubuntu`
   - Password: (your choice)
   - Hostname: `networkbuster-dev`
6. **SSH Server:** Select "Install OpenSSH server"
7. **Snaps:** Skip extra packages
8. Wait for installation (~5 min)
9. **Reboot:** Press Enter

---

## Step 5: Post-Installation Setup

### In Ubuntu VM Terminal

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 24.x (LTS)
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs

# Install Git & Optimization Tools
sudo apt install -y git net-tools ethtool

# Verify installations
node --version  # v24.x
npm --version   # 10.x
git --version   # 2.x
```

---

## Step 6: Clone & Setup NetworkBuster Project

### Clone the Repository
```bash
# Create projects folder
mkdir -p ~/projects
cd ~/projects

# Clone NetworkBuster
git clone https://github.com/NetworkBuster/networkbuster.net.git
cd networkbuster.net

# Switch to development branch
git checkout bigtree
```

### Install Dependencies
```bash
# Install all packages
npm install

# Verify
npm list --depth=0
```

Expected output:
```
networkbuster-server@1.0.1
├── compression@1.8.1
├── express@5.2.1
└── helmet@7.2.0
```

---

## Step 7: Test Servers on Linux

### Terminal 1: Start Main Server
```bash
cd ~/projects/networkbuster.net
node server-universal.js
```

**Expected Output:**
```
🚀 Server running at http://localhost:3000
⚡ Features:
   ✓ Compression enabled
   ✓ Security headers enabled
   ✓ Health checks available
   ✓ Control panel: /control-panel
   ✓ API: /api/*
```

### Terminal 2: Start API Server
```bash
cd ~/projects/networkbuster.net
node api/server-universal.js
```

**Expected Output:**
```
🚀 API Server running at http://localhost:3001
⚡ Features:
   ✓ Compression enabled
   ✓ Security headers enabled
   ✓ Health checks: /health, /api/health/detailed
   ✓ Specs: /api/specs
```

### Terminal 3: Test Health Endpoints
```bash
# Main server health
curl http://localhost:3000/api/health

# API server health
curl http://localhost:3001/api/health

# Detailed health
curl http://localhost:3001/api/health/detailed
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-14T10:30:00Z",
  "uptime": 15,
  "requestCount": 2,
  "port": 3000
}
```

---

## Step 8: Access from Windows

### Get VM IP Address
```bash
# In Ubuntu terminal
ip addr show | grep "inet "
```

Look for: `192.168.x.x` (not 127.0.0.1)

### From Windows Browser
```
http://192.168.x.x:3000
http://192.168.x.x:3001/api/health
http://192.168.x.x:3000/control-panel
```

### PowerShell Testing
```powershell
# From Windows PowerShell (replace x.x with actual IP)
Invoke-WebRequest -Uri "http://192.168.x.x:3000/api/health" | ConvertTo-Json

curl http://192.168.x.x:3001/api/health
```

---

## Step 9: Docker Testing (Bonus)

### Install Docker in Ubuntu
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
```

### Build & Run Image
```bash
cd ~/projects/networkbuster.net

# Build image
docker build -t networkbuster:linux .

# Run container
docker run -p 3000:3000 -p 3001:3001 networkbuster:linux

# Test from Windows
curl http://192.168.x.x:3000/api/health
```

---

## Common Commands

### Start/Stop VM
```powershell
# Start
Start-VM -Name "NetworkBuster-Linux"

# Stop gracefully
Stop-VM -Name "NetworkBuster-Linux"

# Hard shutdown
Stop-VM -Name "NetworkBuster-Linux" -Force
```

### Connect to VM
```powershell
# Open VM console
vmconnect localhost "NetworkBuster-Linux"
```

### SSH from Windows (Advanced)
```powershell
# Get VM IP first
# Then use:
ssh ubuntu@192.168.x.x

# Or with key (if set up):
ssh -i C:\path\to\key ubuntu@192.168.x.x
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Hyper-V not available" | Your Windows edition needs Pro/Enterprise |
| VM won't start | Virtualization enabled in BIOS (restart → F12/Del → enable) |
| No network in VM | Check "Default Switch" in Hyper-V settings |
| Can't reach VM from Windows | Get IP with `ip addr show`, use that IP |
| npm install fails | Run `sudo apt update` first |
| Node not found | Restart terminal after installing |
| Port 3000 in use | Kill with `sudo lsof -i :3000` or change PORT env var |

---

## Testing Checklist

- [ ] Hyper-V enabled on Windows
- [ ] Ubuntu VM created and running
- [ ] Ubuntu system updated (`apt update && apt upgrade`)
- [ ] Node.js 24.x installed
- [ ] Git installed
- [ ] Project cloned to `~/projects/networkbuster.net`
- [ ] Dependencies installed (`npm install`)
- [ ] Main server starts (`node server-universal.js`)
- [ ] API server starts (`node api/server-universal.js`)
- [ ] Health endpoints respond (curl works)
- [ ] Windows can reach VM on network

---

## Performance Tuning (Pro)

### Enable SR-IOV
Single Root I/O Virtualization (SR-IOV) significantly reduces network latency.
1. In Hyper-V Manager → Virtual Switch Manager.
2. Select your switch → Check "Enable SR-IOV".
3. In VM Settings → Network Adapter → Hardware Acceleration → Check "Enable SR-IOV".

### Nested Virtualization (For Docker)
If you plan to run Docker *inside* your Linux VM:
```powershell
Set-VMProcessor -VMName "NetworkBuster-Linux" -ExposeVirtualizationExtensions $true
```

---

## Next Steps

1. ✅ Enable Hyper-V (restart required)
2. ✅ Download Ubuntu ISO
3. ✅ Create VM in Hyper-V Manager
4. ✅ Run `provision-hyperv-vm.ps1` for GPU/Performance
5. ✅ Install Ubuntu
6. ✅ Install Node.js & dependencies
7. ✅ Clone project
8. ✅ Test servers

**You now have a high-performance AI-ready Linux testing environment!**
