from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, NutritionPlan, WorkoutPlan, FoodLog, UserLink

admin.site.register(UserProfile)
admin.site.register(NutritionPlan)
admin.site.register(WorkoutPlan)
admin.site.register(FoodLog)
admin.site.register(UserLink)