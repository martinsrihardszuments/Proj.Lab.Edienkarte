# Kā izveidot datu bāzi

## Svarīgi!
Pēc Python instalācijas **restartēj termināli** (aizver un atver jaunu PowerShell/CMD logu), lai Python tiktu pievienots PATH.

## Soļi:

### 1. Atver jaunu termināli (PowerShell vai CMD)

### 2. Pārej uz projekta direktoriju:
```powershell
cd "C:\Users\jlvil\Downloads\Proj.Lab.Edienkarte-main\Proj.Lab.Edienkarte-main\Code\mealplanner_skeleton"
```

### 3. Pārbaudi, vai Python darbojas:
```powershell
python --version
```
Vai arī:
```powershell
py --version
```

Ja redzi versiju (piemēram, `Python 3.11.5`), turpini tālāk.

### 4. Izveido datu bāzi - izvēlies vienu no opcijām:

#### Opcija A: Izmanto automātisko skriptu (vienkāršākais veids)
```powershell
.\setup_database.bat
```
vai
```powershell
.\setup_database.ps1
```

#### Opcija B: Manuāli (soļi pa soļiem)

**a) Izveido virtuālo vidi:**
```powershell
python -m venv .venv
```

**b) Aktivizē virtuālo vidi:**
```powershell
# PowerShell:
.\.venv\Scripts\Activate.ps1

# Vai CMD:
.venv\Scripts\activate.bat
```

**c) Instalē bibliotēkas:**
```powershell
pip install -r requirements.txt
```

**d) Izveido datu bāzi:**
```powershell
python manage.py migrate
```

**e) (Nav obligāti) Pievieno demo datus:**
```powershell
python manage.py seed
```

### 5. Pārbaudi, vai datu bāze izveidota:
```powershell
if (Test-Path "db.sqlite3") { Write-Host "Datu bāze izveidota!" } else { Write-Host "Datu bāze nav izveidota" }
```

## Problēmas?

### Python nav atrasts
- Restartē termināli
- Pārbaudi, vai Python ir instalēts: `where.exe python`
- Vai arī mēģini: `where.exe py`

### Kļūda ar virtuālo vidi
- Dzēs mapi `.venv` un mēģini no jauna
- Pārbaudi, vai Python darbojas: `python --version`

### Citas problēmas
- Pārbaudi, vai esi pareizajā direktorijā (`manage.py` jābūt redzamam)
- Pārbaudi, vai visas bibliotēkas ir instalētas: `pip list`
