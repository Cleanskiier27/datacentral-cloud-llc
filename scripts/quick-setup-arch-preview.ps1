<#
quick-setup-arch-preview.ps1

One-click helper to:
1) Ensure WSL is enabled.
2) Optionally install ArchWSL from a local .appx/.msixbundle.
3) Launch an ASCII LED preview in a new browser window.

Usage examples:
  .\scripts\quick-setup-arch-preview.ps1
  .\scripts\quick-setup-arch-preview.ps1 -ArchBundlePath "C:\Downloads\ArchWSL.msixbundle"
  .\scripts\quick-setup-arch-preview.ps1 -SkipWslSetup
#>

param(
    [string]$ArchBundlePath = "",
    [switch]$SkipWslSetup,
    [switch]$NoElevation,
    [switch]$ForcePreviewRefresh,
    [switch]$Interactive
)

$ErrorActionPreference = 'Stop'

function Test-IsAdmin {
    $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Invoke-ElevatedRelaunch {
    $argList = @('-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"")
    if ($ArchBundlePath) { $argList += '-ArchBundlePath'; $argList += "`"$ArchBundlePath`"" }
    if ($SkipWslSetup) { $argList += '-SkipWslSetup' }
    if ($NoElevation) { $argList += '-NoElevation' }
    if ($ForcePreviewRefresh) { $argList += '-ForcePreviewRefresh' }
    if ($Interactive) { $argList += '-Interactive' }

    Start-Process -FilePath (Get-Command powershell.exe).Source -ArgumentList ($argList -join ' ') -Verb RunAs -Wait
    exit $LASTEXITCODE
}

function Test-CommandExists([string]$Name) {
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Read-YesNo {
    param(
        [string]$Prompt,
        [bool]$Default = $true
    )

    $defaultText = if ($Default) { "Y/n" } else { "y/N" }
    $raw = Read-Host "$Prompt [$defaultText]"
    if ([string]::IsNullOrWhiteSpace($raw)) { return $Default }

    $answer = $raw.Trim().ToLowerInvariant()
    if ($answer -in @('y', 'yes')) { return $true }
    if ($answer -in @('n', 'no')) { return $false }
    return $Default
}

function Configure-InteractiveOptions {
    Write-Host "`nInteractive setup" -ForegroundColor Cyan
    Write-Host "-----------------" -ForegroundColor Cyan

    $runWsl = Read-YesNo -Prompt "Run WSL setup step" -Default $true
    if (-not $runWsl) { $script:SkipWslSetup = $true }

    $refreshPreview = Read-YesNo -Prompt "Regenerate ASCII preview HTML" -Default $false
    if ($refreshPreview) { $script:ForcePreviewRefresh = $true }

    if ([string]::IsNullOrWhiteSpace($script:ArchBundlePath)) {
        $bundlePathInput = Read-Host "Optional ArchWSL .appx/.msixbundle path (leave empty to skip install)"
        if (-not [string]::IsNullOrWhiteSpace($bundlePathInput)) {
            $script:ArchBundlePath = $bundlePathInput.Trim()
        }
    }
}

function Ensure-Wsl {
    if ($SkipWslSetup) {
        Write-Host "⏭️  Skipping WSL setup by request." -ForegroundColor Yellow
        return
    }

    if (-not (Test-CommandExists 'wsl.exe')) {
        throw "wsl.exe not found. Update Windows or enable WSL components manually first."
    }

    Write-Host "🐧 Ensuring WSL is enabled..." -ForegroundColor Cyan
    & wsl --install --no-distribution | Out-Host
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ WSL command returned exit code $LASTEXITCODE. Continuing with checks..." -ForegroundColor Yellow
    }
}

function Get-WslDistroNames {
    $listOutput = & wsl -l -q 2>$null
    if (-not $listOutput) { return @() }
    return $listOutput | ForEach-Object { $_.Trim() } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
}

function Ensure-ArchWsl {
    $distros = Get-WslDistroNames
    $archCandidates = @('Arch','ArchLinux','ArchWSL')
    foreach ($candidate in $archCandidates) {
        if ($distros -contains $candidate) {
            Write-Host "✅ Arch distro detected in WSL as '$candidate'." -ForegroundColor Green
            return
        }
    }

    if ($ArchBundlePath) {
        if (-not (Test-Path $ArchBundlePath)) {
            throw "Arch bundle not found: $ArchBundlePath"
        }

        Write-Host "📦 Installing ArchWSL package from: $ArchBundlePath" -ForegroundColor Cyan
        Add-AppxPackage -Path $ArchBundlePath
        Write-Host "✅ ArchWSL package installed." -ForegroundColor Green
        return
    }

    Write-Host "ℹ️ Arch is not currently installed in WSL." -ForegroundColor Yellow
    Write-Host "   Download ArchWSL (.appx/.msixbundle), then re-run with -ArchBundlePath." -ForegroundColor Yellow
    Start-Process "https://github.com/yuk7/ArchWSL/releases"
}

function New-AsciiPreview {
    param(
        [string]$RepoRoot
    )

    $asciiSource = Join-Path $RepoRoot "assets\matrix_screenplay.txt"
    $previewDir = Join-Path $env:USERPROFILE "ascii-preview"
    $previewFile = Join-Path $previewDir "index.html"

    if (-not (Test-Path $asciiSource)) {
        throw "ASCII source not found: $asciiSource"
    }

    if (-not (Test-Path $previewDir)) {
        New-Item -ItemType Directory -Path $previewDir -Force | Out-Null
    }

    if ((-not (Test-Path $previewFile)) -or $ForcePreviewRefresh) {
        $asciiRaw = Get-Content -Path $asciiSource -Raw -Encoding UTF8
        $escaped = [System.Net.WebUtility]::HtmlEncode($asciiRaw)

        $html = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ASCII LED Preview</title>
  <style>
    body {
      margin: 0;
      padding: 20px;
      background: #020b06;
      color: #4dff9a;
      font-family: Consolas, 'Courier New', monospace;
    }
    pre {
      white-space: pre;
      overflow: auto;
      border: 1px solid #1f6b45;
      padding: 16px;
      background: #001f12;
    }
  </style>
</head>
<body>
<pre>$escaped</pre>
</body>
</html>
"@

        Set-Content -Path $previewFile -Value $html -Encoding UTF8
    }

    Start-Process $previewFile
    Write-Host "✅ ASCII LED preview opened: $previewFile" -ForegroundColor Green
}

Write-Host "🚀 Quick Setup: Arch Linux + ASCII LED Preview" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

if ((-not $NoElevation) -and (-not (Test-IsAdmin))) {
    Write-Host "Elevation required for WSL/Appx setup. Relaunching as Administrator..." -ForegroundColor Yellow
    Invoke-ElevatedRelaunch
}

if ($Interactive) {
    Configure-InteractiveOptions
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Ensure-Wsl
Ensure-ArchWsl
New-AsciiPreview -RepoRoot $RepoRoot

Write-Host "`nDone." -ForegroundColor Green
Write-Host "Next command after Arch install: wsl -d Arch" -ForegroundColor Cyan