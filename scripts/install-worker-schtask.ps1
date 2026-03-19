<#
install-worker-schtask.ps1
Install or uninstall a Scheduled Task that runs the elevated `run-worker.ps1` at system startup with highest privileges.
Usage:
    .\install-worker-schtask.ps1 -Action install
    .\install-worker-schtask.ps1 -Action uninstall
#>

param(
    [ValidateSet('install','uninstall')]
    [string]$Action = 'install',
    [string]$TaskName = 'NetworkBusterWorker',
    [string]$ScriptPath = "$PSScriptRoot\run-worker.ps1",
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

function Test-IsAdmin {
    $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-IsAdmin)) {
    Write-Output "Elevation required. Relaunching with elevation..."
    $argList = @('-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"")
    if ($Action) { $argList += '-Action'; $argList += $Action }
    if ($TaskName) { $argList += '-TaskName'; $argList += "`"$TaskName`"" }
    if ($ScriptPath) { $argList += '-ScriptPath'; $argList += "`"$ScriptPath`"" }
    if ($Force) { $argList += '-Force' }

    Start-Process -FilePath (Get-Command powershell.exe).Source -ArgumentList ($argList -join ' ') -Verb RunAs -Wait
    exit $LASTEXITCODE
}

$fullScript = (Resolve-Path $ScriptPath).Path

if ($Action -eq 'install') {
    if (-not (Test-Path $fullScript)) { Write-Error "Script not found: $fullScript"; exit 1 }

    # Create scheduled task to run at startup as SYSTEM with highest privileges
    $tr = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$fullScript`""

    # Use schtasks for compatibility
    $exists = (schtasks /Query /TN $TaskName 2>$null) -ne $null
    if ($exists -and -not $Force) {
        Write-Output "A task named '$TaskName' already exists. Use -Force to recreate."
        exit 1
    }

    if ($exists -and $Force) {
        schtasks /Delete /TN $TaskName /F | Out-Null
    }

    schtasks /Create /TN $TaskName /TR $tr /SC ONSTART /RL HIGHEST /RU SYSTEM /F | Out-Null

    Write-Output "Scheduled Task '$TaskName' created to run at startup with highest privileges."
    Write-Output "You can view it in Task Scheduler or with: schtasks /Query /TN $TaskName /V /FO LIST"
    exit 0
}

if ($Action -eq 'uninstall') {
    $exists = (schtasks /Query /TN $TaskName 2>$null) -ne $null
    if (-not $exists) { Write-Output "No scheduled task named '$TaskName' was found."; exit 0 }

    schtasks /Delete /TN $TaskName /F | Out-Null
    Write-Output "Scheduled Task '$TaskName' removed."
    exit 0
}
