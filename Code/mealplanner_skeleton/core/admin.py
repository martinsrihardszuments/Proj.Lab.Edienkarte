from django.contrib import admin
from .models import Product, Recipe, Ingredient, MealPlan, Meal

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "kcal_100g", "p_g_100g", "f_g_100g", "c_g_100g", "price_eur_100g")

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(MealPlan)
admin.site.register(Meal)
