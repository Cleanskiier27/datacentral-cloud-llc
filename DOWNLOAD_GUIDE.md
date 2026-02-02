# NetworkBuster Distribution Download Guide

## Overview
After configuring Git credentials, you can download and manage NetworkBuster distributions through multiple methods:
- **Local WebApp**: Download from the Flask web interface
- **GitHub Releases**: Download from GitHub releases page
- **Direct CLI**: Use the download manager script

## Prerequisites
1. Git installed and configured
2. Python 3.9+
3. Dependencies installed: `pip install -r requirements.txt`

## Step 1: Configure Git Username

### On Windows (PowerShell):
```powershell
.\scripts\configure_git.ps1
```

When prompted:
- Enter your GitHub username
- Enter your GitHub email
- Choose SSH or HTTPS protocol

### On Linux/macOS (Bash):
```bash
chmod +x scripts/configure_git.sh
./scripts/configure_git.sh
```

This creates a configuration file at `~/.networkbuster/config.json`

## Step 2: Download Distributions

### Method 1: Local WebApp (Recommended)

**Start the WebApp:**
```bash
python webapp/app.py
```

**Available endpoints:**
- `GET /` - Web interface with Flash Commands
- `GET /download` - Download latest distribution
- `GET /distro-info` - List available distributions
- `POST /execute/<cmd_id>` - Execute flash commands

**Using curl to download:**
```bash
# Download latest distribution
curl -O http://localhost:5000/download

# Get distribution info
curl http://localhost:5000/distro-info
```

**Using Python requests:**
```python
import requests

# Get distro info
info = requests.get('http://localhost:5000/distro-info').json()
print(info)

# Download latest
response = requests.get('http://localhost:5000/download', stream=True)
with open('networkbuster-distro.zip', 'wb') as f:
    f.write(response.content)
```

### Method 2: Distribution Download Manager

**List available distributions:**
```bash
python scripts/distro_download_manager.py --list
```

**Download from local WebApp:**
```bash
python scripts/distro_download_manager.py --local
```

**Download from GitHub releases:**
```bash
python scripts/distro_download_manager.py --github
python scripts/distro_download_manager.py --github --tag v1.0.0
```

**Extract after download:**
```bash
python scripts/distro_download_manager.py --extract ./dist/networkbuster-distro-*.zip --extract-to ./my-distro
```

### Method 3: Direct Build and Deploy

```bash
# Build distribution
python scripts/build_distro.py

# WebApp will immediately serve the latest build at /download
```

## Configuration File

The git configuration is stored at `~/.networkbuster/config.json`:

```json
{
  "git_username": "your-github-username",
  "git_email": "your-email@example.com",
  "repository": "datacentral-cloud-llc",
  "owner": "Cleanskiier27",
  "protocol": "https",
  "auto_download": true,
  "distribution_path": "./dist"
}
```

## Troubleshooting

### Authentication Issues
If you encounter authentication errors:

```bash
# Clear cached credentials
git credential-cache exit

# Reconfigure git
python scripts/configure_git.ps1  # Windows
./scripts/configure_git.sh        # Linux/macOS
```

### WebApp Connection Issues
```bash
# Check if WebApp is running on port 5000
netstat -an | grep 5000

# Change port if needed
export FLASK_PORT=5001
python webapp/app.py
```

### Download Manager Not Finding Distributions
```bash
# Ensure dist directory exists
mkdir -p dist

# Build a distribution first
python scripts/build_distro.py

# Then download
python scripts/distro_download_manager.py --list
```

## Flash Commands Available

Once configured, you can use Flash Commands through the WebApp:

1. **Build Distro** - Packages the application
   ```bash
   curl -X POST http://localhost:5000/execute/build
   ```

2. **Run AI Training** - Executes neural network pipeline
   ```bash
   curl -X POST http://localhost:5000/execute/train
   ```

3. **Check Status** - Lists active tokens and system health
   ```bash
   curl -X POST http://localhost:5000/execute/status
   ```

## Automated Downloads

For CI/CD pipelines, use the download manager in scripts:

```bash
#!/bin/bash
python scripts/distro_download_manager.py --local \
  --webapp-url http://build-server:5000 && \
python scripts/distro_download_manager.py --extract \
  --extract-to /opt/networkbuster
```

## Security Notes

- Git credentials are stored securely using OS-native methods
- SSH keys should be added to your SSH agent for automated downloads
- HTTPS connections verify SSL certificates by default
- WebApp runs on localhost:5000 by default (use reverse proxy for production)

## Support

For issues or questions:
1. Check the configuration file is valid
2. Verify git credentials with `git config --global --list`
3. Ensure WebApp is running: `python webapp/app.py`
4. Check network connectivity to download servers

---
**NetworkBuster Distribution Management System** | v1.0.0
