from decimal import Decimal
from random import shuffle
from .models import Recipe, MealPlan, Meal

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

def generate_plan_calorie_based(profile: dict, days: int = 7, recent_window: int = 6):
    """
    Generate a plan that hits daily calorie targets and encourages variety.
    recent_window: number of last recipes to avoid repeating.
    """
    # 1) ensure we have recipes
    recipes = list(Recipe.objects.all())
    if not recipes:
        return MealPlan.objects.create(days=days)

    # Mix list to avoid same ordering bias
    shuffle(recipes)

    # 2) compute target kcal per day
    day_kcal = _estimate_target_kcal(profile)

    # 3) build plan
    plan = MealPlan.objects.create(days=days)
    total_kcal = 0
    total_price = Decimal("0.00")
    recent_ids = []

    for day in range(1, days+1):
        targets = _daily_targets(day_kcal)  # {"B":..., "L":..., "D":...}
        for meal_type, kcal_target in targets.items():
            r = _pick_meal_for_target(recipes, kcal_target, set(recent_ids))
            Meal.objects.create(plan=plan, recipe=r, meal_type=meal_type, day_index=day)
            nut = r.nutrition_and_price()
            total_kcal += nut["kcal"]
            total_price += Decimal(str(nut["price"]))
            # record recent for variety
            recent_ids.append(r.id)
            if len(recent_ids) > recent_window:
                recent_ids.pop(0)

    plan.total_kcal = total_kcal
    plan.total_price = total_price
    plan.save()
    return plan
