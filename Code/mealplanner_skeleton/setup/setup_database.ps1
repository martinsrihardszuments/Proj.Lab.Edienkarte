# MealPlanner Database Setup Script
# This script creates the SQLite database and runs migrations

Write-Host "=== MealPlanner Database Setup ===" -ForegroundColor Cyan

# Navigate to project root (parent of setup folder)
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot
Write-Host "Working directory: $projectRoot" -ForegroundColor Cyan

# Find Python
$pythonCmd = $null
if (Test-Path ".venv\Scripts\python.exe") {
    $pythonCmd = ".\.venv\Scripts\python.exe"
    Write-Host "Using virtual environment Python" -ForegroundColor Green
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
    Write-Host "Using system Python" -ForegroundColor Yellow
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
    Write-Host "Using Python launcher" -ForegroundColor Yellow
} else {
    Write-Host "[ERROR] Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ and try again." -ForegroundColor Red
    Write-Host "Or run: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Check if virtual environment exists, create if not
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    & $pythonCmd -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    $pythonCmd = ".\.venv\Scripts\python.exe"
}

# Activate virtual environment and install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
& $pythonCmd -m pip install --upgrade pip --quiet
& $pythonCmd -m pip install -r requirements.txt --quiet

# Run migrations to create database
Write-Host "Creating database schema..." -ForegroundColor Yellow
& $pythonCmd manage.py migrate

if ($LASTEXITCODE -eq 0) {
    Write-Host "Database created successfully!" -ForegroundColor Green
    
    # Ask if user wants to seed demo data
    $seed = Read-Host "Do you want to seed demo data? (y/n)"
    if ($seed -eq "y" -or $seed -eq "Y") {
        Write-Host "Seeding demo data..." -ForegroundColor Yellow
        & $pythonCmd manage.py seed
        Write-Host "Demo data seeded!" -ForegroundColor Green
    }
    
    Write-Host "`nDatabase setup complete!" -ForegroundColor Green
    Write-Host "Database file: db.sqlite3" -ForegroundColor Cyan
} else {
    Write-Host "[ERROR] Failed to create database" -ForegroundColor Red
    exit 1
}
