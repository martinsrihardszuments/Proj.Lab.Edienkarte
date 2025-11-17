# MealPlanner (Skeleton)

Pirmie soļo projektam
Darbojas ar pagaidām ar **SQLite**

## Kā palaist (Windows / macOS / Linux)

```bash
python -m venv .venv
# Windows PowerShell:
. .venv/Scripts/Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt

# Django migrācijas un demo dati
python manage.py migrate
python manage.py seed

# Palaišana
python manage.py runserver
```

Atver: http://127.0.0.1:8000/

- Poga **"Ģenerēt plānu"** izveidos 7 dienu plānu ar 3 ēdienreizēm dienā (B/L/D).
