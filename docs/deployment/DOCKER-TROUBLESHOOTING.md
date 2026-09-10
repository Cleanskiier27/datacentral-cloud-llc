# 🐳 Docker Engine Troubleshooting & Fix Guide

## Issue Identified

**Error:** `500 Internal Server Error for API route http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine`

**Root Cause:** Docker daemon/engine is not responding properly. This is common with Docker Desktop on Windows when WSL2 or the daemon encounters issues.

---

## Quick Fixes (Try in Order)

### Fix #1: Restart Docker Desktop (Fastest)
```powershell
# Close Docker Desktop completely
Get-Process docker* | Stop-Process -Force

# Wait 5 seconds
Start-Sleep -Seconds 5

# Restart Docker
Start-Process "C:\Program Files\Docker\Docker\Docker.exe"

# Wait for startup
Start-Sleep -Seconds 15

# Test
docker ps
```

### Fix #2: Reset Docker Engine
```powershell
# Stop all containers
docker kill $(docker ps -q) 2>$null

# Prune unused data
docker system prune -a --volumes -f

# Restart Docker
taskkill /IM "Docker Desktop.exe" /F
Start-Sleep -Seconds 5
Start-Process "C:\Program Files\Docker\Docker\Docker.exe"
Start-Sleep -Seconds 15

# Test
docker ps
```

### Fix #3: Check WSL2 Status (If Using WSL2)
```powershell
# List WSL distributions
wsl --list --verbose

# Ensure Docker Desktop uses WSL2
# Go to: Docker Desktop Settings → Resources → WSL Integration
# Enable: "Use the WSL 2 based engine"
```

### Fix #4: Full Docker Daemon Reset
```powershell
# 1. Stop Docker completely
taskkill /IM "Docker Desktop.exe" /F
taskkill /IM "com.docker.backend.exe" /F

# 2. Clear Docker data
Remove-Item -Path "$env:APPDATA\Docker" -Recurse -Force -ErrorAction SilentlyContinue

# 3. Clear WSL cache
wsl --shutdown

# 4. Restart Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker.exe"
Start-Sleep -Seconds 30

# 5. Test
docker ps
```

---

## Verify Docker is Working

### Test 1: Check Version
```powershell
docker version
```

**Expected:** Shows both client and server versions

### Test 2: Run Test Container
```powershell
docker run hello-world
```

**Expected:** Prints "Hello from Docker!"

### Test 3: List Containers
```powershell
docker ps -a
```

**Expected:** Shows list of containers (may be empty)

### Test 4: Check Disk Space
```powershell
# Check available space (Docker needs ~10GB free)
Get-PSDrive C | Select-Object Name, Used, Free | Format-Table

# If low on space, remove images
docker image prune -a -f
```

---

## Git String Categorization Issue

The Docker error is showing URL encoding issues: `%2F%2F.%2Fpipe` (forward slashes encoded as `%2F`).

This can affect git operations too. **Fix:**

```powershell
# Reset git configuration
git config --global --unset-all core.safecrlf
git config --global --unset-all core.autocrlf
git config --global core.autocrlf false

# Clear git credential cache
git credential-manager delete https://github.com

# Re-authenticate
git credential-manager approve
```

---

## Build Docker Image Without Starting Daemon

If Docker is still problematic, use **Azure Container Registry** instead:

```powershell
# Build directly with ACR (no Docker daemon needed)
az acr build \
  --registry <your-registry-name> \
  --image networkbuster:latest \
  .
```

---

## Alternative: Use containerd or podman

If Docker Desktop is unstable:

### Install Podman (Drop-in Docker Replacement)
```powershell
# Install via Chocolatey
choco install podman -y

# Use same commands
podman ps
podman run hello-world
```

---

## Docker Desktop Settings to Check

1. **Open Docker Desktop Settings**
   - Right-click Docker icon → Settings
   
2. **Check these settings:**
   - **General:** "Start Docker Desktop when you log in"
   - **Resources:** Allocate enough RAM (4GB min, 8GB recommended)
   - **WSL Integration:** Enable if using WSL2
   - **Docker Engine:** Check daemon logs for errors

3. **View Docker Logs**
   ```powershell
   Get-EventLog -LogName Application -Source Docker -Newest 50
   ```

---

## Troubleshooting Network Issues

If Docker can't reach the internet:

```powershell
# Test docker network
docker network ls

# Create new network
docker network create networkbuster-net

# Test connectivity
docker run --rm --network networkbuster-net busybox ping -c 4 8.8.8.8
```

---

## For NetworkBuster Project

### Without Docker (Recommended if Docker Broken)

```powershell
# Build without Docker - run all three servers
npm run start:tri-servers

# Or individually
npm start                        # Main server
npm run start:api               # API server
npm run start:audio             # Audio server
```

### With Azure Container Registry (When Ready)

```bash
# Build with ACR instead of Docker
az acr build \
  --registry <your-registry-name> \
  --image networkbuster:latest \
  --file Dockerfile .
```

---

## Git Issue: String Categorization

The error message shows git/Docker mixing protocols incorrectly. **Solutions:**

```powershell
# 1. Set proper Git protocol
git config --global url."https://github.com/".insteadOf git://github.com/

# 2. Clear cached URLs
Remove-Item -Path "$env:APPDATA\git\config" -Force -ErrorAction SilentlyContinue

# 3. Re-clone if necessary
git clone https://github.com/NetworkBuster/networkbuster.net.git
cd networkbuster.net
git checkout bigtree
```

---

## Prevention: Keep Docker Healthy

```powershell
# Weekly maintenance
docker system prune -f           # Clean unused data
docker image prune -a -f         # Remove unused images  
docker volume prune -f           # Remove unused volumes
docker network prune -f          # Remove unused networks

# Monthly reset
# Run Fix #3 (Docker Daemon Reset) above
```

---

## Emergency: Work Without Docker

You can develop and deploy **without Docker** right now:

### Option 1: Run Directly (Fastest)
```bash
npm install
npm run start:tri-servers
```

### Option 2: Deploy to Azure Without Docker
```bash
# Use Azure App Service (no Docker needed)
az webapp deployment source config-zip \
  --resource-group networkbuster-rg \
  --name networkbuster \
  --src archive.zip
```

### Option 3: Use Vercel (Perfect for Node.js)
```bash
npm install -g vercel
vercel
```

---

## Quick Status Check Script

```powershell
Write-Host "=== Docker Status ===" -ForegroundColor Cyan
docker version 2>$null | Select-Object -First 1
if ($?) { Write-Host "✓ Docker running" -ForegroundColor Green } 
else { Write-Host "✗ Docker NOT running" -ForegroundColor Red }

Write-Host "`n=== Disk Space ===" -ForegroundColor Cyan
Get-PSDrive C | Format-Table @{Name="Free (GB)"; Expression={[math]::Round($_.Free/1GB,2)}}

Write-Host "`n=== NetworkBuster Status ===" -ForegroundColor Cyan
curl -s http://localhost:3000/api/health 2>$null && Write-Host "✓ Web Server OK" || Write-Host "✗ Web Server offline"
curl -s http://localhost:3001/api/health 2>$null && Write-Host "✓ API Server OK" || Write-Host "✗ API Server offline"
curl -s http://localhost:3002/health 2>$null && Write-Host "✓ Audio Server OK" || Write-Host "✗ Audio Server offline"
```

---

## Action Plan

1. **Now:** Try Fix #1 (Restart Docker Desktop)
2. **If still broken:** Try Fix #2 (Reset Engine)
3. **If still broken:** Try Fix #3 (WSL2 check)
4. **If Docker won't work:** Use Azure ACR or run locally without Docker

Your **tri-server system works perfectly without Docker** - you can keep developing and just skip Docker for now!

---

## Support

Need help? Run this diagnostic:

```powershell
Write-Host "Docker Version:" -ForegroundColor Cyan
docker version 2>&1

Write-Host "`nDocker System Info:" -ForegroundColor Cyan  
docker system info 2>&1 | Select-Object -First 20

Write-Host "`nGit Version:" -ForegroundColor Cyan
git --version

Write-Host "`nNode/NPM:" -ForegroundColor Cyan
node --version; npm --version
```

Save output and share for detailed troubleshooting.
