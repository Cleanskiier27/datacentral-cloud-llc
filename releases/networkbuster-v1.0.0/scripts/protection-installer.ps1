# NetworkBuster Protection Installer for Windows/WSL
# Installs protection against unauthorized sudo usage

param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "install"
)

# Require Administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ ERROR: This script requires Administrator privileges" -ForegroundColor Red
    exit 1
}

Write-Host "🛡️ NetworkBuster Protection Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

function Install-Protection {
    Write-Host "🔒 Installing NetworkBuster Protection System..." -ForegroundColor Yellow
    
    # Configure Git for protection
    wsl git config --global user.email "cadil@networkbuster.local"
    wsl git config --global user.name "NetworkBuster"
    
    # Make protection script executable
    wsl chmod +x ./scripts/protection.sh
    
    # Install as root
    Write-Host "📦 Installing protection service..." -ForegroundColor Yellow
    wsl -u root bash -c "./scripts/protection.sh install"
    
    # Create Windows scheduled task to monitor WSL
    $taskName = "NetworkBusterProtection"
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -Command `"wsl -u root bash -c '/home/networkbuster/datacentral-cloud-llc/scripts/protection.sh monitor'`""
    $trigger = New-ScheduledTaskTrigger -AtStartup
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Force | Out-Null
    
    Write-Host "✅ Protection system installed successfully!" -ForegroundColor Green
    Write-Host "⚠️  Any unauthorized sudo usage will trigger system reboot" -ForegroundColor Yellow
}

function Uninstall-Protection {
    Write-Host "🔓 Removing NetworkBuster Protection..." -ForegroundColor Yellow
    
    # Uninstall service
    wsl -u root bash -c "./scripts/protection.sh uninstall"
    
    # Remove scheduled task
    Unregister-ScheduledTask -TaskName "NetworkBusterProtection" -Confirm:$false -ErrorAction SilentlyContinue
    
    Write-Host "✅ Protection system removed" -ForegroundColor Green
}

function Get-ProtectionStatus {
    Write-Host "📊 Protection Status:" -ForegroundColor Cyan
    wsl bash -c "./scripts/protection.sh status"
    
    Write-Host "`n📋 Windows Scheduled Task:" -ForegroundColor Cyan
    $task = Get-ScheduledTask -TaskName "NetworkBusterProtection" -ErrorAction SilentlyContinue
    if ($task) {
        Write-Host "Status: Running ✅" -ForegroundColor Green
    } else {
        Write-Host "Status: Not Installed ⚠️" -ForegroundColor Yellow
    }
}

# Main execution
switch ($Action.ToLower()) {
    "install" {
        Install-Protection
    }
    "uninstall" {
        Uninstall-Protection
    }
    "status" {
        Get-ProtectionStatus
    }
    default {
        Write-Host "Usage: .\protection-installer.ps1 [-Action install|uninstall|status]" -ForegroundColor White
        Write-Host "  install   - Install protection system" -ForegroundColor Gray
        Write-Host "  uninstall - Remove protection system" -ForegroundColor Gray
        Write-Host "  status    - Check protection status" -ForegroundColor Gray
    }
}
