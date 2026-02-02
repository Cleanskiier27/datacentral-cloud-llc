# NetworkBuster Release Distribution Script
# Creates release packages for distribution
# PIN: drew2

param(
    [Parameter(Mandatory=$false)]
    [string]$Version = "1.0.0",
    
    [Parameter(Mandatory=$false)]
    [string]$OutputPath = "E:\nb powershell\releases"
)

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       NetworkBuster Release Distribution Builder             " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Version: $Version" -ForegroundColor Yellow
Write-Host "Security PIN: drew2" -ForegroundColor Yellow
Write-Host ""

# Create release directory
$releaseDir = "$OutputPath\networkbuster-v$Version"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

Write-Host "[INFO] Creating release package..." -ForegroundColor Green
Write-Host ""

# Create directory structure
New-Item -Path $releaseDir -ItemType Directory -Force | Out-Null
New-Item -Path "$releaseDir\scripts" -ItemType Directory -Force | Out-Null
New-Item -Path "$releaseDir\docs" -ItemType Directory -Force | Out-Null
New-Item -Path "$releaseDir\kubernetes-training" -ItemType Directory -Force | Out-Null

# Copy core files
Write-Host "[1/6] Copying core scripts..." -ForegroundColor Cyan
Copy-Item "E:\nb powershell\scripts\*.ps1" "$releaseDir\scripts\" -Force
Copy-Item "E:\nb powershell\scripts\*.sh" "$releaseDir\scripts\" -Force -ErrorAction SilentlyContinue

# Copy Python apps
Write-Host "[2/6] Copying Python applications..." -ForegroundColor Cyan
Copy-Item "E:\nb powershell\*.py" "$releaseDir\" -Force -ErrorAction SilentlyContinue
Copy-Item "E:\nb powershell\requirements.txt" "$releaseDir\" -Force -ErrorAction SilentlyContinue

# Copy Kubernetes training
Write-Host "[3/6] Copying Kubernetes training resources..." -ForegroundColor Cyan
Copy-Item "E:\nb powershell\kubernetes-training\*" "$releaseDir\kubernetes-training\" -Recurse -Force -ErrorAction SilentlyContinue

# Create documentation
Write-Host "[4/6] Generating documentation..." -ForegroundColor Cyan

$readmeContent = @"
# NetworkBuster v$Version

**Security PIN:** drew2  
**Release Date:** $(Get-Date -Format "yyyy-MM-dd")  
**Personal Use License**

## Overview

NetworkBuster is a comprehensive PowerShell-based cloud management and monitoring system.

## Features

- **Services Management Dashboard** - Real-time Windows service monitoring
- **Security Testing Suite** - Ethical security testing for your own systems
- **Robot Recycling Manager** - Flask-based task and inventory management
- **Kubernetes Training** - Complete K8s learning environment
- **Sudo Permission Manager** - PIN-based sudo control for WSL
- **Token Manager** - Authentication token management
- **License Manager** - Personal use licensing

## Installation

### Prerequisites
- Windows 10/11 with PowerShell 5.1+
- WSL2 with Ubuntu (optional)
- Python 3.8+ (optional)
- MicroK8s (optional for Kubernetes training)

### Quick Start

1. Extract the release package to your preferred location
2. Open PowerShell as Administrator
3. Navigate to the scripts directory
4. Run the NetworkBuster profile:

``````powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\scripts\networkbuster-profile.ps1
``````

## Available Commands

- **nb-dashboard** - Launch services management dashboard
- **nb-services** - Open services online tool
- **nb-apps** - View all NetworkBuster applications
- **nb-k8s** - Access Kubernetes training resources
- **nb-security** - Run security testing suite
- **nb-help** - Display all commands

## Security Features

- **PIN Protection:** All tools require PIN authentication (drew2)
- **Personal Use License:** Authorized for personal use only
- **Ethical Testing:** Security tools designed for own-system testing only

## Components

### PowerShell Scripts
- services-dashboard.ps1 - Real-time service monitoring
- services-online.ps1 - Interactive service management
- security-test.ps1 - Security assessment tool
- networkbuster-profile.ps1 - PowerShell profile with banner

### Python Applications
- robot_recycling_app.py - Robot management system (Flask)
- token_manager.py - Token authentication
- personal_license.py - License management

### Kubernetes Training
- Docker Compose configurations
- Kubernetes manifests
- Training documentation
- All 6 NB apps containerized

## Configuration

Security PIN: **drew2**  
Default ports:
- Services Dashboard: Auto-assigned
- Robot Recycling: 5000
- Services in K8s: 8080-8084

## License

Personal Use Only License  
© 2026 NetworkBuster  
Unauthorized distribution or commercial use prohibited.

## Support

For issues or questions:
- Review documentation in docs/ folder
- Check security-reports/ for system analysis
- Refer to kubernetes-training/README.md for K8s help

## Security Notes

⚠️ **Important:**
- Use security testing tools ONLY on systems you own
- Never attempt unauthorized access to systems
- Keep your PIN secure
- Regular security audits recommended

## Version History

### v$Version ($(Get-Date -Format "yyyy-MM-dd"))
- Initial release
- Services management dashboard
- Security testing suite
- Kubernetes training environment
- Complete app suite

---

**NetworkBuster** - Cloud Management System  
*Unlimited Access | Personal Use | PIN: drew2*
"@

$readmeContent | Out-File "$releaseDir\README.md" -Encoding UTF8

# Create installation guide
$installGuide = @"
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

``````powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
``````

## Step 4: Run Initial Setup

Navigate to the scripts directory:

``````powershell
cd "E:\nb powershell\scripts"
.\networkbuster-profile.ps1
``````

## Step 5: Verify Installation

Run the following command:

``````powershell
nb-help
``````

You should see all available NetworkBuster commands.

## Optional Components

### Install Python Apps (Robot Recycling)

``````powershell
cd "E:\nb powershell"
pip install -r requirements.txt
python robot_recycling_app.py
``````

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
"@

$installGuide | Out-File "$releaseDir\docs\INSTALLATION.md" -Encoding UTF8

# Create license file
Write-Host "[5/6] Creating license file..." -ForegroundColor Cyan

$licenseContent = @"
NetworkBuster Personal Use License

Copyright (c) 2026 NetworkBuster

PERSONAL USE ONLY

This software is provided for personal, non-commercial use only.

PERMISSIONS:
- Install and use on personal systems
- Modify for personal use
- Test on systems you own or have authorization to test

RESTRICTIONS:
- NO commercial use
- NO redistribution without permission
- NO warranty provided
- NO liability accepted

SECURITY NOTICE:
Use security testing features only on systems you own or have explicit 
authorization to test. Unauthorized access to computer systems is illegal.

PIN: drew2
Machine Authorized: Personal Use

For licensing inquiries: cadillac.gas@outlook.com
"@

$licenseContent | Out-File "$releaseDir\LICENSE.txt" -Encoding UTF8

# Create checksums
Write-Host "[6/6] Generating checksums..." -ForegroundColor Cyan

$checksums = @()
Get-ChildItem "$releaseDir\scripts" -Filter *.ps1 | ForEach-Object {
    $hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
    $checksums += "$($_.Name): $hash"
}

$checksums | Out-File "$releaseDir\CHECKSUMS.txt"

# Create archive
Write-Host ""
Write-Host "[INFO] Creating release archive..." -ForegroundColor Green

$archivePath = "$OutputPath\networkbuster-v$Version-$timestamp.zip"
Compress-Archive -Path "$releaseDir\*" -DestinationPath $archivePath -Force

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[SUCCESS] Release package created!" -ForegroundColor Green
Write-Host ""
Write-Host "Release Details:" -ForegroundColor Yellow
Write-Host "  Version: $Version" -ForegroundColor White
Write-Host "  Archive: $archivePath" -ForegroundColor White
Write-Host "  Size: $([math]::Round((Get-Item $archivePath).Length / 1MB, 2)) MB" -ForegroundColor White
Write-Host ""
Write-Host "Package Contents:" -ForegroundColor Yellow
Write-Host "  - PowerShell scripts" -ForegroundColor White
Write-Host "  - Python applications" -ForegroundColor White
Write-Host "  - Kubernetes training" -ForegroundColor White
Write-Host "  - Documentation" -ForegroundColor White
Write-Host "  - License file" -ForegroundColor White
Write-Host "  - Checksums" -ForegroundColor White
Write-Host ""

# Open release folder
$openFolder = Read-Host "Open release folder? (Y/N)"
if ($openFolder -eq "Y") {
    explorer $OutputPath
}
