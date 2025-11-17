from django.core.management.base import BaseCommand
from core.models import Product, Recipe, Ingredient

def add_product(name, kcal, p, f, c, price):
    return Product.objects.get_or_create(
        name=name, kcal_100g=kcal, p_g_100g=p, f_g_100g=f, c_g_100g=c, price_eur_100g=price
    )[0]

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
        chicken = add_product("Chicken breast", 165, 31, 3.6, 0, 0.90)
        tuna = add_product("Canned tuna (in water)", 132, 29, 1, 0, 1.20)
        eggs = add_product("Eggs", 155, 13, 11, 1.1, 0.60)
        greek = add_product("Greek yogurt (low fat)", 59, 10, 0.4, 3.6, 0.50)
        tofu = add_product("Tofu", 76, 8, 4.8, 1.9, 0.45)
        beef = add_product("Lean beef", 187, 26, 9, 0, 1.30)
        lentils = add_product("Boiled lentils", 116, 9, 0.4, 20, 0.25)

        # Carbs
        oats = add_product("Oats", 379, 13, 7, 67, 0.20)
        rice = add_product("Rice", 360, 7, 0.6, 79, 0.18)
        pasta = add_product("Pasta (dry)", 371, 13, 1.5, 75, 0.22)
        bread = add_product("Wholegrain bread", 247, 13, 4.2, 41, 0.30)
        banana = add_product("Banana", 89, 1.1, 0.3, 23, 0.35)

        # Fats & extras
        olive = add_product("Olive oil", 884, 0, 100, 0, 1.10)
        avocado = add_product("Avocado", 160, 2, 15, 9, 0.90)
        almonds = add_product("Almonds", 579, 21, 50, 22, 1.50)
        tomato = add_product("Tomato", 18, 0.9, 0.2, 3.9, 0.20)
        cucumber = add_product("Cucumber", 16, 0.7, 0.1, 3.6, 0.15)
        onion = add_product("Onion", 40, 1.1, 0.1, 9.3, 0.10)
        spinach = add_product("Spinach", 23, 2.9, 0.4, 3.6, 0.20)
        # More proteins, legumes and seafood
        salmon = add_product("Salmon (fillet)", 208, 20, 13, 0, 2.50)
        mackerel = add_product("Mackerel", 205, 19, 13.9, 0, 2.00)
        shrimp = add_product("Shrimp (cooked)", 99, 24, 0.3, 0, 2.20)
        turkey = add_product("Turkey breast", 135, 29, 1.5, 0, 1.10)
        chickpeas = add_product("Chickpeas (cooked)", 164, 8.9, 2.6, 27.4, 0.40)
        blackbeans = add_product("Black beans (cooked)", 132, 8.9, 0.5, 23.7, 0.35)

        # Grains & alternatives
        quinoa = add_product("Quinoa (cooked)", 120, 4.4, 1.9, 21.3, 0.50)
        couscous = add_product("Couscous (cooked)", 112, 3.8, 0.2, 23.2, 0.30)
        sweet_potato = add_product("Sweet potato", 86, 1.6, 0.1, 20.1, 0.45)

        # Vegetables & extras
        bell = add_product("Bell pepper", 31, 1, 0.3, 6, 0.25)
        zucchini = add_product("Zucchini", 17, 1.2, 0.3, 3.1, 0.20)
        mushroom = add_product("Mushrooms", 22, 3.1, 0.3, 3.3, 0.25)
        mixed_greens = add_product("Mixed salad greens", 20, 2, 0.2, 3.3, 0.50)

        # Breakfast & pantry
        granola = add_product("Granola", 471, 10, 20, 60, 0.60)
        chia = add_product("Chia seeds", 486, 17, 31, 42, 1.20)
        peanut = add_product("Peanut butter", 588, 25, 50, 20, 0.80)
        hummus = add_product("Hummus", 166, 8, 9.6, 14.3, 0.70)
        pumpkin = add_product("Pumpkin", 26, 1, 0.1, 6.5, 0.30)

        # Recipes (balanced across kcal levels)
        make_recipe("Oats & Yogurt Bowl", [(oats,60), (greek,200), (banana,100), (almonds,15)])
        make_recipe("Avocado Toast & Egg", [(bread,80), (avocado,70), (eggs,120), (tomato,80)])
        make_recipe("Chicken Rice Bowl", [(chicken,200), (rice,150), (olive,10), (spinach,80)])
        make_recipe("Tuna Salad", [(tuna,150), (tomato,100), (cucumber,100), (olive,10), (bread,60)])
        make_recipe("Tofu Stir-fry", [(tofu,200), (rice,150), (olive,10), (onion,60), (spinach,80)])
        make_recipe("Beef Pasta", [(beef,180), (pasta,160), (olive,10), (tomato,120)])
        make_recipe("Lentil Soup & Bread", [(lentils,300), (olive,10), (onion,60), (bread,60)])
        make_recipe("Omelette", [(eggs,180), (spinach,80), (olive,8), (tomato,80)])
        make_recipe("Yogurt, Oats & Almonds", [(greek,220), (oats,40), (almonds,15), (banana,80)])
        make_recipe("Simple Rice & Tuna", [(tuna,160), (rice,160), (olive,8), (spinach,60)])

        # New recipes for increased variety
        make_recipe("Salmon & Quinoa Bowl", [(salmon,140), (quinoa,180), (spinach,60), (avocado,50), (olive,8)])
        make_recipe("Shrimp Stir-fry", [(shrimp,120), (rice,140), (bell,80), (zucchini,80), (olive,8)])
        make_recipe("Chickpea Curry", [(chickpeas,200), (rice,120), (tomato,120), (onion,60), (olive,8)])
        make_recipe("Sweet Potato Buddha Bowl", [(sweet_potato,200), (blackbeans,120), (spinach,60), (avocado,50), (olive,8)])
        make_recipe("Turkey Wrap", [(turkey,120), (bread,80), (mixed_greens,40), (hummus,40), (tomato,40)])
        make_recipe("Veggie Stir-fry", [(tofu,150), (quinoa,140), (bell,80), (mushroom,80), (olive,8)])
        make_recipe("Mushroom Pasta", [(mushroom,160), (pasta,160), (olive,8), (onion,60)])
        make_recipe("Pancakes & Banana", [(oats,80), (eggs,100), (banana,120), (peanut,10)])
        make_recipe("Smoothie Bowl", [(greek,180), (banana,100), (chia,15), (granola,40), (peanut,10)])
        make_recipe("Hummus & Veg Wrap", [(hummus,80), (cucumber,80), (bell,80), (bread,80), (tomato,40)])
        make_recipe("Bean Chilli", [(blackbeans,180), (tomato,140), (onion,80), (rice,100), (olive,8)])
        make_recipe("Quinoa Salad", [(quinoa,160), (mixed_greens,60), (cucumber,60), (avocado,40), (olive,8)])

        self.stdout.write(self.style.SUCCESS("Demo products & variety recipes ready."))
