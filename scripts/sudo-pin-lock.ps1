# NetworkBuster Sudo PIN Lock Manager
# PowerShell wrapper for PIN-based sudo permission management

param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "menu",
    [string]$PIN = ""
)

$SECURITY_PIN = "drew2"
$SCRIPT_PATH = "E:\datacentral-cloud-llc\scripts\sudo-pin-lock.sh"

function Test-PIN {
    param([string]$InputPIN)
    
    if ($InputPIN -eq $SECURITY_PIN) {
        Write-Host "✅ PIN VERIFIED" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ INVALID PIN" -ForegroundColor Red
        return $false
    }
}

function Lock-SudoWithPIN {
    Write-Host "🔒 Locking sudo permissions..." -ForegroundColor Yellow
    Write-Host "Debugger PIN: drew2" -ForegroundColor Cyan
    
    wsl bash $SCRIPT_PATH --lock
    
    Write-Host ""
    Write-Host "✅ Sudo permissions locked with PIN" -ForegroundColor Green
    Write-Host "⚠️  PIN required for all sudo operations: 524-629-634" -ForegroundColor Yellow
}

function Unlock-SudoWithPIN {
    Write-Host "🔓 Unlocking sudo permissions..." -ForegroundColor Yellow
    
    if ($PIN -eq "") {
        $PIN = Read-Host "Enter PIN (drew2)" -AsSecureString
        $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($PIN)
        $PIN = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    }
    
    if (Test-PIN $PIN) {
        wsl bash $SCRIPT_PATH --unlock
        Write-Host "✅ Sudo permissions unlocked" -ForegroundColor Green
    } else {
        Write-Host "❌ Cannot unlock - invalid PIN" -ForegroundColor Red
    }
}

function Get-SecurityStatus {
    Write-Host "🔍 Security Status Check..." -ForegroundColor Cyan
    wsl bash $SCRIPT_PATH --status
}

function Show-Menu {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Blue
    Write-Host "║  NetworkBuster Sudo PIN Lock Manager  ║" -ForegroundColor Blue
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Debugger PIN: drew2" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. 🔒 Lock sudo permissions"
    Write-Host "2. 🔓 Unlock sudo permissions"
    Write-Host "3. 🔍 Check security status"
    Write-Host "4. ⚠️  Emergency unlock"
    Write-Host "0. Exit"
    Write-Host ""
}

# Main execution
switch ($Action.ToLower()) {
    "lock" {
        Lock-SudoWithPIN
    }
    "unlock" {
        Unlock-SudoWithPIN
    }
    "status" {
        Get-SecurityStatus
    }
    "emergency" {
        Write-Host "⚠️  EMERGENCY UNLOCK" -ForegroundColor Red
        $confirmPIN = Read-Host "Enter PIN to confirm"
        if (Test-PIN $confirmPIN) {
            wsl bash $SCRIPT_PATH --emergency
        }
    }
    default {
        while ($true) {
            Show-Menu
            $choice = Read-Host "Select option"
            
            switch ($choice) {
                "1" { Lock-SudoWithPIN }
                "2" { Unlock-SudoWithPIN }
                "3" { Get-SecurityStatus }
                "4" { 
                    $confirmPIN = Read-Host "Enter PIN to confirm emergency unlock"
                    if (Test-PIN $confirmPIN) {
                        wsl bash $SCRIPT_PATH --emergency
                    }
                }
                "0" { Write-Host "Exiting..."; exit 0 }
                default { Write-Host "Invalid option" -ForegroundColor Red }
            }
            
            Write-Host ""
            Read-Host "Press Enter to continue"
        }
    }
}
