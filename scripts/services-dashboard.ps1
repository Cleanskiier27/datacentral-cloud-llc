# NetworkBuster Services Management Dashboard
# Comprehensive real-time service monitoring with statistics and controls

param(
    [Parameter(Mandatory=$false)]
    [int]$RefreshInterval = 5
)

$script:Running = $true

# Dashboard configuration
$DashboardConfig = @{
    Title = "NetworkBuster Services Management Dashboard"
    PIN = "drew2"
    RefreshInterval = $RefreshInterval
    AutoRefresh = $true
}

function Show-Dashboard {
    Clear-Host
    
    # Get current time
    $currentTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    # Header
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "       NETWORKBUSTER SERVICES MANAGEMENT DASHBOARD             " -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Security PIN: drew2  |  Time: $currentTime  " -ForegroundColor Yellow
    Write-Host ""
    Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
    
    # Get all services
    $allServices = Get-Service
    $runningServices = $allServices | Where-Object {$_.Status -eq 'Running'}
    $stoppedServices = $allServices | Where-Object {$_.Status -eq 'Stopped'}
    
    # Statistics
    $totalCount = $allServices.Count
    $runningCount = $runningServices.Count
    $stoppedCount = $stoppedServices.Count
    $runningPercent = [math]::Round(($runningCount / $totalCount) * 100, 1)
    
    # Display statistics
    Write-Host ""
    Write-Host "  SYSTEM STATISTICS" -ForegroundColor Green
    Write-Host "  ----------------" -ForegroundColor Green
    Write-Host "  Total Services    : $totalCount" -ForegroundColor White
    Write-Host "  Running Services  : $runningCount ($runningPercent%)" -ForegroundColor Green
    Write-Host "  Stopped Services  : $stoppedCount" -ForegroundColor Red
    Write-Host ""
    
    # Progress bar for running services
    $barLength = 50
    $filledLength = [math]::Floor(($runningCount / $totalCount) * $barLength)
    $emptyLength = $barLength - $filledLength
    $progressBar = ("#" * $filledLength) + ("-" * $emptyLength)
    Write-Host "  Progress: [$progressBar] $runningPercent%" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
    
    # Critical Windows Services Status
    Write-Host ""
    Write-Host "  CRITICAL SERVICES STATUS" -ForegroundColor Yellow
    Write-Host "  -----------------------" -ForegroundColor Yellow
    
    $criticalServices = @(
        "Dhcp",
        "Dnscache",
        "EventLog",
        "PlugPlay",
        "RpcSs",
        "Schedule",
        "SENS",
        "Themes",
        "Winmgmt",
        "wuauserv"
    )
    
    foreach ($svcName in $criticalServices) {
        $svc = Get-Service -Name $svcName -ErrorAction SilentlyContinue
        if ($svc) {
            $statusColor = if ($svc.Status -eq "Running") { "Green" } else { "Red" }
            $statusText = if ($svc.Status -eq "Running") { "[RUN] " } else { "[STOP]" }
            Write-Host "  $statusText " -NoNewline -ForegroundColor $statusColor
            Write-Host "$($svc.DisplayName)" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
    
    # Recently Changed Services
    Write-Host ""
    Write-Host "  RECENTLY CHANGED SERVICES (Last 5)" -ForegroundColor Magenta
    Write-Host "  ---------------------------------" -ForegroundColor Magenta
    
    $recentServices = Get-Service | Sort-Object Status | Select-Object -First 5
    foreach ($svc in $recentServices) {
        $statusColor = if ($svc.Status -eq "Running") { "Green" } else { "Red" }
        $statusText = if ($svc.Status -eq "Running") { "[RUN] " } else { "[STOP]" }
        Write-Host "  $statusText " -NoNewline -ForegroundColor $statusColor
        Write-Host "$($svc.Name) - $($svc.DisplayName)" -ForegroundColor White
    }
    
    Write-Host ""
    Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
    
    # System Performance Metrics
    Write-Host ""
    Write-Host "  SYSTEM PERFORMANCE" -ForegroundColor Cyan
    Write-Host "  -----------------" -ForegroundColor Cyan
    
    # CPU and Memory
    $cpu = Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average
    $cpuLoad = [math]::Round($cpu.Average, 1)
    
    $os = Get-CimInstance Win32_OperatingSystem
    $totalMemGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
    $freeMemGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
    $usedMemGB = [math]::Round($totalMemGB - $freeMemGB, 2)
    $memPercent = [math]::Round(($usedMemGB / $totalMemGB) * 100, 1)
    
    Write-Host "  CPU Usage         : $cpuLoad%" -ForegroundColor White
    Write-Host "  Memory Usage      : $usedMemGB GB / $totalMemGB GB ($memPercent%)" -ForegroundColor White
    
    # Disk Space
    $disk = Get-PSDrive C
    $diskUsedGB = [math]::Round($disk.Used / 1GB, 2)
    $diskFreeGB = [math]::Round($disk.Free / 1GB, 2)
    $diskTotalGB = $diskUsedGB + $diskFreeGB
    $diskPercent = [math]::Round(($diskUsedGB / $diskTotalGB) * 100, 1)
    
    Write-Host "  C: Drive Usage    : $diskUsedGB GB / $diskTotalGB GB ($diskPercent%)" -ForegroundColor White
    
    # Uptime
    $uptime = (Get-Date) - $os.LastBootUpTime
    $uptimeStr = "$($uptime.Days)d $($uptime.Hours)h $($uptime.Minutes)m"
    Write-Host "  System Uptime     : $uptimeStr" -ForegroundColor White
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    
    # Menu
    Write-Host ""
    Write-Host "  CONTROLS" -ForegroundColor Yellow
    Write-Host "  --------" -ForegroundColor Yellow
    Write-Host "  [V] View All Services  [S] Search Services  [M] Manage Service" -ForegroundColor White
    Write-Host "  [R] Refresh Now        [A] Auto-Refresh: $($DashboardConfig.AutoRefresh)" -ForegroundColor White
    Write-Host "  [Q] Quit Dashboard" -ForegroundColor Gray
    Write-Host ""
    
    if ($DashboardConfig.AutoRefresh) {
        Write-Host "  Auto-refreshing in $RefreshInterval seconds... (Press any key to control)" -ForegroundColor DarkGray
    } else {
        Write-Host "  Press any key to continue..." -ForegroundColor DarkGray
    }
}

function Show-AllServices {
    Clear-Host
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "                    ALL SERVICES VIEW                          " -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    Get-Service | Sort-Object Status, DisplayName | Format-Table -AutoSize `
        @{Label="Status"; Expression={if ($_.Status -eq "Running") { "[RUN]" } else { "[STOP]" }}}, `
        @{Label="Service Name"; Expression={$_.Name}}, `
        @{Label="Display Name"; Expression={$_.DisplayName}}, `
        @{Label="Start Type"; Expression={$_.StartType}}
    
    Write-Host ""
    Read-Host "Press Enter to return to dashboard"
}

function Search-Services {
    Clear-Host
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "                    SEARCH SERVICES                            " -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    $searchTerm = Read-Host "Enter search term (name or display name)"
    
    if ($searchTerm) {
        Write-Host ""
        Write-Host "Search results for: '$searchTerm'" -ForegroundColor Yellow
        Write-Host ""
        
        Get-Service | Where-Object {
            $_.Name -like "*$searchTerm*" -or $_.DisplayName -like "*$searchTerm*"
        } | Format-Table -AutoSize `
            @{Label="Status"; Expression={if ($_.Status -eq "Running") { "[RUN]" } else { "[STOP]" }}}, `
            @{Label="Service Name"; Expression={$_.Name}}, `
            @{Label="Display Name"; Expression={$_.DisplayName}}, `
            @{Label="Start Type"; Expression={$_.StartType}}
    }
    
    Write-Host ""
    Read-Host "Press Enter to return to dashboard"
}

function Manage-Service {
    Clear-Host
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "                    MANAGE SERVICE                             " -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    $serviceName = Read-Host "Enter service name"
    
    if ($serviceName) {
        $svc = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
        
        if ($svc) {
            Write-Host ""
            Write-Host "Service: $($svc.DisplayName)" -ForegroundColor Green
            Write-Host "Name: $($svc.Name)" -ForegroundColor White
            Write-Host "Status: $($svc.Status)" -ForegroundColor Yellow
            Write-Host "Start Type: $($svc.StartType)" -ForegroundColor White
            Write-Host ""
            Write-Host "Actions:" -ForegroundColor Yellow
            Write-Host "  [1] Start Service" -ForegroundColor Green
            Write-Host "  [2] Stop Service" -ForegroundColor Red
            Write-Host "  [3] Restart Service" -ForegroundColor Yellow
            Write-Host "  [Q] Cancel" -ForegroundColor Gray
            Write-Host ""
            
            $action = Read-Host "Select action"
            
            switch ($action) {
                "1" {
                    try {
                        Start-Service -Name $serviceName -ErrorAction Stop
                        Write-Host "[SUCCESS] Service started" -ForegroundColor Green
                    } catch {
                        Write-Host "[ERROR] $_" -ForegroundColor Red
                    }
                }
                "2" {
                    try {
                        Stop-Service -Name $serviceName -Force -ErrorAction Stop
                        Write-Host "[SUCCESS] Service stopped" -ForegroundColor Green
                    } catch {
                        Write-Host "[ERROR] $_" -ForegroundColor Red
                    }
                }
                "3" {
                    try {
                        Restart-Service -Name $serviceName -Force -ErrorAction Stop
                        Write-Host "[SUCCESS] Service restarted" -ForegroundColor Green
                    } catch {
                        Write-Host "[ERROR] $_" -ForegroundColor Red
                    }
                }
            }
        } else {
            Write-Host "[ERROR] Service not found: $serviceName" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Start-Sleep 2
}

# Main loop
while ($script:Running) {
    Show-Dashboard
    
    if ($DashboardConfig.AutoRefresh) {
        # Wait for refresh interval or key press
        $timeout = $RefreshInterval
        $startTime = Get-Date
        
        while (((Get-Date) - $startTime).TotalSeconds -lt $timeout) {
            if ([Console]::KeyAvailable) {
                $key = [Console]::ReadKey($true)
                
                switch ($key.Key) {
                    'V' { Show-AllServices }
                    'S' { Search-Services }
                    'M' { Manage-Service }
                    'R' { break }
                    'A' { 
                        $DashboardConfig.AutoRefresh = -not $DashboardConfig.AutoRefresh
                        break
                    }
                    'Q' { 
                        $script:Running = $false
                        break
                    }
                }
                break
            }
            Start-Sleep -Milliseconds 100
        }
    } else {
        # Wait for key press
        $key = [Console]::ReadKey($true)
        
        switch ($key.Key) {
            'V' { Show-AllServices }
            'S' { Search-Services }
            'M' { Manage-Service }
            'R' { }
            'A' { $DashboardConfig.AutoRefresh = -not $DashboardConfig.AutoRefresh }
            'Q' { $script:Running = $false }
        }
    }
}

Clear-Host
Write-Host ""
Write-Host "NetworkBuster Services Dashboard closed." -ForegroundColor Green
Write-Host ""
