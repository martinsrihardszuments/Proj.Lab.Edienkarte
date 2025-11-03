from decimal import Decimal
from .models import Recipe, MealPlan, Meal

def generate_plan(days:int=7):
    plan = MealPlan.objects.create(days=days)
    recipes = list(Recipe.objects.all())
    if not recipes:
        return plan
    total_kcal = 0
    total_price = Decimal("0.00")
    i = 0
    for d in range(1, days+1):
        for t in ["B","L","D"]:
            r = recipes[i % len(recipes)]
            Meal.objects.create(plan=plan, recipe=r, meal_type=t, day_index=d)
            nut = r.nutrition_and_price()
            total_kcal += nut["kcal"]
            total_price += Decimal(str(nut["price"]))
            i += 1
    plan.total_kcal = total_kcal
    plan.total_price = total_price
    plan.save()
    return plan
