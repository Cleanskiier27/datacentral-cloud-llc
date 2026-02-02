# NetworkBuster Installation Guide

## Step 1: System Requirements

- Windows 10/11 (64-bit)
- PowerShell 5.1 or higher
- Administrator privileges
- 2GB free disk space

## Step 2: Extract Files

Extract the release package to:
- Recommended: E:\nb powershell\
- Alternative: C:\NetworkBuster\

## Step 3: Configure Execution Policy

Open PowerShell as Administrator and run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 4: Run Initial Setup

Navigate to the scripts directory:

```powershell
cd "E:\nb powershell\scripts"
.\networkbuster-profile.ps1
```

## Step 5: Verify Installation

Run the following command:

```powershell
nb-help
```

You should see all available NetworkBuster commands.

## Optional Components

### Install Python Apps (Robot Recycling)

```powershell
cd "E:\nb powershell"
pip install -r requirements.txt
python robot_recycling_app.py
```

### Install Kubernetes Training

1. Install MicroK8s
2. Navigate to kubernetes-training/
3. Follow README.md instructions

## Troubleshooting

### Scripts won't run
- Check execution policy: Get-ExecutionPolicy
- Run as Administrator
- Use: -ExecutionPolicy Bypass flag

### Python apps fail
- Verify Python 3.8+ installed
- Install dependencies: pip install -r requirements.txt

### Permission errors
- Ensure Administrator privileges
- Check antivirus isn't blocking scripts

## Security PIN

Default PIN: **drew2**

Change PIN in:
- scripts\sudo-pin-lock.ps1
- All script files with PIN verification

---

For additional help, see README.md
