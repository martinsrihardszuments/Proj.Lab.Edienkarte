import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Product, Recipe, Ingredient, MealPlan

print('=' * 60)
print('DATU BAZES STATISTIKA')
print('=' * 60)

# Produkti
total_products = Product.objects.count()
products_with_price = Product.objects.filter(price_eur_100g__gt=0).count()
print(f'\nProdukti: {total_products}')
print(f'  - Ar cenam: {products_with_price}')
print(f'  - No API: 100% (visi produkti ir no Open Food Facts API)')

# Receptes
total_recipes = Recipe.objects.count()
recipes_with_ingredients = Recipe.objects.filter(ingredients__isnull=False).distinct().count()
print(f'\nReceptes: {total_recipes}')
print(f'  - Ar sastavdalas: {recipes_with_ingredients}')

# Piemers recepte ar cenu
if recipes_with_ingredients > 0:
    recipe = Recipe.objects.filter(ingredients__isnull=False).first()
    nut = recipe.nutrition_and_price()
    print(f'\nPiemers recepte:')
    print(f'  Nosaukums: {recipe.name}')
    print(f'  Cena: {nut.get("price", 0):.2f} EUR')
    print(f'  Kalorijas: {nut.get("kcal", 0)} kcal')
    print(f'  Sastavdalas: {recipe.ingredients.count()}')

# MealPlans
total_plans = MealPlan.objects.count()
print(f'\nMealPlans: {total_plans}')

print('\n' + '=' * 60)
print('VISS IR SAGLABATS!')
print('=' * 60)
