# NetworkBuster PowerShell Banner and Profile
# Auto-loads on PowerShell startup

# NetworkBuster ASCII Banner
$banner = @"

    ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
    ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
    ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ 
    ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗ 
    ██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
    ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
                                                                     
    ██████╗ ██╗   ██╗███████╗████████╗███████╗██████╗              
    ██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗             
    ██████╔╝██║   ██║███████╗   ██║   █████╗  ██████╔╝             
    ██╔══██╗██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗             
    ██████╔╝╚██████╔╝███████║   ██║   ███████╗██║  ██║             
    ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝             
                                                                     
           🔑 Security PIN: drew2 | 🔐 Unlimited Access            
"@

Write-Host $banner -ForegroundColor Cyan

# System Information
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║          NetworkBuster Cloud Management System            ║" -ForegroundColor Blue
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""
Write-Host "🌐 System: " -NoNewline -ForegroundColor Green
Write-Host "$env:COMPUTERNAME" -ForegroundColor White
Write-Host "👤 User: " -NoNewline -ForegroundColor Green
Write-Host "$env:USERNAME" -ForegroundColor White
Write-Host "📅 Date: " -NoNewline -ForegroundColor Green
Write-Host (Get-Date -Format "dddd, MMMM dd, yyyy HH:mm:ss") -ForegroundColor White
Write-Host "📁 Location: " -NoNewline -ForegroundColor Green
Write-Host "$PWD" -ForegroundColor White
Write-Host "🔐 PIN: " -NoNewline -ForegroundColor Green
Write-Host "drew2" -ForegroundColor Yellow
Write-Host ""

# Quick Stats
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

# Services Status
$services = Get-Service | Where-Object {$_.Status -eq 'Running'} | Measure-Object
Write-Host "🔧 Running Services: " -NoNewline -ForegroundColor Cyan
Write-Host $services.Count -ForegroundColor White

# Disk Space
$disk = Get-PSDrive C | Select-Object Used,Free
$usedGB = [math]::Round($disk.Used / 1GB, 2)
$freeGB = [math]::Round($disk.Free / 1GB, 2)
Write-Host "💾 C: Drive: " -NoNewline -ForegroundColor Cyan
Write-Host "$usedGB GB used, $freeGB GB free" -ForegroundColor White

# Network
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*"} | Select-Object -First 1).IPAddress
Write-Host "🌐 IP Address: " -NoNewline -ForegroundColor Cyan
Write-Host $ip -ForegroundColor White

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Quick Commands
Write-Host "📌 Quick Commands:" -ForegroundColor Yellow
Write-Host "  nb-services    - List all services online tool" -ForegroundColor Gray
Write-Host "  nb-status      - System status dashboard" -ForegroundColor Gray
Write-Host "  nb-lock        - Lock sudo permissions" -ForegroundColor Gray
Write-Host "  nb-apps        - View all NetworkBuster apps" -ForegroundColor Gray
Write-Host "  nb-k8s         - Kubernetes training resources" -ForegroundColor Gray
Write-Host "  nb-unlock      - Unlock sudo permissions" -ForegroundColor Gray
Write-Host "  nb-help        - Show all commands" -ForegroundColor Gray
Write-Host ""

# Custom Functions
function nb-dashboard {
    Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "E:\nb powershell\scripts\services-dashboard.ps1"
}

function nb-services {
    Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "E:\nb powershell\scripts\services-online.ps1"
}

function nb-status {
    E:\nb powershell\scripts\system-status.ps1
}

function nb-lock {
    E:\datacentral-cloud-llc\scripts\sudo-pin-lock.ps1 -Action lock
}

function nb-unlock {
    E:\datacentral-cloud-llc\scripts\sudo-pin-lock.ps1 -Action unlock
}

function nb-apps {
    E:\datacentral-cloud-llc\scripts\nb-apps-menu.ps1
}

function nb-k8s {
    Set-Location E:\datacentral-cloud-llc\kubernetes-training
    Write-Host "📚 Kubernetes Training Directory" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Get-ChildItem -Recurse -Directory | Format-Table Name, FullName
}

function nb-help {
    Write-Host "NetworkBuster Command Reference" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "System Management:" -ForegroundColor Yellow
    Write-Host "  nb-services  - Services management tool" -ForegroundColor White
    Write-Host "  nb-status    - System status dashboard" -ForegroundColor White
    Write-Host "  nb-lock      - Lock sudo permissions" -ForegroundColor White
    Write-Host "  nb-unlock    - Unlock sudo permissions" -ForegroundColor White
    Write-Host "  nb-apps      - View all NetworkBuster apps" -ForegroundColor White
    Write-Host "  nb-k8s       - Kubernetes training resources" -ForegroundColor White
    Write-Host ""
    Write-Host "Tools:" -ForegroundColor Yellow
    Write-Host "  E:\datacentral-cloud-llc\robot_recycling_app.py - Robot recycling app" -ForegroundColor White
    Write-Host "  E:\wsl-auto-installer.ps1 - WSL package installer" -ForegroundColor White
    Write-Host ""
}

# Set custom prompt
function prompt {
    $location = Get-Location
    Write-Host "[" -NoNewline -ForegroundColor DarkGray
    Write-Host "NetworkBuster" -NoNewline -ForegroundColor Cyan
    Write-Host "] " -NoNewline -ForegroundColor DarkGray
    Write-Host "$location" -NoNewline -ForegroundColor Green
    Write-Host " $" -NoNewline -ForegroundColor White
    return " "
}

Write-Host "✅ NetworkBuster environment loaded. Type " -NoNewline -ForegroundColor Green
Write-Host "nb-help" -NoNewline -ForegroundColor Yellow
Write-Host " for available commands." -ForegroundColor Green
Write-Host ""
