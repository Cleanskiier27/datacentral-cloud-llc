# NetworkBuster Apps Directory
# Centralized menu for all NB applications

Clear-Host

Write-Host @"
╔══════════════════════════════════════════════════════════════════╗
║              NetworkBuster Applications Directory                ║
║                    All NB Apps in One Place                      ║
╚══════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host ""
Write-Host "🔑 Security PIN: " -NoNewline -ForegroundColor Yellow
Write-Host "drew2" -ForegroundColor White
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# App Registry
$apps = @(
    @{
        Number = "1"
        Name = "Services Management Tool"
        Description = "Real-time service monitoring and management"
        Path = "E:\datacentral-cloud-llc\scripts\services-online.ps1"
        Type = "System"
        Icon = "🔧"
    },
    @{
        Number = "2"
        Name = "Robot Recycling Management"
        Description = "Flask-based robot recycling and task management"
        Path = "E:\datacentral-cloud-llc\robot_recycling_app.py"
        Type = "Web App"
        Icon = "🤖"
    },
    @{
        Number = "3"
        Name = "Sudo Permission Manager"
        Description = "PIN-based sudo lock/unlock system"
        Path = "E:\datacentral-cloud-llc\scripts\sudo-pin-lock.ps1"
        Type = "Security"
        Icon = "🔐"
    },
    @{
        Number = "4"
        Name = "System Status Dashboard"
        Description = "Comprehensive system status monitoring"
        Path = "E:\datacentral-cloud-llc\scripts\system-status.ps1"
        Type = "System"
        Icon = "📊"
    },
    @{
        Number = "5"
        Name = "WSL Auto Installer"
        Description = "Automated package installation for WSL"
        Path = "E:\wsl-auto-installer.ps1"
        Type = "Utility"
        Icon = "📦"
    },
    @{
        Number = "6"
        Name = "Personal License Manager"
        Description = "Personal use authorization and licensing"
        Path = "E:\datacentral-cloud-llc\personal_license.py"
        Type = "Security"
        Icon = "📜"
    },
    @{
        Number = "7"
        Name = "Token Manager"
        Description = "Authentication token management system"
        Path = "E:\datacentral-cloud-llc\token_manager.py"
        Type = "Security"
        Icon = "🎫"
    },
    @{
        Number = "8"
        Name = "NetworkBuster Repository Manager"
        Description = "Repository download and initialization"
        Path = "E:\datacentral-cloud-llc\scripts\networkbuster.sh"
        Type = "Utility"
        Icon = "📂"
    },
    @{
        Number = "9"
        Name = "Protection Monitor"
        Description = "Real-time sudo usage protection"
        Path = "E:\datacentral-cloud-llc\scripts\protection.sh"
        Type = "Security"
        Icon = "🛡️"
    }
)

# Display apps by category
$categories = $apps | Group-Object Type | Sort-Object Name

foreach ($category in $categories) {
    Write-Host "[$($category.Name)]" -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($app in $category.Group | Sort-Object Number) {
        Write-Host "  $($app.Icon) " -NoNewline -ForegroundColor White
        Write-Host "[$($app.Number)] " -NoNewline -ForegroundColor Cyan
        Write-Host "$($app.Name)" -ForegroundColor White
        Write-Host "      $($app.Description)" -ForegroundColor Gray
        Write-Host ""
    }
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""
Write-Host "📌 Options:" -ForegroundColor Yellow
Write-Host "  [1-9]  Launch application" -ForegroundColor White
Write-Host "  [K]    View Kubernetes training directory" -ForegroundColor Cyan
Write-Host "  [L]    List all app paths" -ForegroundColor Gray
Write-Host "  [Q]    Return to prompt" -ForegroundColor DarkGray
Write-Host ""
Write-Host -NoNewline "Select option: "

$choice = Read-Host

switch ($choice.ToUpper()) {
    {$_ -match '^[1-9]$'} {
        $selectedApp = $apps | Where-Object {$_.Number -eq $_}
        if ($selectedApp) {
            Write-Host ""
            Write-Host "🚀 Launching: $($selectedApp.Name)" -ForegroundColor Green
            Write-Host ""
            
            $ext = [System.IO.Path]::GetExtension($selectedApp.Path)
            
            if ($ext -eq ".ps1") {
                Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", $selectedApp.Path
            } elseif ($ext -eq ".py") {
                Start-Process powershell -ArgumentList "-NoExit", "-Command", "python `"$($selectedApp.Path)`""
            } elseif ($ext -eq ".sh") {
                Start-Process powershell -ArgumentList "-NoExit", "-Command", "wsl bash `"$($selectedApp.Path)`""
            }
        }
    }
    "K" {
        Write-Host ""
        Write-Host "📚 Kubernetes Training Directory" -ForegroundColor Cyan
        Write-Host "================================" -ForegroundColor Cyan
        Write-Host ""
        Set-Location E:\datacentral-cloud-llc\kubernetes-training
        Get-ChildItem -Recurse | Format-Table Name, Length, LastWriteTime
        Read-Host "Press Enter to continue"
    }
    "L" {
        Write-Host ""
        Write-Host "📋 All Application Paths" -ForegroundColor Cyan
        Write-Host "========================" -ForegroundColor Cyan
        Write-Host ""
        foreach ($app in $apps | Sort-Object Number) {
            Write-Host "[$($app.Number)] " -NoNewline -ForegroundColor Cyan
            Write-Host $app.Path -ForegroundColor White
        }
        Write-Host ""
        Read-Host "Press Enter to continue"
    }
    "Q" {
        Write-Host "Returning to prompt..." -ForegroundColor Gray
    }
    default {
        Write-Host "Invalid option" -ForegroundColor Red
    }
}
