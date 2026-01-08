from decimal import Decimal
from random import shuffle, choice
from .models import Recipe, MealPlan, Meal, Product, Ingredient

def _estimate_target_kcal(profile):
    """Mifflin-St Jeor + activity; adjust by goal."""
    # If the user supplied an explicit calorie target, use it (respect clamping).
    explicit = profile.get("target_kcal")
    if explicit:
        try:
            val = int(explicit)
            return int(max(1400, min(val, 3800)))
        except Exception:
            pass

    sex = profile.get("sex","M")
    age = int(profile.get("age",25))
    height_cm = int(profile.get("height_cm",175))
    weight_kg = float(profile.get("weight_kg",70))
    activity = profile.get("activity","MED")
    goal = profile.get("goal","KEEP")

    # BMR (Mifflin-St Jeor)
    if sex == "M":
        bmr = 10*weight_kg + 6.25*height_cm - 5*age + 5
    else:
        bmr = 10*weight_kg + 6.25*height_cm - 5*age - 161

    mult = {"LOW":1.2, "MED":1.55, "HIGH":1.75}.get(activity, 1.55)
    tdee = bmr * mult

    if goal == "CUT":
        target = tdee - 500
    elif goal == "GAIN":
        target = tdee + 300
    else:
        target = tdee

    # clamp to reasonable range
    return int(max(1400, min(target, 3800)))

def _daily_targets(total_kcal):
    """Split across B/L/D roughly 30/40/30."""
    b = int(total_kcal*0.30)
    l = int(total_kcal*0.40)
    d = total_kcal - b - l
    return {"B": b, "L": l, "D": d}

def _pick_meal_for_target(recipes, target_kcal, used_recent):
    """
    Greedy-ish: choose the recipe with kcal closest to target
    (computed from its ingredients), excluding a small recent window
    to increase variety.
    """
    best = None
    best_diff = 10**9
    for r in recipes:
        if r.id in used_recent:  # avoid repetition in recent window
            continue
        nut = r.nutrition_and_price()
        diff = abs(nut["kcal"] - target_kcal)
        if diff < best_diff:
            best, best_diff = r, diff
    if best is None:
        # fallback (if all were excluded): allow all
        for r in recipes:
            nut = r.nutrition_and_price()
            diff = abs(nut["kcal"] - target_kcal)
            if diff < best_diff:
                best, best_diff = r, diff
    return best

def _product_contains_allergen(product_name: str, allergen: str) -> bool:
    """Check if a product name contains an allergen keyword"""
    product_lower = product_name.lower()
    allergen_lower = allergen.lower()
    
    # Special exclusions - products that contain misleading words
    exclusions = [
        'peanut butter',  # contains 'butter' but is not dairy
        'cocoa butter',   # contains 'butter' but is not dairy
        'shea butter',    # contains 'butter' but is not dairy
    ]
    
    # If product is in exclusion list, handle specially
    for exclusion in exclusions:
        if exclusion in product_lower:
            # For peanut butter, only exclude if checking for peanuts
            if 'peanut' in exclusion and allergen_lower in ['peanuts', 'peanut']:
                return True
            # Don't exclude for dairy/milk
            if allergen_lower in ['milk', 'dairy', 'butter']:
                return False
    
    # Direct match
    if allergen_lower in product_lower:
        return True
    
    # Special cases and synonyms
    allergen_synonyms = {
        'milk': ['milk', 'dairy', 'cream', ' butter', 'yogurt', 'yoghurt', 'cheese', 'cheddar', 'mozzarella', 'parmesan'],
        'dairy': ['milk', 'dairy', 'cream', ' butter', 'yogurt', 'yoghurt', 'cheese', 'cheddar', 'mozzarella', 'parmesan'],
        'eggs': ['egg'],
        'fish': ['fish', 'salmon', 'tuna', 'cod', 'tilapia', 'mackerel'],
        'shellfish': ['shrimp', 'crab', 'lobster', 'shellfish', 'prawn'],
        'nuts': ['nut', 'almond', 'walnut', 'cashew', 'hazelnut'],
        'peanuts': ['peanut'],
        'wheat': ['wheat', 'flour'],
        'soy': ['soy', 'tofu', 'edamame'],
        'meat': ['beef', 'pork', 'lamb', 'veal'],
        'chicken': ['chicken', 'poultry', 'turkey'],
        'pork': ['pork', 'bacon', 'ham'],
        'beef': ['beef', 'steak'],
        'rice': ['rice'],
        'pasta': ['pasta', 'spaghetti', 'noodle'],
        'potato': ['potato'],
        'tomato': ['tomato'],
        'onion': ['onion'],
        'garlic': ['garlic'],
        'cheese': ['cheese', 'cheddar', 'mozzarella', 'parmesan'],
        'yogurt': ['yogurt', 'yoghurt'],
        'bread': ['bread', 'toast', 'wholegrain bread'],
    }
    
    # Check synonyms
    for synonym in allergen_synonyms.get(allergen_lower, [allergen_lower]):
        if synonym in product_lower:
            return True
    
    return False

def _filter_products_by_allergens(products, excluded_items: list):
    """Filter out products that contain any of the excluded items"""
    if not excluded_items:
        return products
    
    filtered = []
    for product in products:
        has_allergen = False
        for allergen in excluded_items:
            if _product_contains_allergen(product.name, allergen):
                has_allergen = True
                break
        if not has_allergen:
            filtered.append(product)
    
    return filtered

def _create_balanced_meal(meal_type: str, target_kcal: int, recent_products: set, excluded_items: list = None):
    """
    Create a balanced meal with carbs + protein + vitamins for lunch/dinner
    or breakfast foods for breakfast.
    Returns a Recipe object.
    """
    if excluded_items is None:
        excluded_items = []
    
    if meal_type == "B":
        # Breakfast: eggs/oats + fruit/yogurt
        breakfast_foods = list(Product.objects.filter(category='BREAKFAST').exclude(id__in=recent_products))
        vitamins = list(Product.objects.filter(category='VITAMINS').exclude(id__in=recent_products))
        
        # Filter by allergies
        breakfast_foods = _filter_products_by_allergens(breakfast_foods, excluded_items)
        vitamins = _filter_products_by_allergens(vitamins, excluded_items)
        
        if not breakfast_foods:
            breakfast_foods = list(Product.objects.filter(category='BREAKFAST'))
            breakfast_foods = _filter_products_by_allergens(breakfast_foods, excluded_items)
        if not vitamins:
            vitamins = list(Product.objects.filter(category='VITAMINS'))
            vitamins = _filter_products_by_allergens(vitamins, excluded_items)
        
        if breakfast_foods and vitamins:
            main = choice(breakfast_foods)
            side = choice(vitamins)
            
            # Calculate portions to hit target (roughly 70/30 split)
            main_amount = min(600, int(target_kcal * 0.7 / main.kcal_100g * 100))
            side_amount = min(400, int(target_kcal * 0.3 / side.kcal_100g * 100)) if side.kcal_100g > 0 else 100
            
            recipe = Recipe.objects.create(
                name=f"{main.name} with {side.name}",
                portion_g=main_amount + side_amount,
                meal_type='B'
            )
            Ingredient.objects.create(recipe=recipe, product=main, amount_g=main_amount)
            Ingredient.objects.create(recipe=recipe, product=side, amount_g=side_amount)
            return recipe
    else:
        # Lunch/Dinner: protein + carbs + vitamins
        proteins = list(Product.objects.filter(category='PROTEIN').exclude(id__in=recent_products))
        carbs = list(Product.objects.filter(category='CARBS').exclude(id__in=recent_products))
        vitamins = list(Product.objects.filter(category='VITAMINS').exclude(id__in=recent_products))
        
        # Filter by allergies
        proteins = _filter_products_by_allergens(proteins, excluded_items)
        carbs = _filter_products_by_allergens(carbs, excluded_items)
        vitamins = _filter_products_by_allergens(vitamins, excluded_items)
        
        # Fallback if recent filter removes all
        if not proteins:
            proteins = list(Product.objects.filter(category='PROTEIN'))
            proteins = _filter_products_by_allergens(proteins, excluded_items)
        if not carbs:
            carbs = list(Product.objects.filter(category='CARBS'))
            carbs = _filter_products_by_allergens(carbs, excluded_items)
        if not vitamins:
            vitamins = list(Product.objects.filter(category='VITAMINS'))
            vitamins = _filter_products_by_allergens(vitamins, excluded_items)
        
        if proteins and carbs and vitamins:
            protein = choice(proteins)
            carb = choice(carbs)
            vit = choice(vitamins)
            
            # Calculate portions to hit target (40% protein, 40% carbs, 20% vitamins)
            protein_amount = min(500, int(target_kcal * 0.4 / protein.kcal_100g * 100)) if protein.kcal_100g > 0 else 150
            carb_amount = min(500, int(target_kcal * 0.4 / carb.kcal_100g * 100)) if carb.kcal_100g > 0 else 150
            vit_amount = min(400, int(target_kcal * 0.2 / vit.kcal_100g * 100)) if vit.kcal_100g > 0 else 100
            
            recipe = Recipe.objects.create(
                name=f"{protein.name} with {carb.name} & {vit.name}",
                portion_g=protein_amount + carb_amount + vit_amount,
                meal_type=meal_type
            )
            Ingredient.objects.create(recipe=recipe, product=protein, amount_g=protein_amount)
            Ingredient.objects.create(recipe=recipe, product=carb, amount_g=carb_amount)
            Ingredient.objects.create(recipe=recipe, product=vit, amount_g=vit_amount)
            return recipe
    
    # Fallback: create a simple meal with any available product
    all_products = list(Product.objects.all())
    if all_products:
        product = choice(all_products)
        amount = min(300, int(target_kcal / product.kcal_100g * 100)) if product.kcal_100g > 0 else 300
        recipe = Recipe.objects.create(
            name=f"{product.name}",
            portion_g=amount,
            meal_type=meal_type
        )
        Ingredient.objects.create(recipe=recipe, product=product, amount_g=amount)
        return recipe
    
    return None

def generate_plan_calorie_based(profile: dict, days: int = 7, recent_window: int = 6):
    """
    Generate a balanced meal plan with proper food categories:
    - Breakfast: breakfast foods (eggs, oats) + vitamins (fruits)
    - Lunch/Dinner: protein + carbs + vitamins
    - Excludes allergens and disliked foods
    """
    # Get excluded items from profile
    excluded_items = profile.get('allergies_and_dislikes', [])
    
    # 1) Check if we have products in all categories
    breakfast_count = Product.objects.filter(category='BREAKFAST').count()
    protein_count = Product.objects.filter(category='PROTEIN').count()
    carbs_count = Product.objects.filter(category='CARBS').count()
    vitamins_count = Product.objects.filter(category='VITAMINS').count()
    
    if not (breakfast_count and protein_count and carbs_count and vitamins_count):
        # Not enough categorized products, fallback to old method
        recipes = list(Recipe.objects.all())
        if recipes:
            return _generate_plan_old_method(profile, days, recipes)
        return MealPlan.objects.create(days=days)

    # 2) compute target kcal per day
    day_kcal = _estimate_target_kcal(profile)

    # 3) build plan with balanced meals
    plan = MealPlan.objects.create(days=days)
    total_kcal = 0
    total_price = Decimal("0.00")
    recent_product_ids = []

    for day in range(1, days+1):
        targets = _daily_targets(day_kcal)  # {"B":..., "L":..., "D":...}
        for meal_type, kcal_target in targets.items():
            recipe = _create_balanced_meal(meal_type, kcal_target, set(recent_product_ids), excluded_items)
            if recipe:
                Meal.objects.create(plan=plan, recipe=recipe, meal_type=meal_type, day_index=day)
                nut = recipe.nutrition_and_price()
                total_kcal += nut["kcal"]
                total_price += Decimal(str(nut["price"]))
                
                # Track recent products for variety
                for ing in recipe.ingredients.all():
                    recent_product_ids.append(ing.product.id)
                    if len(recent_product_ids) > recent_window * 3:  # 3 ingredients per meal
                        recent_product_ids.pop(0)

    plan.total_kcal = total_kcal
    plan.total_price = total_price
    plan.save()
    return plan

def _generate_plan_old_method(profile: dict, days: int, recipes: list):
    """Fallback to old recipe-based method if products aren't categorized"""
    shuffle(recipes)
    day_kcal = _estimate_target_kcal(profile)
    plan = MealPlan.objects.create(days=days)
    total_kcal = 0
    total_price = Decimal("0.00")
    recent_ids = []

    for day in range(1, days+1):
        targets = _daily_targets(day_kcal)
        for meal_type, kcal_target in targets.items():
            r = _pick_meal_for_target(recipes, kcal_target, set(recent_ids))
            if r:
                Meal.objects.create(plan=plan, recipe=r, meal_type=meal_type, day_index=day)
                nut = r.nutrition_and_price()
                total_kcal += nut["kcal"]
                total_price += Decimal(str(nut["price"]))
                recent_ids.append(r.id)
                if len(recent_ids) > 6:
                    recent_ids.pop(0)

    plan.total_kcal = total_kcal
    plan.total_price = total_price
    plan.save()
    return plan
