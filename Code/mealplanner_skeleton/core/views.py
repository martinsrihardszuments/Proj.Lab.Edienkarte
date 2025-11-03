from django.shortcuts import render, redirect
from .models import MealPlan
from .services import generate_plan

def home(request):
    plan = MealPlan.objects.order_by("-created_at").first()
    return render(request, "home.html", {"plan": plan})

def generate(request):
    generate_plan(days=7)
    return redirect("home")

# convenience route to seed demo data from code
from django.http import HttpResponse
from django.core.management import call_command

def seed_view(request):
    call_command("seed")
    return redirect("home")
