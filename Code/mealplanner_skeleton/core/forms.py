from django import forms

class UserInputForm(forms.Form):
    SEX = [("M","Male"), ("F","Female")]
    ACTIVITY = [("LOW","Low"), ("MED","Moderate"), ("HIGH","High")]
    GOAL = [("CUT","Lose"), ("KEEP","Maintain"), ("GAIN","Gain")]
    
    # Common allergens and dietary restrictions
    ALLERGENS = [
        ('milk', 'Milk/Dairy'),
        ('eggs', 'Eggs'),
        ('fish', 'Fish'),
        ('shellfish', 'Shellfish'),
        ('nuts', 'Tree Nuts'),
        ('peanuts', 'Peanuts'),
        ('wheat', 'Wheat/Gluten'),
        ('soy', 'Soy'),
        ('meat', 'Meat'),
        ('chicken', 'Chicken'),
        ('pork', 'Pork'),
        ('beef', 'Beef'),
        ('rice', 'Rice'),
        ('pasta', 'Pasta'),
        ('potato', 'Potato'),
        ('tomato', 'Tomato'),
        ('onion', 'Onion'),
        ('garlic', 'Garlic'),
        ('cheese', 'Cheese'),
        ('yogurt', 'Yogurt'),
        ('bread', 'Bread'),
    ]

    age = forms.IntegerField(min_value=10, max_value=100)
    height_cm = forms.IntegerField(min_value=100, max_value=230, label="Height (cm)")
    weight_kg = forms.FloatField(min_value=30, max_value=300, label="Weight (kg)")
    sex = forms.ChoiceField(choices=SEX, initial="M")
    activity = forms.ChoiceField(choices=ACTIVITY, initial="MED")
    goal = forms.ChoiceField(choices=GOAL, initial="KEEP")
    diet_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":2}))
    target_kcal = forms.IntegerField(required=False, min_value=800, max_value=6000, label="Target calories (optional)")
    
    # Multi-select for allergens and dislikes
    allergies_and_dislikes = forms.MultipleChoiceField(
        choices=ALLERGENS,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'allergen-checkbox'
        }),
        label="Allergies & Foods to Avoid",
        help_text="Select all items you want to exclude from your meal plan"
    )
