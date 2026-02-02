# NetworkBuster Application Uninstaller
# Windows app cleanup and removal

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host "ERROR: This uninstaller must run as Administrator!" -ForegroundColor Red
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host ""
    exit 1
}

Clear-Host

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       NetworkBuster Application Uninstaller                 " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This will completely remove NetworkBuster from your system." -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Are you sure you want to uninstall? (YES/NO)"

if ($confirm -ne "YES") {
    Write-Host ""
    Write-Host "Uninstall cancelled." -ForegroundColor Green
    Write-Host ""
    exit 0
}

Write-Host ""
Write-Host "[INFO] Starting uninstall process..." -ForegroundColor Cyan
Write-Host ""

$InstallPath = "C:\Program Files\NetworkBuster"

# Remove installation directory
if (Test-Path $InstallPath) {
    Write-Host "[1/3] Removing installation files..." -ForegroundColor Cyan
    Remove-Item $InstallPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Installation directory removed" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[INFO] Installation directory not found (already removed?)" -ForegroundColor Yellow
    Write-Host ""
}

# Remove Start Menu shortcuts
Write-Host "[2/3] Removing Start Menu shortcuts..." -ForegroundColor Cyan
$startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\NetworkBuster"

if (Test-Path $startMenuPath) {
    Remove-Item $startMenuPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Start Menu shortcuts removed" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[INFO] Start Menu shortcuts not found" -ForegroundColor Yellow
    Write-Host ""
}

# Remove desktop shortcuts
Write-Host "[3/3] Removing desktop shortcuts..." -ForegroundColor Cyan
$desktopPath = "$env:USERPROFILE\Desktop"
$desktopShortcut = "$desktopPath\NetworkBuster.lnk"

if (Test-Path $desktopShortcut) {
    Remove-Item $desktopShortcut -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Desktop shortcut removed" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[INFO] Desktop shortcut not found" -ForegroundColor Yellow
    Write-Host ""
}

# Summary
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[SUCCESS] NetworkBuster has been uninstalled!" -ForegroundColor Green
Write-Host ""
Write-Host "All files and shortcuts have been removed from your system." -ForegroundColor White
Write-Host ""
Write-Host "Thank you for using NetworkBuster!" -ForegroundColor Cyan
Write-Host ""
Write-Host "If you have any feedback, please visit:" -ForegroundColor Yellow
Write-Host "  https://github.com/Cleanskiier27/datacentral-cloud-llc" -ForegroundColor White
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Start-Sleep 3
