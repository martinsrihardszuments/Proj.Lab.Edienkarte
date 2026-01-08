#!/usr/bin/env python
"""Test real scenario: generate meal plan with allergen exclusions"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.services import generate_plan_calorie_based

print("=== Scenārijs 1: Atlasīta 'meat' alerģija ===")
profile = {
    'allergies_and_dislikes': ['meat'],
    'target_kcal': 2000,
    'sex': 'M',
    'age': 25,
    'height_cm': 175,
    'weight_kg': 70,
    'activity': 'MED',
    'goal': 'KEEP'
}
plan = generate_plan_calorie_based(profile, days=1)
print(f"Plāna ID: {plan.id}")
for meal in plan.meals.all():
    print(f"\nDay {meal.day_index}, {meal.get_meal_type_display()}:")
    print(f"  Recipe: {meal.recipe.name}")
    for ing in meal.recipe.ingredients.all():
        print(f"    - {ing.product.name} ({ing.amount_g}g)")

print("\n" + "="*60)
print("=== Scenārijs 2: Atlasīta 'chicken' alerģija ===")
profile['allergies_and_dislikes'] = ['chicken']
plan = generate_plan_calorie_based(profile, days=1)
print(f"Plāna ID: {plan.id}")
for meal in plan.meals.all():
    print(f"\nDay {meal.day_index}, {meal.get_meal_type_display()}:")
    print(f"  Recipe: {meal.recipe.name}")
    for ing in meal.recipe.ingredients.all():
        print(f"    - {ing.product.name} ({ing.amount_g}g)")

print("\n" + "="*60)
print("=== Scenārijs 3: Atlasīta 'milk' (dairy) alerģija ===")
profile['allergies_and_dislikes'] = ['milk']
plan = generate_plan_calorie_based(profile, days=1)
print(f"Plāna ID: {plan.id}")
for meal in plan.meals.all():
    print(f"\nDay {meal.day_index}, {meal.get_meal_type_display()}:")
    print(f"  Recipe: {meal.recipe.name}")
    for ing in meal.recipe.ingredients.all():
        print(f"    - {ing.product.name} ({ing.amount_g}g)")

print("\n" + "="*60)
print("=== Scenārijs 4: Atlasītas 'meat' UN 'chicken' alerģijas ===")
profile['allergies_and_dislikes'] = ['meat', 'chicken']
plan = generate_plan_calorie_based(profile, days=1)
print(f"Plāna ID: {plan.id}")
for meal in plan.meals.all():
    print(f"\nDay {meal.day_index}, {meal.get_meal_type_display()}:")
    print(f"  Recipe: {meal.recipe.name}")
    for ing in meal.recipe.ingredients.all():
        print(f"    - {ing.product.name} ({ing.amount_g}g)")
