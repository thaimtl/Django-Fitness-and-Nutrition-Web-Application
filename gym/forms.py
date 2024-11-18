from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, NutritionPlan, FoodLog, WorkoutPlan, UserLink
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    age = forms.IntegerField()
    sex = forms.ChoiceField(choices=UserProfile.SEX)
    weight = forms.FloatField(help_text="Please enter your weight in kg.")
    height = forms.FloatField(help_text="Please enter your height in cm.")
    fitness_goal = forms.ChoiceField(choices=UserProfile.FITNESS_GOALS)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                sex=self.cleaned_data['sex'],
                weight=self.cleaned_data['weight'],
                height=self.cleaned_data['height'],
                fitness_goal=self.cleaned_data['fitness_goal']
            )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'sex', 'weight', 'height', 'fitness_goal']
        widgets = {
            'sex': forms.Select(choices=UserProfile.SEX),
            'fitness_goal': forms.Select(choices=UserProfile.FITNESS_GOALS),
        }
class NutritionPlanForm(forms.ModelForm):
    class Meta:
        model = NutritionPlan
        fields = ['meal_plan']
        widgets = {
            'meal_plan': forms.Select(choices=NutritionPlan.PLAN_CHOICES),
        }
class FoodLogForm(forms.ModelForm):
    class Meta:
        model = FoodLog
        fields = ['food_name', 'quantity', 'calories', 'protein', 'carbs', 'fats']
        widgets = {
            'food_name': forms.TextInput(attrs={'placeholder': 'e.g., Chicken Breast'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'e.g., 200 grams'}),
            'calories': forms.NumberInput(attrs={'placeholder': 'e.g., 300'}),
            'protein': forms.NumberInput(attrs={'placeholder': 'e.g., 25 grams'}),
            'carbs': forms.NumberInput(attrs={'placeholder': 'e.g., 0 grams'}),
            'fats': forms.NumberInput(attrs={'placeholder': 'e.g., 5 grams'}),
        }
class AddExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['name_of_exercise', 'sets', 'reps', 'weight_trained','description']
        widgets = {
            'name_of_exercise': forms.TextInput(attrs={'placeholder': 'e.g., Bench Press'}),
            'sets': forms.NumberInput(attrs={'placeholder': 'e.g., 3'}),
            'reps': forms.NumberInput(attrs={'placeholder': 'e.g., 8'}),
            'weight_trained': forms.TextInput(attrs={'placeholder': 'e.g., 50 kg'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter any information you feel like would be useful OR you can include a link to any video/website.'})}
class AddLinkForm(forms.ModelForm):
    class Meta:
        model = UserLink
        fields = ['title', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title'}),
            'url': forms.URLInput(attrs={'placeholder': 'Enter the URL'}),
        }