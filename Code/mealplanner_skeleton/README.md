# Meal Planner

A Django-based meal planning application that generates balanced weekly meal plans using real nutrition data from the Open Food Facts API.

## Project Structure

```
mealplanner_skeleton/
├── docs/              # Documentation and project information
├── scripts/           # Utility scripts for debugging and exports
├── setup/             # Setup and server management scripts
├── config/            # Django project configuration
├── core/              # Main application code
├── templates/         # HTML templates
├── db.sqlite3         # Database file
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Quick Start

### 1. Setup Database
Run one of the setup scripts from the `setup/` folder:
```bash
# Windows PowerShell (recommended)
.\setup\setup_database.ps1

# Windows Command Prompt
setup\setup_database.bat
```

### 2. Start Server
```bash
# From setup folder
.\setup\start_server.bat
```

### 3. Access the Application
Open your browser and go to: `http://127.0.0.1:8000/`

### 4. Stop Server
```bash
.\setup\stop_server.bat
```

## Features

- 🎯 Personalized calorie calculations using Mifflin-St Jeor formula
- 🍽️ Generate 3 different meal plan options side-by-side
- 📊 Complete nutritional breakdown (calories, protein, carbs, fat, sugar)
- 🥗 Category-based meal generation (Breakfast, Protein, Carbs, Vitamins)
- 💰 Price tracking for meal plans
- 🌐 Real nutrition data from Open Food Facts API

## Technologies

- **Backend**: Django 5.0.6
- **Database**: SQLite
- **Frontend**: HTML, Tailwind CSS
- **API**: Open Food Facts
- **Python**: 3.13

## Team

Created by: Marta, Martins, Janis, Kristers and Eduards

© 2026 Meal Planner
