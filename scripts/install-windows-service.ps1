<#
install-windows-service.ps1
Registers the NetworkBuster nb-apps Docker Compose stack (incl. Nexus
Connector/Engine) to start automatically on Windows.

Prefers NSSM (https://nssm.cc, if already installed and on PATH) to create a
real Windows Service that the Service Control Manager can start/stop/restart.
When NSSM isn't available, falls back to a SYSTEM-level Scheduled Task that
starts the stack at boot (same convention as install-worker-schtask.ps1),
since Windows has no built-in way to run an arbitrary script as an SCM service.

Usage:
    .\install-windows-service.ps1 -Action install
    .\install-windows-service.ps1 -Action uninstall
#>

param(
    [ValidateSet('install','uninstall')]
    [string]$Action = 'install',
    [string]$ServiceName = 'NetworkBusterNexus',
    [string]$StackDir = "$PSScriptRoot\..\kubernetes-training\nb-apps"
)

$ErrorActionPreference = 'Stop'

function Test-IsAdmin {
    $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-IsAdmin)) {
    Write-Output "Elevation required. Relaunching with elevation..."
    $argList = @('-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"",'-Action',$Action,'-ServiceName',"`"$ServiceName`"",'-StackDir',"`"$StackDir`"")
    Start-Process -FilePath (Get-Command powershell.exe).Source -ArgumentList ($argList -join ' ') -Verb RunAs -Wait
    exit $LASTEXITCODE
}

$StackDir = (Resolve-Path $StackDir).Path
$nssm = Get-Command nssm.exe -ErrorAction SilentlyContinue
$docker = Get-Command docker.exe -ErrorAction SilentlyContinue
if (-not $docker) { Write-Error "Docker Desktop / docker.exe not found on PATH."; exit 1 }

if ($Action -eq 'uninstall') {
    if ($nssm) {
        & $nssm.Source stop $ServiceName 2>$null | Out-Null
        & $nssm.Source remove $ServiceName confirm 2>$null | Out-Null
        Write-Output "Removed Windows Service '$ServiceName' (nssm)."
    }
    $taskExists = @(schtasks /Query /TN $ServiceName 2>$null).Count -gt 0
    if ($taskExists) {
        schtasks /Delete /TN $ServiceName /F | Out-Null
        Write-Output "Removed Scheduled Task '$ServiceName'."
    }
    exit 0
}

# --- install ---
Push-Location $StackDir
& $docker.Source compose build
Pop-Location

if ($nssm) {
    Write-Output "nssm.exe detected -- registering a real Windows Service."
    & $nssm.Source install $ServiceName $docker.Source "compose up"
    & $nssm.Source set $ServiceName AppDirectory $StackDir
    & $nssm.Source set $ServiceName Start SERVICE_AUTO_START
    & $nssm.Source set $ServiceName AppStdout "$StackDir\nexus-service.log"
    & $nssm.Source set $ServiceName AppStderr "$StackDir\nexus-service.log"
    & $nssm.Source set $ServiceName AppExit Default Restart
    & $nssm.Source start $ServiceName
    Write-Output "Windows Service '$ServiceName' installed and started."
    Write-Output "Manage with: Get-Service $ServiceName | sc.exe query $ServiceName"
} else {
    Write-Output "nssm.exe not found on PATH -- falling back to a SYSTEM Scheduled Task at startup."
    $tr = "`"$($docker.Source)`" compose -f `"$StackDir\docker-compose.yml`" up -d"
    $exists = @(schtasks /Query /TN $ServiceName 2>$null).Count -gt 0
    if ($exists) { schtasks /Delete /TN $ServiceName /F | Out-Null }
    schtasks /Create /TN $ServiceName /TR $tr /SC ONSTART /RL HIGHEST /RU SYSTEM /F | Out-Null
    Write-Output "Scheduled Task '$ServiceName' created to start the stack at boot."
    Write-Output "Install nssm (https://nssm.cc) and re-run this script for true SCM integration."
}
