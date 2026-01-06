from django.core.management.base import BaseCommand
from core.models import Recipe, MealPlan

class Command(BaseCommand):
    help = "Clear all old recipes and meal plans to use the new dynamic system"

    def handle(self, *args, **options):
        recipe_count = Recipe.objects.count()
        plan_count = MealPlan.objects.count()
        
        Recipe.objects.all().delete()
        MealPlan.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS(f'Deleted {recipe_count} recipes and {plan_count} meal plans'))
        self.stdout.write(self.style.SUCCESS('Now meals will be generated dynamically from product categories!'))
