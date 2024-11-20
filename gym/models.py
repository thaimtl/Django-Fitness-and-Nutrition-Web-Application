from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    FITNESS_GOALS = [
        ('light', 'Light'),
        ('moderate', 'Moderate'),
        ('intense', 'Intense'),
    ]
    SEX = [('male', 'Male'), ('female', 'Female')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    sex = models.CharField(max_length=10, choices=SEX)
    weight = models.FloatField()
    height = models.FloatField()
    fitness_goal = models.CharField(max_length=20, choices=FITNESS_GOALS)

    def __str__(self):
        return self.user.username

class NutritionPlan(models.Model):
    PLAN_CHOICES = [
        ('high_carb', 'High carb diet'),
        ('high_protein', 'High protein diet'),
        ('high_protein_high_carb_low_fat', 'High protein, high carb, low fat diet'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_plan = models.CharField(max_length=100, choices=PLAN_CHOICES, default='high_carb')
    calories = models.FloatField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)
    fats = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    def calculate_calories(self, user_profile):
        if user_profile.sex == 'male':
            if user_profile.fitness_goal == 'light':
                self.calories = round((10 * user_profile.weight + 6.25 * user_profile.height - 5 * user_profile.age + 5) * 1.375)
            elif user_profile.fitness_goal == 'moderate':
                self.calories = round((10 * user_profile.weight + 6.25 * user_profile.height - 5 * user_profile.age + 5) * 1.55)
            else:
                self.calories = round((10 * user_profile.weight + 6.25 * user_profile.height - 5 * user_profile.age + 5) * 1.725)
        else:
            if user_profile.fitness_goal == 'light':
                self.calories = round((10 * user_profile.weight + 6.25 * user_profile.height - 5 * user_profile.age - 161) * 1.375)
            elif user_profile.fitness_goal == 'moderate':
                self.calories = round((10 * user_profile.weight + 6.25 * user_profile.height - 5 * user_profile.age - 161) * 1.55)
            else:
                self.calories = round((10 * user_profile.weight + 6.25 * user_profile.height - 5 * user_profile.age - 161) * 1.725)
    def calculate_bmi(self, user_profile):
        self.bmi = round(user_profile.weight / ((user_profile.height / 100) ** 2), 1)

    def calculate_macros(self):
        if self.meal_plan == 'high_carb':
            self.protein = round(0.3 * self.calories / 4)
            self.carbs = round(0.4 * self.calories / 4)
            self.fats = round(0.3 * self.calories / 9)
        elif self.meal_plan == 'high_protein':
            self.protein = round(0.4 * self.calories / 4)
            self.carbs = round(0.3 * self.calories / 4)
            self.fats = round(0.3 * self.calories / 9)
        else:
            self.protein = round(0.4 * self.calories / 4)
            self.carbs = round(0.4 * self.calories / 4)
            self.fats = round(0.2 * self.calories / 9)
    def rank_bmi(self):
        if self.bmi < 18.5:
            return "underweight. You need to increase your calories intake."
        elif 18.5 <= self.bmi <= 24.9:
            return "normal weight. Keep it going!"
        elif 25 <= self.bmi < 29.9:
            return "overweight. You need to exercise more and/or decrease your calories intake."
        else:
            return "obese. You need to exercise more and/or decrease your calories intake."

class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=50)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    date_logged = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} - {self.user.username} - {self.date_logged}"

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    WORKOUT_TYPES = [
        ('arms', 'Arms'),
        ('back', 'Back'),
        ('chest', 'Chest'),
        ('legs', 'Legs'),
        ('shoulders', 'Shoulders'),
    ]
    type = models.CharField(null=True, blank=True, max_length=50, choices=WORKOUT_TYPES)
    name_of_exercise = models.CharField(null=True, blank=True, max_length=255)
    sets = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    weight_trained = models.CharField(null=True, blank=True, max_length=50)
    description = models.TextField(null=True, blank=True)
    is_default = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name_of_exercise} - {self.user.username} - {self.created_at}"
    
    def calculate_sets_reps(self, userprofile):
        if userprofile.fitness_goal == 'light':
            self.sets = 3
            self.reps = 8
        elif userprofile.fitness_goal == 'moderate':
            self.sets = 4
            self.reps = 10
        else:
            self.sets = 15
            self.reps = 3
class UserLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
