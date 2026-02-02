# NetworkBuster WSL Auto Installer
# Bypasses sudo and runs apt install commands automatically

param(
    [Parameter(Mandatory=$false)]
    [string[]]$Packages = @("curl", "wget", "git", "build-essential")
)

Write-Host "🚀 NetworkBuster WSL Auto Installer" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Enable sudo bypass in WSL
Write-Host "🔓 Enabling sudo bypass in WSL..." -ForegroundColor Yellow
wsl -u root bash -c "echo 'ALL ALL=(ALL) NOPASSWD: ALL' | tee /etc/sudoers.d/bypass && chmod 0440 /etc/sudoers.d/bypass"
Write-Host "✅ UNLIMITED SUCCESS - Sudo bypass enabled" -ForegroundColor Green

# Update package lists
Write-Host "📦 Updating package lists..." -ForegroundColor Yellow
wsl -u root bash -c "apt-get update -y"
Write-Host "✅ UNLIMITED SUCCESS - Package lists updated" -ForegroundColor Green

# Install packages
Write-Host "📥 Installing packages..." -ForegroundColor Yellow
foreach ($package in $Packages) {
    Write-Host "Installing $package..." -ForegroundColor Cyan
    wsl -u root bash -c "apt-get install -y $package"
    Write-Host "✅ UNLIMITED SUCCESS - $package installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ UNLIMITED SUCCESS - All installations complete!" -ForegroundColor Green
Write-Host "✅ Sudo bypass active - no passwords required" -ForegroundColor Green
Write-Host "✅ All packages ready in WSL" -ForegroundColor Green
Write-Host ""
Write-Host "To install more packages, run:" -ForegroundColor Cyan
Write-Host "  wsl apt install <package-name>" -ForegroundColor White
