# NetworkBuster Sudo Manager for Windows/WSL
# Restricts sudo access to admin only with local machine access

param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "status"
)

# Require Administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ ERROR: This script requires Administrator privileges" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "🔒 NetworkBuster Sudo Manager" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

function Disable-WSLPasswordlessSudo {
    Write-Host "🛡️ Disabling passwordless sudo in WSL..." -ForegroundColor Yellow
    
    # Remove passwordless sudo files
    wsl -u root bash -c "rm -f /etc/sudoers.d/networkbuster /etc/sudoers.d/$env:USERNAME 2>/dev/null"
    
    # Restore default sudo configuration (require password)
    wsl -u root bash -c "sed -i '/NOPASSWD/d' /etc/sudoers 2>/dev/null"
    
    Write-Host "✅ Passwordless sudo disabled" -ForegroundColor Green
}

function Enable-AdminOnlyAccess {
    Write-Host "🔐 Configuring admin-only local access..." -ForegroundColor Yellow
    
    # Set WSL to require Windows admin for root access
    $wslConfig = @"
[user]
default=networkbuster

[network]
hostname=localhost

[interop]
enabled=true
appendWindowsPath=false
"@
    
    $wslConfigPath = "$env:USERPROFILE\.wslconfig"
    Set-Content -Path $wslConfigPath -Value $wslConfig -Force
    
    Write-Host "✅ Admin-only access configured" -ForegroundColor Green
    Write-Host "⚠️  Restart WSL with: wsl --shutdown" -ForegroundColor Yellow
}

function Get-SudoStatus {
    Write-Host "📊 Current Sudo Status:" -ForegroundColor Cyan
    Write-Host ""
    
    # Check Windows admin status
    $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
    Write-Host "Windows Admin: $isAdmin" -ForegroundColor $(if($isAdmin){"Green"}else{"Red"})
    
    # Check WSL sudo configuration
    $sudoersCheck = wsl -u root bash -c "ls -la /etc/sudoers.d/ 2>/dev/null | grep -E 'networkbuster|$env:USERNAME' | wc -l"
    $hasSudoers = [int]$sudoersCheck -gt 0
    Write-Host "WSL Passwordless Sudo: $hasSudoers" -ForegroundColor $(if($hasSudoers){"Red"}else{"Green"})
    
    # Check .wslconfig
    $wslConfigExists = Test-Path "$env:USERPROFILE\.wslconfig"
    Write-Host ".wslconfig Present: $wslConfigExists" -ForegroundColor $(if($wslConfigExists){"Green"}else{"Yellow"})
}

# Main execution
switch ($Action.ToLower()) {
    "disable" {
        Disable-WSLPasswordlessSudo
        Enable-AdminOnlyAccess
        Write-Host ""
        Write-Host "✅ Sudo access restricted to admin only" -ForegroundColor Green
        Write-Host "Run 'wsl --shutdown' to apply changes" -ForegroundColor Yellow
    }
    "status" {
        Get-SudoStatus
    }
    "enable" {
        Write-Host "⚠️  Re-enabling passwordless sudo (not recommended)" -ForegroundColor Red
        wsl -u root bash -c "echo '$env:USERNAME ALL=(ALL) NOPASSWD: ALL' | tee /etc/sudoers.d/$env:USERNAME"
        wsl -u root bash -c "chmod 0440 /etc/sudoers.d/$env:USERNAME"
        Write-Host "✅ Passwordless sudo enabled" -ForegroundColor Yellow
    }
    default {
        Write-Host "Usage: .\sudo.ps1 [-Action status|disable|enable]" -ForegroundColor White
        Write-Host "  status  - Check current sudo configuration" -ForegroundColor Gray
        Write-Host "  disable - Disable passwordless sudo (admin only)" -ForegroundColor Gray
        Write-Host "  enable  - Enable passwordless sudo (not recommended)" -ForegroundColor Gray
    }
}
