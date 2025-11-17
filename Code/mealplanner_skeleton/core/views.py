from django.contrib import messages
from django.shortcuts import render, redirect
from .models import MealPlan
from .forms import UserInputForm
from .services import generate_plan_calorie_based, _estimate_target_kcal
from decimal import Decimal
from django.core.management import call_command

def home(request):
    form = UserInputForm(initial=request.session.get("guest_profile") or None)

    if request.method == "POST":
        form = UserInputForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.session["guest_profile"] = data  # keep for this session
            # also record which profile we used to generate the latest plan
            request.session["last_generated_profile"] = data
            generate_plan_calorie_based(data, days=7)
            messages.success(request, "Plan generated based on your inputs.")
            return redirect("home")

    plan = MealPlan.objects.order_by("-created_at").first()

    # Compute a preview of the target kcal to show users before generating
    # Prefer POST data (if present) so the preview updates on form submit/validation
    if request.method == "POST":
        preview_profile = request.POST
    else:
        preview_profile = request.session.get("guest_profile") or form.initial or {}

    preview_kcal = _estimate_target_kcal(preview_profile or {})

    # Build per-day aggregates for easier display (kcal & price per day)
    plan_by_day = []
    if plan:
        for day in range(1, plan.days + 1):
            meals = list(
                plan.meals.filter(day_index=day).select_related("recipe").order_by("meal_type")
            )
            day_kcal = 0
            day_price = Decimal("0.00")
            for m in meals:
                nut = m.recipe.nutrition_and_price()
                day_kcal += int(nut.get("kcal", 0))
                try:
                    day_price += Decimal(str(nut.get("price", 0)))
                except Exception:
                    pass
            plan_by_day.append({"day": day, "meals": meals, "kcal": day_kcal, "price": day_price})

    return render(
        request,
        "home.html",
        {"form": form, "plan": plan, "preview_kcal": preview_kcal, "plan_by_day": plan_by_day},
    )


def generate(request):
    """Trigger plan generation using session-stored guest_profile or GET params.

    This mirrors the POST behavior in `home` but is useful for a dedicated URL
    that can be called from client-side code or links.
    """
    profile = request.session.get("guest_profile") or {}
    # If query params supplied, allow them to override
    if request.GET:
        profile = {**profile, **request.GET.dict()}

    # store last generated profile for visibility and debugging
    request.session["last_generated_profile"] = profile
    generate_plan_calorie_based(profile, days=7)
    from django.shortcuts import redirect
    from django.contrib import messages
    messages.success(request, "Plan generated.")
    return redirect("home")


def seed_view(request):
    """Run the demo `seed` management command and redirect back with a message."""
    from django.shortcuts import redirect
    from django.contrib import messages
    try:
        call_command("seed")
        messages.success(request, "Demo data seeded.")
    except Exception as exc:
        messages.error(request, f"Seeding failed: {exc}")
    return redirect("home")
