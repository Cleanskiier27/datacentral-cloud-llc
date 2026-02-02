<#
Run-worker.ps1
Simple elevated worker runner. If not run as Administrator it will re-launch itself with elevation.
Reads config from ../config/worker-config.json and starts background jobs to simulate workers.
#>

param(
    [string]$ConfigPath = "$(Resolve-Path "$PSScriptRoot\..\config\worker-config.json").Path",
    [switch]$NoElevate
)

$ErrorActionPreference = 'Stop'

function Test-IsAdmin {
    $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not $NoElevate -and -not (Test-IsAdmin)) {
    Write-Output "Not elevated. Relaunching with elevation..."
    $argList = @('-ExecutionPolicy','Bypass','-File', "`"$PSCommandPath`"")

    if ($ConfigPath) { $argList += '-ConfigPath'; $argList += "`"$ConfigPath`"" }
    if ($NoElevate) { $argList += '-NoElevate' }

    Start-Process -FilePath (Get-Command powershell.exe).Source -ArgumentList ($argList -join ' ') -Verb RunAs -Wait
    exit $LASTEXITCODE
}

if (-not (Test-Path $ConfigPath)) {
    Write-Error "Config file not found: $ConfigPath"
    exit 1
}

$config = Get-Content $ConfigPath | ConvertFrom-Json
$numWorkers = [int]($config.numWorkers | ForEach-Object { $_ })
$interval = [int]($config.pollIntervalSeconds | ForEach-Object { $_ })
$logPath = (Resolve-Path (Join-Path $PSScriptRoot "..\" + ($config.logPath -replace '/','\\'))).Path

# Ensure log dir exists
$logDir = Split-Path $logPath -Parent
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

$jobScript = {
    param($id,$interval,$logPath)
    while ($true) {
        $ts = Get-Date -Format o
        "[$ts] Worker $id: heartbeat" | Out-File -FilePath $logPath -Append
        Start-Sleep -Seconds $interval
    }
}

for ($i = 1; $i -le $numWorkers; $i++) {
    Start-Job -ScriptBlock $jobScript -ArgumentList $i,$interval,$logPath -Name "Worker-$i" | Out-Null
    Write-Output "Started worker #$i as background job."
}

Write-Output "Started $numWorkers workers. Use Get-Job / Receive-Job / Stop-Job to manage jobs, or run the script under a Task Scheduler entry for persistent runs."

try {
    while ($true) { Start-Sleep -Seconds 5 }
} catch [System.Exception] {
    Write-Output "Shutting down: stopping jobs..."
    Get-Job | Stop-Job -Force -ErrorAction SilentlyContinue
    Get-Job | Remove-Job -ErrorAction SilentlyContinue
    exit 0
}