# NetworkBuster Services Online Management Tool
# Real-time service monitoring and management

param(
    [Parameter(Mandatory=$false)]
    [string]$Filter = "All"
)

Clear-Host

# Banner
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "           NetworkBuster Services Online Tool                  " -ForegroundColor Cyan
Write-Host "              Real-time Service Management                     " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Security PIN: drew2" -ForegroundColor Yellow
Write-Host ""

function Show-ServicesDashboard {
    param([string]$FilterType = "All")
    
    Clear-Host
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "        NetworkBuster Services Management Dashboard            " -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Refreshed: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
    Write-Host "Filter: $FilterType" -ForegroundColor Yellow
    Write-Host ""
    
    # Get services based on filter
    $services = switch ($FilterType) {
        "Running" { Get-Service | Where-Object {$_.Status -eq 'Running'} }
        "Stopped" { Get-Service | Where-Object {$_.Status -eq 'Stopped'} }
        "Critical" { 
            Get-Service | Where-Object {
                $_.Status -eq 'Running' -and 
                ($_.Name -like "*Windows*" -or $_.Name -like "*System*" -or $_.Name -like "*Security*")
            }
        }
        default { Get-Service }
    }
    
    # Statistics
    $total = ($services | Measure-Object).Count
    $running = ($services | Where-Object {$_.Status -eq 'Running'} | Measure-Object).Count
    $stopped = ($services | Where-Object {$_.Status -eq 'Stopped'} | Measure-Object).Count
    
    Write-Host "Statistics:" -ForegroundColor Green
    Write-Host "   Total: $total | Running: $running | Stopped: $stopped" -ForegroundColor White
    Write-Host ""
    Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host ""
    
    # Display services
    $services | Sort-Object Status, DisplayName | Format-Table -AutoSize `
        @{Label="Status"; Expression={if ($_.Status -eq "Running") { "[RUN]" } else { "[STOP]" }}}, `
        @{Label="Service Name"; Expression={$_.Name}}, `
        @{Label="Display Name"; Expression={$_.DisplayName}}, `
        @{Label="Start Type"; Expression={$_.StartType}}
    
    Write-Host ""
    Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
}

function Show-Menu {
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  [1] View All Services" -ForegroundColor White
    Write-Host "  [2] View Running Services" -ForegroundColor Green
    Write-Host "  [3] View Stopped Services" -ForegroundColor Red
    Write-Host "  [4] View Critical Services" -ForegroundColor Cyan
    Write-Host "  [5] Start a Service" -ForegroundColor Green
    Write-Host "  [6] Stop a Service" -ForegroundColor Red
    Write-Host "  [7] Restart a Service" -ForegroundColor Yellow
    Write-Host "  [8] Search Services" -ForegroundColor Cyan
    Write-Host "  [R] Refresh" -ForegroundColor Gray
    Write-Host "  [Q] Quit" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host -NoNewline "Select option: "
}

function Start-ServiceByName {
    $serviceName = Read-Host "Enter service name"
    try {
        Start-Service -Name $serviceName -ErrorAction Stop
        Write-Host "[SUCCESS] Service '$serviceName' started successfully" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] $_" -ForegroundColor Red
    }
    Start-Sleep 2
}

function Stop-ServiceByName {
    $serviceName = Read-Host "Enter service name"
    $confirm = Read-Host "Are you sure you want to stop '$serviceName'? (Y/N)"
    if ($confirm -eq 'Y') {
        try {
            Stop-Service -Name $serviceName -Force -ErrorAction Stop
            Write-Host "[SUCCESS] Service '$serviceName' stopped successfully" -ForegroundColor Green
        } catch {
            Write-Host "[ERROR] $_" -ForegroundColor Red
        }
    }
    Start-Sleep 2
}

function Restart-ServiceByName {
    $serviceName = Read-Host "Enter service name"
    try {
        Restart-Service -Name $serviceName -Force -ErrorAction Stop
        Write-Host "[SUCCESS] Service '$serviceName' restarted successfully" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] $_" -ForegroundColor Red
    }
    Start-Sleep 2
}

function Search-Services {
    $searchTerm = Read-Host "Enter search term"
    Write-Host ""
    Write-Host "Searching for services matching '$searchTerm'..." -ForegroundColor Cyan
    Write-Host ""
    
    Get-Service | Where-Object {
        $_.Name -like "*$searchTerm*" -or $_.DisplayName -like "*$searchTerm*"
    } | Format-Table -AutoSize `
        @{Label="Status"; Expression={if ($_.Status -eq "Running") { "[RUN]" } else { "[STOP]" }}}, `
        @{Label="Service Name"; Expression={$_.Name}}, `
        @{Label="Display Name"; Expression={$_.DisplayName}}
    
    Write-Host ""
    Read-Host "Press Enter to continue"
}

# Main loop
$currentFilter = $Filter

while ($true) {
    Show-ServicesDashboard -FilterType $currentFilter
    Show-Menu
    
    $choice = Read-Host
    
    switch ($choice.ToUpper()) {
        "1" { $currentFilter = "All" }
        "2" { $currentFilter = "Running" }
        "3" { $currentFilter = "Stopped" }
        "4" { $currentFilter = "Critical" }
        "5" { Start-ServiceByName }
        "6" { Stop-ServiceByName }
        "7" { Restart-ServiceByName }
        "8" { Search-Services }
        "R" { }
        "Q" { 
            Write-Host "Exiting NetworkBuster Services Tool..." -ForegroundColor Yellow
            exit 
        }
        default { 
            Write-Host "Invalid option" -ForegroundColor Red
            Start-Sleep 1
        }
    }
}
