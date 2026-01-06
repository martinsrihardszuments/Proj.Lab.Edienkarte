from django.core.management.base import BaseCommand
from core.models import Product, Recipe, Ingredient


class Command(BaseCommand):
    help = "Create recipes using API products"

    def handle(self, *args, **options):
        # Find products by name patterns
        def find_product(pattern):
            products = Product.objects.filter(name__icontains=pattern)
            return products.first() if products.exists() else None

        # Get products
        chicken = find_product("chicken") or find_product("pollo") or find_product("poultry")
        salmon = find_product("salmon") or find_product("saumon")
        tuna = find_product("tuna") or find_product("thon") or find_product("atun")
        eggs = find_product("egg") or find_product("oeuf")
        yogurt = find_product("yogurt") or find_product("yoghurt") or find_product("yaourt")
        rice = find_product("rice") or find_product("riz")
        pasta = find_product("pasta") or find_product("spaghetti") or find_product("penne")
        bread = find_product("bread") or find_product("pain") or find_product("rye")
        oats = find_product("oats") or find_product("oat") or find_product("avoine")
        olive_oil = find_product("olive") or find_product("huile")
        avocado = find_product("avocado")
        tomato = find_product("tomato") or find_product("tomate")
        cucumber = find_product("cucumber") or find_product("concombre")
        spinach = find_product("spinach") or find_product("epinard")
        onion = find_product("onion") or find_product("oignon")
        banana = find_product("banana")
        almonds = find_product("almond") or find_product("amande")
        beef = find_product("beef") or find_product("boeuf")
        quinoa = find_product("quinoa")
        lentils = find_product("lentil") or find_product("lentille")
        chickpeas = find_product("chickpea") or find_product("pois chiche")
        bell_pepper = find_product("pepper") or find_product("poivron")
        mushroom = find_product("mushroom") or find_product("champignon")
        sweet_potato = find_product("sweet potato") or find_product("patate")
        turkey = find_product("turkey") or find_product("dinde")
        hummus = find_product("hummus") or find_product("houmous")
        peanut_butter = find_product("peanut") or find_product("cacahuete")
        cheese = find_product("cheese") or find_product("fromage") or find_product("cheddar") or find_product("mozzarella")
        butter = find_product("butter") or find_product("beurre") or find_product("margarine")

        recipes_data = []

        # Breakfast recipes
        if oats and yogurt and banana and almonds:
            recipes_data.append({
                "name": "Oats & Yogurt Bowl",
                "ingredients": [(oats, 60), (yogurt, 200), (banana, 100), (almonds, 15)]
            })

        if bread and avocado and eggs and tomato:
            recipes_data.append({
                "name": "Avocado Toast & Egg",
                "ingredients": [(bread, 80), (avocado, 70), (eggs, 120), (tomato, 80)]
            })

        if yogurt and oats and almonds and banana:
            recipes_data.append({
                "name": "Yogurt, Oats & Almonds",
                "ingredients": [(yogurt, 220), (oats, 40), (almonds, 15), (banana, 80)]
            })

        # Lunch recipes
        if chicken and rice and olive_oil and spinach:
            recipes_data.append({
                "name": "Chicken Rice Bowl",
                "ingredients": [(chicken, 200), (rice, 150), (olive_oil, 10), (spinach, 80)]
            })

        if tuna and tomato and cucumber and olive_oil and bread:
            recipes_data.append({
                "name": "Tuna Salad",
                "ingredients": [(tuna, 150), (tomato, 100), (cucumber, 100), (olive_oil, 10), (bread, 60)]
            })

        if salmon and quinoa and spinach and avocado and olive_oil:
            recipes_data.append({
                "name": "Salmon & Quinoa Bowl",
                "ingredients": [(salmon, 140), (quinoa, 180), (spinach, 60), (avocado, 50), (olive_oil, 8)]
            })

        if chickpeas and rice and tomato and onion and olive_oil:
            recipes_data.append({
                "name": "Chickpea Curry",
                "ingredients": [(chickpeas, 200), (rice, 120), (tomato, 120), (onion, 60), (olive_oil, 8)]
            })

        if turkey and bread and spinach and hummus and tomato:
            recipes_data.append({
                "name": "Turkey Wrap",
                "ingredients": [(turkey, 120), (bread, 80), (spinach, 40), (hummus, 40), (tomato, 40)]
            })

        # Dinner recipes
        if beef and pasta and olive_oil and tomato:
            recipes_data.append({
                "name": "Beef Pasta",
                "ingredients": [(beef, 180), (pasta, 160), (olive_oil, 10), (tomato, 120)]
            })

        if lentils and olive_oil and onion and bread:
            recipes_data.append({
                "name": "Lentil Soup & Bread",
                "ingredients": [(lentils, 300), (olive_oil, 10), (onion, 60), (bread, 60)]
            })

        if eggs and spinach and olive_oil and tomato:
            recipes_data.append({
                "name": "Omelette",
                "ingredients": [(eggs, 180), (spinach, 80), (olive_oil, 8), (tomato, 80)]
            })

        if pasta and mushroom and olive_oil and onion:
            recipes_data.append({
                "name": "Mushroom Pasta",
                "ingredients": [(mushroom, 160), (pasta, 160), (olive_oil, 8), (onion, 60)]
            })

        if sweet_potato and chickpeas and spinach and avocado and olive_oil:
            recipes_data.append({
                "name": "Sweet Potato Buddha Bowl",
                "ingredients": [(sweet_potato, 200), (chickpeas, 120), (spinach, 60), (avocado, 50), (olive_oil, 8)]
            })

        # Create recipes
        created = 0
        updated = 0

        for recipe_data in recipes_data:
            recipe, created_flag = Recipe.objects.get_or_create(
                name=recipe_data["name"],
                defaults={"portion_g": 300}
            )

            # Clear existing ingredients if updating
            had_ingredients = recipe.ingredients.exists()
            if had_ingredients:
                recipe.ingredients.all().delete()
                updated += 1

            # Add ingredients
            for product, amount in recipe_data["ingredients"]:
                if product:  # Make sure product exists
                    Ingredient.objects.create(
                        recipe=recipe,
                        product=product,
                        amount_g=amount
                    )

            if created_flag:
                created += 1

            # Calculate and show price
            nut = recipe.nutrition_and_price()
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created_flag else 'Updated'}: {recipe.name} "
                    f"({nut['kcal']} kcal, €{nut['price']:.2f})"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n=== Complete ==="
                f"\nCreated: {created} recipes"
                f"\nUpdated: {updated} recipes"
                f"\nTotal recipes: {Recipe.objects.count()}"
            )
        )
