from django.core.management.base import BaseCommand
from core.models import Product, Recipe, Ingredient

def add_product(name, kcal, p, f, c, price, category='OTHER'):
    product, created = Product.objects.get_or_create(
        name=name,
        defaults={
            'kcal_100g': kcal,
            'p_g_100g': p,
            'f_g_100g': f,
            'c_g_100g': c,
            'price_eur_100g': price,
            'category': category
        }
    )
    if not created and product.category == 'OTHER':
        product.category = category
        product.save()
    return product

def make_recipe(name, items, portion_g=300):
    r, _ = Recipe.objects.get_or_create(name=name, defaults={"portion_g": portion_g})
    if r.ingredients.exists():
        return r
    for prod, amount in items:
        Ingredient.objects.create(recipe=r, product=prod, amount_g=amount)
    return r

class Command(BaseCommand):
    help = "Seed demo products and recipes for variety"

    def handle(self, *args, **opts):
        # Proteins
        chicken = add_product("Chicken breast", 165, 31, 3.6, 0, 0.90, 'PROTEIN')
        tuna = add_product("Canned tuna (in water)", 132, 29, 1, 0, 1.20, 'PROTEIN')
        eggs = add_product("Eggs", 155, 13, 11, 1.1, 0.60, 'BREAKFAST')
        greek = add_product("Greek yogurt (low fat)", 59, 10, 0.4, 3.6, 0.50, 'BREAKFAST')
        tofu = add_product("Tofu", 76, 8, 4.8, 1.9, 0.45, 'PROTEIN')
        beef = add_product("Lean beef", 187, 26, 9, 0, 1.30, 'PROTEIN')
        lentils = add_product("Boiled lentils", 116, 9, 0.4, 20, 0.25, 'PROTEIN')

        # Carbs
        oats = add_product("Oats", 379, 13, 7, 67, 0.20, 'BREAKFAST')
        rice = add_product("Rice", 360, 7, 0.6, 79, 0.18, 'CARBS')
        pasta = add_product("Pasta (dry)", 371, 13, 1.5, 75, 0.22, 'CARBS')
        bread = add_product("Wholegrain bread", 247, 13, 4.2, 41, 0.30, 'CARBS')
        banana = add_product("Banana", 89, 1.1, 0.3, 23, 0.35, 'VITAMINS')

        # Fats & extras
        olive = add_product("Olive oil", 884, 0, 100, 0, 1.10, 'OTHER')
        avocado = add_product("Avocado", 160, 2, 15, 9, 0.90, 'VITAMINS')
        almonds = add_product("Almonds", 579, 21, 50, 22, 1.50, 'OTHER')
        tomato = add_product("Tomato", 18, 0.9, 0.2, 3.9, 0.20, 'VITAMINS')
        cucumber = add_product("Cucumber", 16, 0.7, 0.1, 3.6, 0.15, 'VITAMINS')
        onion = add_product("Onion", 40, 1.1, 0.1, 9.3, 0.10, 'VITAMINS')
        spinach = add_product("Spinach", 23, 2.9, 0.4, 3.6, 0.20, 'VITAMINS')
        # More proteins, legumes and seafood
        salmon = add_product("Salmon (fillet)", 208, 20, 13, 0, 2.50, 'PROTEIN')
        mackerel = add_product("Mackerel", 205, 19, 13.9, 0, 2.00, 'PROTEIN')
        shrimp = add_product("Shrimp (cooked)", 99, 24, 0.3, 0, 2.20, 'PROTEIN')
        turkey = add_product("Turkey breast", 135, 29, 1.5, 0, 1.10, 'PROTEIN')
        chickpeas = add_product("Chickpeas (cooked)", 164, 8.9, 2.6, 27.4, 0.40, 'PROTEIN')
        blackbeans = add_product("Black beans (cooked)", 132, 8.9, 0.5, 23.7, 0.35, 'PROTEIN')

        # Grains & alternatives
        quinoa = add_product("Quinoa (cooked)", 120, 4.4, 1.9, 21.3, 0.50, 'CARBS')
        couscous = add_product("Couscous (cooked)", 112, 3.8, 0.2, 23.2, 0.30, 'CARBS')
        sweet_potato = add_product("Sweet potato", 86, 1.6, 0.1, 20.1, 0.45, 'CARBS')

        # Vegetables & extras
        bell = add_product("Bell pepper", 31, 1, 0.3, 6, 0.25, 'VITAMINS')
        zucchini = add_product("Zucchini", 17, 1.2, 0.3, 3.1, 0.20, 'VITAMINS')
        mushroom = add_product("Mushrooms", 22, 3.1, 0.3, 3.3, 0.25, 'VITAMINS')
        mixed_greens = add_product("Mixed salad greens", 20, 2, 0.2, 3.3, 0.50, 'VITAMINS')

        # Breakfast & pantry
        granola = add_product("Granola", 471, 10, 20, 60, 0.60, 'BREAKFAST')
        chia = add_product("Chia seeds", 486, 17, 31, 42, 1.20, 'OTHER')
        peanut = add_product("Peanut butter", 588, 25, 50, 20, 0.80, 'OTHER')
        hummus = add_product("Hummus", 166, 8, 9.6, 14.3, 0.70, 'OTHER')
        pumpkin = add_product("Pumpkin", 26, 1, 0.1, 6.5, 0.30, 'VITAMINS')

        # Don't create pre-made recipes anymore - meals will be generated dynamically!
        self.stdout.write(self.style.SUCCESS("Demo products with categories ready for dynamic meal generation!"))
