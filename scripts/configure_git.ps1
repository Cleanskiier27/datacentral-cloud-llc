# NetworkBuster Git Configuration Script (Windows)
# Sets up git credentials for automated distribution downloads

param(
    [string]$GitUsername = "",
    [string]$GitEmail = "",
    [string]$Protocol = "https"
)

Write-Host "🔑 NetworkBuster Git Configuration Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Get git username and email if not provided
if ([string]::IsNullOrEmpty($GitUsername)) {
    $GitUsername = Read-Host "Enter your GitHub username"
}

if ([string]::IsNullOrEmpty($GitEmail)) {
    $GitEmail = Read-Host "Enter your GitHub email"
}

if ([string]::IsNullOrEmpty($Protocol)) {
    $Protocol = Read-Host "Use SSH or HTTPS? (ssh/https) [default: https]"
    if ([string]::IsNullOrEmpty($Protocol)) { $Protocol = "https" }
}

# Configure git globally
Write-Host "`n🔧 Configuring global git settings..." -ForegroundColor Yellow
git config --global user.name "$GitUsername"
git config --global user.email "$GitEmail"

Write-Host "✅ Git user configured:" -ForegroundColor Green
Write-Host "   Username: $GitUsername"
Write-Host "   Email: $GitEmail"

# Configure local repository
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot
Write-Host "`n🔧 Configuring local repository..." -ForegroundColor Yellow
git config user.name "$GitUsername"
git config user.email "$GitEmail"
Write-Host "✅ Local repository configured" -ForegroundColor Green

# Configure protocol
if ($Protocol -eq "ssh") {
    Write-Host "`n🔐 Configuring SSH..." -ForegroundColor Yellow
    git config url."git@github.com:".insteadOf "https://github.com/"
    Write-Host "✅ SSH configured" -ForegroundColor Green
}
else {
    Write-Host "`n📦 Configuring HTTPS..." -ForegroundColor Yellow
    # Windows uses credential manager automatically
    Write-Host "✅ HTTPS configured (Windows Credential Manager will handle authentication)" -ForegroundColor Green
}

# Create configuration directory
Write-Host "`n📁 Setting up configuration..." -ForegroundColor Yellow
$ConfigDir = Join-Path $env:USERPROFILE ".networkbuster"
if (-not (Test-Path $ConfigDir)) {
    New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null
}

# Create config.json
$ConfigFile = Join-Path $ConfigDir "config.json"
$Config = @{
    git_username = $GitUsername
    git_email = $GitEmail
    repository = "datacentral-cloud-llc"
    owner = "Cleanskiier27"
    protocol = $Protocol
    auto_download = $true
    distribution_path = "./dist"
} | ConvertTo-Json

$Config | Out-File -FilePath $ConfigFile -Encoding UTF8 -Force
Write-Host "✅ Configuration saved to $ConfigFile" -ForegroundColor Green

# Display summary
Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "✅ Git Configuration Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "You can now:" -ForegroundColor Yellow
Write-Host "  1. Run the WebApp: python webapp/app.py"
Write-Host "  2. Build distributions: python scripts/build_distro.py"
Write-Host "  3. Download distributions: curl http://localhost:5000/download"
Write-Host ""
Write-Host "Git Credentials:" -ForegroundColor Cyan
Write-Host "  Username: $GitUsername"
Write-Host "  Protocol: $Protocol"
