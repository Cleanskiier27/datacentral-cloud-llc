# NetworkBuster Windows Application Installer
# Automated installation with GUI and system integration
# PIN: drew2

param(
    [Parameter(Mandatory=$false)]
    [string]$InstallPath = "C:\Program Files\NetworkBuster",
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateDesktopShortcut = $false
)

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host "ERROR: This installer must run as Administrator!" -ForegroundColor Red
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please right-click PowerShell and select 'Run as administrator'" -ForegroundColor Yellow
    Write-Host "Then run this script again." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Clear-Host

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       NetworkBuster Windows Application Installer           " -ForegroundColor Cyan
Write-Host "              Version 1.0.0 - Personal Use                    " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Installation welcome
Write-Host "Welcome to NetworkBuster Installation" -ForegroundColor Green
Write-Host ""
Write-Host "This installer will:" -ForegroundColor Yellow
Write-Host "  ✓ Check system requirements" -ForegroundColor White
Write-Host "  ✓ Copy files to: $InstallPath" -ForegroundColor White
Write-Host "  ✓ Create Start Menu shortcuts" -ForegroundColor White
Write-Host "  ✓ Create Desktop shortcuts (optional)" -ForegroundColor White
Write-Host "  ✓ Configure PowerShell environment" -ForegroundColor White
Write-Host "  ✓ Create uninstaller" -ForegroundColor White
Write-Host ""

# License confirmation
Write-Host "================================================================" -ForegroundColor DarkGray
Write-Host ""
Write-Host "PERSONAL USE LICENSE" -ForegroundColor Yellow
Write-Host ""
Write-Host "This software is licensed for personal use only." -ForegroundColor White
Write-Host "By installing, you agree to the license terms." -ForegroundColor White
Write-Host ""

$agreeLicense = Read-Host "Do you agree to the Personal Use License? (YES/NO)"

if ($agreeLicense -ne "YES") {
    Write-Host ""
    Write-Host "Installation cancelled." -ForegroundColor Red
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: System Requirements Check
Write-Host "[STEP 1/6] Checking System Requirements..." -ForegroundColor Cyan
Write-Host ""

$osVersion = [System.Environment]::OSVersion.Version
$isWin10Plus = $osVersion.Major -ge 10

if (-not $isWin10Plus) {
    Write-Host "[ERROR] Windows 10 or higher required!" -ForegroundColor Red
    exit 1
}

Write-Host "  [OK] Windows 10/11 detected: $osVersion" -ForegroundColor Green

$psVersion = $PSVersionTable.PSVersion.Major
if ($psVersion -lt 5) {
    Write-Host "[ERROR] PowerShell 5.0+ required!" -ForegroundColor Red
    exit 1
}

Write-Host "  [OK] PowerShell 5.1+ detected: $($PSVersionTable.PSVersion)" -ForegroundColor Green

$diskSpace = (Get-PSDrive C).Free / 1GB
if ($diskSpace -lt 0.1) {
    Write-Host "[ERROR] At least 100MB free disk space required!" -ForegroundColor Red
    exit 1
}

Write-Host "  [OK] Disk space available: $([math]::Round($diskSpace, 1)) GB" -ForegroundColor Green

Write-Host ""
Write-Host "[SUCCESS] All system requirements met!" -ForegroundColor Green
Write-Host ""
Start-Sleep 1

# Step 2: Create Installation Directory
Write-Host "[STEP 2/6] Creating Installation Directory..." -ForegroundColor Cyan
Write-Host ""

if (Test-Path $InstallPath) {
    Write-Host "  [INFO] Path already exists, checking contents..." -ForegroundColor Yellow
    $confirmation = Read-Host "  Reinstall to existing path? (YES/NO)"
    
    if ($confirmation -ne "YES") {
        Write-Host "  Installation cancelled." -ForegroundColor Red
        exit 1
    }
    
    Remove-Item "$InstallPath\scripts" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "$InstallPath\docs" -Recurse -Force -ErrorAction SilentlyContinue
}

New-Item -Path $InstallPath -ItemType Directory -Force -ErrorAction SilentlyContinue | Out-Null
New-Item -Path "$InstallPath\scripts" -ItemType Directory -Force | Out-Null
New-Item -Path "$InstallPath\docs" -ItemType Directory -Force | Out-Null
New-Item -Path "$InstallPath\data" -ItemType Directory -Force | Out-Null

Write-Host "  [OK] Installation directory created: $InstallPath" -ForegroundColor Green
Write-Host ""
Start-Sleep 1

# Step 3: Copy Application Files
Write-Host "[STEP 3/6] Copying Application Files..." -ForegroundColor Cyan
Write-Host ""

# Copy from current location or release folder
$sourceLocations = @(
    "E:\nb powershell",
    "E:\datacentral-cloud-llc",
    (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
)

$sourceFound = $false
$sourcePath = ""

foreach ($location in $sourceLocations) {
    if (Test-Path "$location\scripts\networkbuster-profile.ps1") {
        $sourcePath = $location
        $sourceFound = $true
        break
    }
}

if (-not $sourceFound) {
    Write-Host "[ERROR] Could not find NetworkBuster source files!" -ForegroundColor Red
    Write-Host "  Expected at one of these locations:" -ForegroundColor Yellow
    $sourceLocations | ForEach-Object { Write-Host "    - $_" -ForegroundColor Gray }
    exit 1
}

Write-Host "  [INFO] Source found: $sourcePath" -ForegroundColor Green
Write-Host ""

# Copy scripts
try {
    Copy-Item "$sourcePath\scripts\*.ps1" "$InstallPath\scripts\" -Force -ErrorAction Stop
    Write-Host "  [OK] PowerShell scripts copied" -ForegroundColor Green
    
    Copy-Item "$sourcePath\*.py" "$InstallPath\" -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Python applications copied" -ForegroundColor Green
    
    Copy-Item "$sourcePath\*.txt" "$InstallPath\" -Force -ErrorAction SilentlyContinue
    Copy-Item "$sourcePath\*.md" "$InstallPath\" -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Documentation copied" -ForegroundColor Green
    
    Copy-Item "$sourcePath\requirements.txt" "$InstallPath\" -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Requirements file copied" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to copy files: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Start-Sleep 1

# Step 4: Configure PowerShell
Write-Host "[STEP 4/6] Configuring PowerShell..." -ForegroundColor Cyan
Write-Host ""

# Set execution policy
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Execution policy configured" -ForegroundColor Green
} catch {
    Write-Host "  [WARNING] Could not set execution policy: $_" -ForegroundColor Yellow
}

# Create PowerShell profile entry
$profileContent = @"
# NetworkBuster - Added by installer
if (Test-Path '$InstallPath\scripts\networkbuster-profile.ps1') {
    Write-Host "Loading NetworkBuster..." -ForegroundColor Cyan
    & '$InstallPath\scripts\networkbuster-profile.ps1'
}
"@

Write-Host "  [OK] PowerShell environment configured" -ForegroundColor Green
Write-Host ""
Start-Sleep 1

# Step 5: Create Shortcuts
Write-Host "[STEP 5/6] Creating Shortcuts..." -ForegroundColor Cyan
Write-Host ""

# Get paths
$startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\NetworkBuster"
$desktopPath = "$env:USERPROFILE\Desktop"

# Create Start Menu folder
New-Item -Path $startMenuPath -ItemType Directory -Force -ErrorAction SilentlyContinue | Out-Null

# Create WshShell object for shortcuts
$shell = New-Object -ComObject WScript.Shell

# Main launcher shortcut
$mainShortcut = "$startMenuPath\NetworkBuster.lnk"
$mainLink = $shell.CreateShortCut($mainShortcut)
$mainLink.TargetPath = "powershell.exe"
$mainLink.Arguments = "-ExecutionPolicy Bypass -File `"$InstallPath\scripts\networkbuster-profile.ps1`""
$mainLink.WorkingDirectory = $InstallPath
$mainLink.Description = "NetworkBuster - Cloud Management System"
$mainLink.IconLocation = "C:\Windows\System32\shell32.dll,16"
$mainLink.Save()

Write-Host "  [OK] Start Menu shortcut created: NetworkBuster" -ForegroundColor Green

# Services Dashboard shortcut
$dashboardShortcut = "$startMenuPath\Services Dashboard.lnk"
$dashboardLink = $shell.CreateShortCut($dashboardShortcut)
$dashboardLink.TargetPath = "powershell.exe"
$dashboardLink.Arguments = "-ExecutionPolicy Bypass -File `"$InstallPath\scripts\services-dashboard.ps1`""
$dashboardLink.WorkingDirectory = $InstallPath
$dashboardLink.Description = "NetworkBuster Services Dashboard"
$dashboardLink.IconLocation = "C:\Windows\System32\imageres.dll,3"
$dashboardLink.Save()

Write-Host "  [OK] Start Menu shortcut created: Services Dashboard" -ForegroundColor Green

# Services Online shortcut
$servicesShortcut = "$startMenuPath\Services Online.lnk"
$servicesLink = $shell.CreateShortCut($servicesShortcut)
$servicesLink.TargetPath = "powershell.exe"
$servicesLink.Arguments = "-ExecutionPolicy Bypass -File `"$InstallPath\scripts\services-online.ps1`""
$servicesLink.WorkingDirectory = $InstallPath
$servicesLink.Description = "NetworkBuster Services Online Tool"
$servicesLink.IconLocation = "C:\Windows\System32\imageres.dll,81"
$servicesLink.Save()

Write-Host "  [OK] Start Menu shortcut created: Services Online" -ForegroundColor Green

# Uninstall shortcut
$uninstallShortcut = "$startMenuPath\Uninstall.lnk"
$uninstallLink = $shell.CreateShortCut($uninstallShortcut)
$uninstallLink.TargetPath = "powershell.exe"
$uninstallLink.Arguments = "-ExecutionPolicy Bypass -File `"$InstallPath\uninstall.ps1`""
$uninstallLink.WorkingDirectory = $InstallPath
$uninstallLink.Description = "Uninstall NetworkBuster"
$uninstallLink.IconLocation = "C:\Windows\System32\imageres.dll,108"
$uninstallLink.Save()

Write-Host "  [OK] Start Menu shortcut created: Uninstall" -ForegroundColor Green

# Optional desktop shortcuts
if ($CreateDesktopShortcut) {
    Copy-Item $mainShortcut "$desktopPath\NetworkBuster.lnk" -Force
    Write-Host "  [OK] Desktop shortcut created: NetworkBuster" -ForegroundColor Green
}

Write-Host ""
Start-Sleep 1

# Step 6: Create Uninstaller
Write-Host "[STEP 6/6] Creating Uninstaller..." -ForegroundColor Cyan
Write-Host ""

$uninstallerContent = @"
# NetworkBuster Uninstaller

`$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not `$isAdmin) {
    Write-Host "This uninstaller must run as Administrator!" -ForegroundColor Red
    exit 1
}

Clear-Host

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       NetworkBuster Uninstaller                             " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This will completely remove NetworkBuster from your system." -ForegroundColor Yellow
Write-Host ""

`$confirm = Read-Host "Are you sure? (YES/NO)"

if (`$confirm -ne "YES") {
    Write-Host "Uninstall cancelled." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "Removing files..." -ForegroundColor Cyan

# Remove installation directory
Remove-Item "$InstallPath" -Recurse -Force -ErrorAction SilentlyContinue

# Remove Start Menu shortcuts
Remove-Item "`$env:APPDATA\Microsoft\Windows\Start Menu\Programs\NetworkBuster" -Recurse -Force -ErrorAction SilentlyContinue

# Remove desktop shortcuts
Remove-Item "`$env:USERPROFILE\Desktop\NetworkBuster.lnk" -Force -ErrorAction SilentlyContinue

Write-Host "[OK] Files removed" -ForegroundColor Green
Write-Host ""
Write-Host "[SUCCESS] NetworkBuster has been uninstalled." -ForegroundColor Green
Write-Host ""
Write-Host "Thank you for using NetworkBuster!" -ForegroundColor Cyan
Write-Host ""

Start-Sleep 3
"@

$uninstallerContent | Out-File "$InstallPath\uninstall.ps1" -Encoding UTF8

Write-Host "  [OK] Uninstaller created" -ForegroundColor Green
Write-Host ""

# Installation Summary
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[SUCCESS] Installation Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Installation Summary:" -ForegroundColor Yellow
Write-Host "  Install Path: $InstallPath" -ForegroundColor White
Write-Host "  Start Menu: Programs > NetworkBuster" -ForegroundColor White
Write-Host "  PIN Code: drew2" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Start > NetworkBuster (launch main app)" -ForegroundColor White
Write-Host "  2. Use nb-dashboard command in PowerShell" -ForegroundColor White
Write-Host "  3. Try: nb-help for all available commands" -ForegroundColor White
Write-Host ""
Write-Host "Quick Commands:" -ForegroundColor Yellow
Write-Host "  nb-dashboard   - Services management dashboard" -ForegroundColor White
Write-Host "  nb-services    - Interactive services tool" -ForegroundColor White
Write-Host "  nb-apps        - View all apps" -ForegroundColor White
Write-Host "  nb-k8s         - Kubernetes training" -ForegroundColor White
Write-Host "  nb-help        - Show all commands" -ForegroundColor White
Write-Host ""
Write-Host "To Uninstall:" -ForegroundColor Yellow
Write-Host "  Start > NetworkBuster > Uninstall" -ForegroundColor White
Write-Host "  OR: C:\Program Files\NetworkBuster\uninstall.ps1" -ForegroundColor White
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Offer to launch
$launch = Read-Host "Launch NetworkBuster now? (Y/N)"

if ($launch -eq "Y") {
    Write-Host ""
    Write-Host "Launching NetworkBuster..." -ForegroundColor Green
    Write-Host ""
    Start-Sleep 1
    
    & powershell.exe -ExecutionPolicy Bypass -File "$InstallPath\scripts\networkbuster-profile.ps1"
}

Write-Host ""
Write-Host "Installation finished!" -ForegroundColor Green
Write-Host ""
