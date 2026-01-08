#!/usr/bin/env python
"""Test allergen filtering"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Product
from core.services import _product_contains_allergen, _filter_products_by_allergens

# Test 1: Check if meat excludes correct products
print("=== Test 1: Atlasot 'meat' ===")
all_proteins = Product.objects.filter(category='PROTEIN')
for p in all_proteins:
    is_meat = _product_contains_allergen(p.name, 'meat')
    print(f"{p.name:30} -> {'IZSLĒGTS' if is_meat else 'OK'}")

print("\n=== Test 2: Atlasot 'chicken' ===")
for p in all_proteins:
    is_chicken = _product_contains_allergen(p.name, 'chicken')
    print(f"{p.name:30} -> {'IZSLĒGTS' if is_chicken else 'OK'}")

print("\n=== Test 3: Atlasot 'milk' vai 'dairy' ===")
all_products = Product.objects.all()
for p in all_products:
    is_dairy = _product_contains_allergen(p.name, 'milk')
    if is_dairy:
        print(f"{p.name:30} -> IZSLĒGTS (piena produkts)")

print("\n=== Test 4: Atlasot 'shellfish' ===")
for p in all_proteins:
    is_shellfish = _product_contains_allergen(p.name, 'shellfish')
    if is_shellfish:
        print(f"{p.name:30} -> IZSLĒGTS (jūras produkts)")

print("\n=== Test 5: Filtrēt produktus ar 'meat' ===")
filtered = _filter_products_by_allergens(list(all_proteins), ['meat'])
print(f"Pieejami proteīni (bez gaļas): {len(filtered)} no {all_proteins.count()}")
for p in filtered:
    print(f"  - {p.name}")
