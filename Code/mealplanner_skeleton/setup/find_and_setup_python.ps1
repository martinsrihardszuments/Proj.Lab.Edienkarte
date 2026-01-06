# Script to find Python and setup database
Write-Host "=== Meklē Python un izveido datu bāzi ===" -ForegroundColor Cyan

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Atjauno PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Meklē Python dažādos veidos
$pythonFound = $null

Write-Host "`nMeklē Python..." -ForegroundColor Yellow

# 1. Mēģina ar python komandu
try {
    $result = python --version 2>&1
    if ($LASTEXITCODE -eq 0 -and $result -notlike "*netika atrasts*" -and $result -notlike "*not found*") {
        $pythonFound = "python"
        Write-Host "✓ Python atrasts: $result" -ForegroundColor Green
    }
} catch {}

# 2. Mēģina ar py komandu
if (-not $pythonFound) {
    try {
        $result = py --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonFound = "py"
            Write-Host "✓ Python launcher atrasts: $result" -ForegroundColor Green
        }
    } catch {}
}

# 3. Meklē Python instalācijas mapēs
if (-not $pythonFound) {
    Write-Host "Meklē Python instalācijas mapēs..." -ForegroundColor Yellow
    $searchPaths = @(
        "$env:LOCALAPPDATA\Programs\Python",
        "$env:PROGRAMFILES\Python*",
        "${env:ProgramFiles(x86)}\Python*",
        "C:\Python*"
    )
    
    foreach ($basePath in $searchPaths) {
        $dirs = Get-ChildItem $basePath -ErrorAction SilentlyContinue -Directory
        foreach ($dir in $dirs) {
            $pythonExe = Join-Path $dir.FullName "python.exe"
            if (Test-Path $pythonExe) {
                try {
                    $version = & $pythonExe --version 2>&1
                    if ($LASTEXITCODE -eq 0 -and $version -notlike "*netika atrasts*") {
                        $pythonFound = $pythonExe
                        Write-Host "✓ Python atrasts: $pythonExe ($version)" -ForegroundColor Green
                        break
                    }
                } catch {}
            }
        }
        if ($pythonFound) { break }
    }
}

# Ja Python nav atrasts
if (-not $pythonFound) {
    Write-Host "`n❌ Python nav atrasts!" -ForegroundColor Red
    Write-Host "`nLūdzu:" -ForegroundColor Yellow
    Write-Host "1. Instalē Python no https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. RESTARTĒ termināli pēc instalācijas" -ForegroundColor White
    Write-Host "3. Palaid šo skriptu atkārtoti" -ForegroundColor White
    Write-Host "`nVai arī izpildi manuāli:" -ForegroundColor Yellow
    Write-Host "python -m venv .venv" -ForegroundColor Cyan
    Write-Host ".\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "pip install -r requirements.txt" -ForegroundColor Cyan
    Write-Host "python manage.py migrate" -ForegroundColor Cyan
    exit 1
}

# Izveido datu bāzi
Write-Host "`n=== Izveido datu bāzi ===" -ForegroundColor Cyan

# Pārbauda vai ir virtuālā vide
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Izveido virtuālo vidi..." -ForegroundColor Yellow
    & $pythonFound -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Neizdevās izveidot virtuālo vidi" -ForegroundColor Red
        exit 1
    }
    $pythonCmd = ".\.venv\Scripts\python.exe"
} else {
    Write-Host "Virtuālā vide jau pastāv" -ForegroundColor Green
    $pythonCmd = ".\.venv\Scripts\python.exe"
}

# Instalē requirements
Write-Host "Instalē bibliotēkas..." -ForegroundColor Yellow
& $pythonCmd -m pip install --upgrade pip --quiet
& $pythonCmd -m pip install -r requirements.txt --quiet

# Izpilda migrācijas
Write-Host "Izveido datu bāzi..." -ForegroundColor Yellow
& $pythonCmd manage.py migrate

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Datu bāze izveidota veiksmīgi!" -ForegroundColor Green
    Write-Host "Datu bāzes fails: db.sqlite3" -ForegroundColor Cyan
    
    # Jautā par demo datiem
    $seed = Read-Host "`nVai pievienot demo datus? (y/n)"
    if ($seed -eq "y" -or $seed -eq "Y") {
        Write-Host "Pievieno demo datus..." -ForegroundColor Yellow
        & $pythonCmd manage.py seed
        Write-Host "✓ Demo dati pievienoti!" -ForegroundColor Green
    }
    
    Write-Host "`n=== Gatavs! ===" -ForegroundColor Green
    Write-Host "Lai palaidu serveri: python manage.py runserver" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Neizdevās izveidot datu bāzi" -ForegroundColor Red
    exit 1
}
