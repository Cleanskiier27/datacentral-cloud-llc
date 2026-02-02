' NetworkBuster Installer - Run as Administrator
' VBScript wrapper for elevated execution

Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute "powershell.exe", "-NoProfile -ExecutionPolicy Bypass -File """ & CreateObject("WScript.Shell").CurrentDirectory & "\installer.ps1""", "", "runas", 1
