from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=120)
    kcal_100g = models.IntegerField()
    p_g_100g = models.FloatField()
    f_g_100g = models.FloatField()
    c_g_100g = models.FloatField()
    price_eur_100g = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self): return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    portion_g = models.IntegerField(default=300)

    def nutrition_and_price(self):
        kcal=p=fat=carb=price=0.0
        for ing in self.ingredients.all():
            ratio = ing.amount_g / 100.0
            pr = ing.product
            kcal += pr.kcal_100g * ratio
            p += pr.p_g_100g * ratio
            fat += pr.f_g_100g * ratio
            carb += pr.c_g_100g * ratio
            price += float(pr.price_eur_100g) * ratio
        return dict(kcal=int(kcal), P=round(p,1), F=round(fat,1), C=round(carb,1), price=round(price,2))

    def __str__(self): return self.name

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_g = models.FloatField()

class MealPlan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    days = models.IntegerField(default=7)
    total_kcal = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Meal(models.Model):
    MEAL = [("B","Brokastis"),("L","Pusdienas"),("D","Vakariņas")]
    plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="meals")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=1, choices=MEAL)
    day_index = models.IntegerField(default=1)
