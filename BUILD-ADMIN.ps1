# Run this script as Administrator to build the .exe
# Right-click → "Run with PowerShell" → Accept UAC prompt

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Rareness v0.3 - Windows Build Script (Admin Mode Required)" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "`nRight-click this file and select 'Run with PowerShell'`n" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "[1/3] Running in Administrator mode ✓" -ForegroundColor Green

# Navigate to project directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "[2/3] Building desktop app...`n" -ForegroundColor Yellow

# Run the build
npm run desktop:build

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n================================================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESS! ✓" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "`nYour .exe is ready:" -ForegroundColor Cyan
    Write-Host "  packages\desktop\release\Rareness-0.3.0-Portable.exe`n" -ForegroundColor White
    
    # Open release folder
    Write-Host "[3/3] Opening release folder..." -ForegroundColor Yellow
    Start-Process "packages\desktop\release"
    
} else {
    Write-Host "`n================================================================" -ForegroundColor Red
    Write-Host "  BUILD FAILED!" -ForegroundColor Red
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host "`nCheck the error messages above.`n" -ForegroundColor Yellow
}

pause
