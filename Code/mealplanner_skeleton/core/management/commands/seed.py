from django.core.management.base import BaseCommand
from core.models import Product, Recipe, Ingredient

class Command(BaseCommand):
    help = "Ievieto demo produktus un receptes"

    def handle(self, *args, **opts):
        eggs, _ = Product.objects.get_or_create(
            name="Olas", kcal_100g=155, p_g_100g=13, f_g_100g=11, c_g_100g=1.1, price_eur_100g=0.60
        )
        oats, _ = Product.objects.get_or_create(
            name="Auzu pārslas", kcal_100g=379, p_g_100g=13, f_g_100g=7, c_g_100g=67, price_eur_100g=0.20
        )
        chicken, _ = Product.objects.get_or_create(
            name="Vistas fileja", kcal_100g=165, p_g_100g=31, f_g_100g=3.6, c_g_100g=0, price_eur_100g=0.90
        )
        rice, _ = Product.objects.get_or_create(
            name="Rīsi", kcal_100g=360, p_g_100g=7, f_g_100g=0.6, c_g_100g=79, price_eur_100g=0.18
        )

        r1, _ = Recipe.objects.get_or_create(name="Omlete ar auzām", portion_g=300)
        Ingredient.objects.get_or_create(recipe=r1, product=eggs, amount_g=150)
        Ingredient.objects.get_or_create(recipe=r1, product=oats, amount_g=50)

        r2, _ = Recipe.objects.get_or_create(name="Vistas rīsi", portion_g=350)
        Ingredient.objects.get_or_create(recipe=r2, product=chicken, amount_g=200)
        Ingredient.objects.get_or_create(recipe=r2, product=rice, amount_g=150)

        self.stdout.write(self.style.SUCCESS("Demo produkti un receptes sagatavotas."))
