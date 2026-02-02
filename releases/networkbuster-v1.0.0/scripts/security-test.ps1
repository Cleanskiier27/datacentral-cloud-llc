# NetworkBuster Security Testing Suite
# Ethical security testing for YOUR OWN systems only
# PIN: drew2

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       NetworkBuster Security Testing Suite v1.0              " -ForegroundColor Cyan
Write-Host "              Ethical Testing - Own Systems Only               " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Security PIN: drew2" -ForegroundColor Yellow
Write-Host ""
Write-Host "WARNING: Use only on systems you own or have explicit authorization to test" -ForegroundColor Red
Write-Host ""

# Verify user authorization
$confirm = Read-Host "Do you confirm you own this system and authorize security testing? (YES/NO)"

if ($confirm -ne "YES") {
    Write-Host ""
    Write-Host "Testing cancelled. Authorization not confirmed." -ForegroundColor Red
    Write-Host ""
    exit
}

Write-Host ""
Write-Host "[INFO] Starting security assessment of local system..." -ForegroundColor Green
Write-Host ""

# Create report directory
$reportDir = "E:\nb powershell\security-reports"
New-Item -Path $reportDir -ItemType Directory -Force | Out-Null
$reportFile = "$reportDir\security-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"

# Initialize report
"NetworkBuster Security Testing Report" | Out-File $reportFile
"Generated: $(Get-Date)" | Out-File $reportFile -Append
"System: $env:COMPUTERNAME" | Out-File $reportFile -Append
"User: $env:USERNAME" | Out-File $reportFile -Append
"" | Out-File $reportFile -Append
"================================================================" | Out-File $reportFile -Append
"" | Out-File $reportFile -Append

function Test-OpenPorts {
    Write-Host "[TEST 1/8] Scanning open network ports..." -ForegroundColor Cyan
    
    $commonPorts = @(21, 22, 23, 25, 53, 80, 135, 139, 443, 445, 3306, 3389, 5432, 8080)
    $openPorts = @()
    
    foreach ($port in $commonPorts) {
        $connection = Test-NetConnection -ComputerName localhost -Port $port -WarningAction SilentlyContinue
        if ($connection.TcpTestSucceeded) {
            $openPorts += $port
            Write-Host "  [OPEN] Port $port" -ForegroundColor Yellow
        }
    }
    
    "TEST 1: Open Ports" | Out-File $reportFile -Append
    "Open ports found: $($openPorts -join ', ')" | Out-File $reportFile -Append
    "" | Out-File $reportFile -Append
}

function Test-FirewallStatus {
    Write-Host "[TEST 2/8] Checking Windows Firewall status..." -ForegroundColor Cyan
    
    $firewallProfiles = Get-NetFirewallProfile
    
    foreach ($profile in $firewallProfiles) {
        $status = if ($profile.Enabled) { "ENABLED" } else { "DISABLED - RISK" }
        $color = if ($profile.Enabled) { "Green" } else { "Red" }
        Write-Host "  [$status] $($profile.Name) Profile" -ForegroundColor $color
        
        "$($profile.Name) Profile: $status" | Out-File $reportFile -Append
    }
    "" | Out-File $reportFile -Append
}

function Test-WindowsUpdates {
    Write-Host "[TEST 3/8] Checking Windows Update status..." -ForegroundColor Cyan
    
    $updateService = Get-Service -Name wuauserv
    $status = $updateService.Status
    $color = if ($status -eq "Running") { "Green" } else { "Yellow" }
    
    Write-Host "  Windows Update Service: $status" -ForegroundColor $color
    
    "Windows Update Service: $status" | Out-File $reportFile -Append
    "" | Out-File $reportFile -Append
}

function Test-PasswordPolicy {
    Write-Host "[TEST 4/8] Analyzing password policy..." -ForegroundColor Cyan
    
    $policy = net accounts
    Write-Host "  Password policy retrieved" -ForegroundColor Green
    
    "Password Policy:" | Out-File $reportFile -Append
    $policy | Out-File $reportFile -Append
    "" | Out-File $reportFile -Append
}

function Test-SharedFolders {
    Write-Host "[TEST 5/8] Checking for network shares..." -ForegroundColor Cyan
    
    $shares = Get-SmbShare | Where-Object {$_.Name -notlike '*$'}
    
    foreach ($share in $shares) {
        Write-Host "  [SHARE] $($share.Name) - $($share.Path)" -ForegroundColor Yellow
        "$($share.Name) - $($share.Path)" | Out-File $reportFile -Append
    }
    "" | Out-File $reportFile -Append
}

function Test-RunningServices {
    Write-Host "[TEST 6/8] Auditing running services..." -ForegroundColor Cyan
    
    $services = Get-Service | Where-Object {$_.Status -eq 'Running'}
    $count = $services.Count
    
    Write-Host "  Total running services: $count" -ForegroundColor Green
    
    "Running Services: $count" | Out-File $reportFile -Append
    "" | Out-File $reportFile -Append
}

function Test-AdminUsers {
    Write-Host "[TEST 7/8] Checking local administrators..." -ForegroundColor Cyan
    
    $admins = Get-LocalGroupMember -Group "Administrators" -ErrorAction SilentlyContinue
    
    foreach ($admin in $admins) {
        Write-Host "  [ADMIN] $($admin.Name)" -ForegroundColor Yellow
        "$($admin.Name)" | Out-File $reportFile -Append
    }
    "" | Out-File $reportFile -Append
}

function Test-SecuritySoftware {
    Write-Host "[TEST 8/8] Detecting security software..." -ForegroundColor Cyan
    
    $defender = Get-Service -Name WinDefend -ErrorAction SilentlyContinue
    if ($defender) {
        $status = $defender.Status
        $color = if ($status -eq "Running") { "Green" } else { "Red" }
        Write-Host "  Windows Defender: $status" -ForegroundColor $color
        "Windows Defender: $status" | Out-File $reportFile -Append
    }
    "" | Out-File $reportFile -Append
}

# Run all tests
Test-OpenPorts
Test-FirewallStatus
Test-WindowsUpdates
Test-PasswordPolicy
Test-SharedFolders
Test-RunningServices
Test-AdminUsers
Test-SecuritySoftware

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[SUCCESS] Security assessment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Report saved to: $reportFile" -ForegroundColor Yellow
Write-Host ""
Write-Host "Recommendations:" -ForegroundColor Cyan
Write-Host "  1. Keep Windows and all software updated" -ForegroundColor White
Write-Host "  2. Enable Windows Firewall on all profiles" -ForegroundColor White
Write-Host "  3. Use strong passwords and enable MFA" -ForegroundColor White
Write-Host "  4. Minimize open ports and unnecessary services" -ForegroundColor White
Write-Host "  5. Regular security audits recommended" -ForegroundColor White
Write-Host ""

# Open report
$openReport = Read-Host "Open report now? (Y/N)"
if ($openReport -eq "Y") {
    notepad $reportFile
}
