from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm, UserProfileForm, NutritionPlanForm, FoodLogForm, AddExerciseForm, AddLinkForm
from django.http import JsonResponse
from .models import UserProfile, NutritionPlan, FoodLog, WorkoutPlan, UserLink
from django.views.decorators.csrf import csrf_exempt
def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'message': 'Invalid credentials'})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form})

@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            default_exercises = WorkoutPlan.objects.filter(user=request.user, is_default=True)
            for exercise in default_exercises:
                exercise.calculate_sets_reps(user_profile)
                exercise.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('profile')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form})

def about(request):
    return render(request, "about.html")

def gym_fitness(request):
    return render(request, "gym_fitness.html")
def resources(request):
    return render(request, "resources.html")

@login_required
@login_required
def nutrition(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = NutritionPlanForm(request.POST)
        if form.is_valid():
            meal_plan = form.cleaned_data['meal_plan']
            nutrition_plan = NutritionPlan.objects.create(user=request.user, meal_plan=meal_plan)
            nutrition_plan.calculate_calories(user_profile)
            nutrition_plan.calculate_bmi(user_profile)
            nutrition_plan.calculate_macros()
            nutrition_plan.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'nutrition_plan': {
                        'calories': nutrition_plan.calories,
                        'protein': nutrition_plan.protein,
                        'carbs': nutrition_plan.carbs,
                        'fats': nutrition_plan.fats,
                        'bmi': nutrition_plan.bmi,
                        'bmi_rank': nutrition_plan.rank_bmi()
                    }
                })
            else:
                # For non-AJAX requests, render the template with the updated data
                form = NutritionPlanForm()
                food_log_form = FoodLogForm()
                food_logs = FoodLog.objects.filter(user=request.user).order_by('-date_logged')
                total_calories = sum(log.calories for log in food_logs)
                total_protein = sum(log.protein for log in food_logs)
                total_carbs = sum(log.carbs for log in food_logs)
                total_fats = sum(log.fats for log in food_logs)
                return render(request, 'nutrition.html', {
                    'form': form,
                    'food_log_form': food_log_form,
                    'nutrition_plan': nutrition_plan,
                    'bmi_rank': nutrition_plan.rank_bmi(),
                    'food_logs': food_logs,
                    'total_calories': total_calories,
                    'total_protein': total_protein,
                    'total_carbs': total_carbs,
                    'total_fats': total_fats
                })
    else:
        form = NutritionPlanForm()
    nutrition_plans = NutritionPlan.objects.filter(user=request.user).order_by('-created_at')
    food_log_form = FoodLogForm()
    food_logs = FoodLog.objects.filter(user=request.user).order_by('-date_logged')
    total_calories = sum(log.calories for log in food_logs)
    total_protein = sum(log.protein for log in food_logs)
    total_carbs = sum(log.carbs for log in food_logs)
    total_fats = sum(log.fats for log in food_logs)
    return render(request, 'nutrition.html', {
        'form': form,
        'food_log_form': food_log_form,
        'nutrition_plans': nutrition_plans,
        'food_logs': food_logs,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fats': total_fats
    })

@login_required
def log_food(request):
    if request.method == 'POST':
        form = FoodLogForm(request.POST)
        if form.is_valid():
            food_log = form.save(commit=False)
            food_log.user = request.user
            food_log.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'food_log': {
                        'id': food_log.id,
                        'food_name': food_log.food_name,
                        'quantity': food_log.quantity,
                        'calories': food_log.calories,
                        'protein': food_log.protein,
                        'carbs': food_log.carbs,
                        'fats': food_log.fats,
                        'date_logged': food_log.date_logged.strftime('%Y-%m-%d %H:%M:%S')
                    }
                })
            return redirect('nutrition')
    return redirect('nutrition')
@login_required
def view_food_logs(request):
    food_logs = FoodLog.objects.filter(user=request.user).order_by('-date_logged')
    total_calories = sum(log.calories for log in food_logs)
    total_protein = sum(log.protein for log in food_logs)
    total_carbs = sum(log.carbs for log in food_logs)
    total_fats = sum(log.fats for log in food_logs)
    return JsonResponse({
        'food_logs': list(food_logs.values()),
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fats': total_fats
    })

@login_required
def delete_food_log(request, log_id):
    food_log = FoodLog.objects.get(id=log_id, user=request.user)
    if request.method == 'POST':
        food_log.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('nutrition')
    return redirect('nutrition')
@login_required
def workout_abs(request):
    if request.method == 'POST':
        form = AddLinkForm(request.POST)
        if form.is_valid():
            user_link = form.save(commit=False)
            user_link.user = request.user
            user_link.save()
            return redirect('workout_abs')
    else:
        form = AddLinkForm()

    user_links = UserLink.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "workout_abs.html", {'form': form, 'user_links': user_links})
@login_required
def workout_legs(request):
    user_profile = UserProfile.objects.get(user=request.user)
    default_exercises = [
        {"name": "squats", "description": "https://www.youtube.com/watch?v=q1fCgfieNEs"},
        {"name": "lunges", "description": "https://www.youtube.com/watch?v=ugW5I-a5A-Q"},
        {"name": "leg press", "description": "https://www.youtube.com/watch?v=p5dCqF7wWUw"},
        {"name": "standing calf raises", "description": "https://www.youtube.com/watch?v=1lKjFPrYqf0"}
    ]

    # Check if default exercises already exist for the user
    existing_exercises = WorkoutPlan.objects.filter(user=request.user, is_default=True, type='legs')
    existing_exercise_names = [exercise.name_of_exercise for exercise in existing_exercises]

    # Create default exercises if they don't exist
    for exercise in default_exercises:
        if exercise['name'] not in existing_exercise_names:
            workout_plan = WorkoutPlan.objects.create(
                user=request.user,
                name_of_exercise=exercise['name'],
                description=exercise['description'],
                is_default=True,
                type='legs' 
            )
            workout_plan.calculate_sets_reps(user_profile)
            workout_plan.save()
       

    # Fetch all workout plans for the user
    user_workout_plans = WorkoutPlan.objects.filter(user=request.user, type='legs', is_default=False).order_by('-created_at')
    default_workout_plans = WorkoutPlan.objects.filter(user=request.user, type='legs', is_default=True)
    form = AddExerciseForm()
    return render(request, "workout_legs.html", {
        'user_workout_plans': user_workout_plans,
        'default_workout_plans': default_workout_plans,
        'exercise_form': form
    })
@login_required
def workout_back(request):
    user_profile = UserProfile.objects.get(user=request.user)
    default_exercises = [
        {"name": "Deadlifts", "description": "https://www.youtube.com/watch?v=r4MzxtBKyNE"},
        {"name": "Pull-Ups/Chin-Ups", "description": "https://www.youtube.com/watch?v=UfhT0OSUU0w"},
        {"name": "Lat Pulldowns", "description": "https://www.youtube.com/watch?v=SALxEARiMkw"},
        {"name": "Barbell Rows", "description": "https://www.youtube.com/watch?v=9Gf-Ourup_k"}
    ]

    # Check if default exercises already exist for the user
    existing_exercises = WorkoutPlan.objects.filter(user=request.user, is_default=True, type='back')
    existing_exercise_names = [exercise.name_of_exercise for exercise in existing_exercises]

    # Create default exercises if they don't exist
    for exercise in default_exercises:
        if exercise['name'] not in existing_exercise_names:
            workout_plan = WorkoutPlan.objects.create(
                user=request.user,
                name_of_exercise=exercise['name'],
                description=exercise['description'],
                is_default=True,
                type='back' 
            )
            workout_plan.calculate_sets_reps(user_profile)
            workout_plan.save()
       

    # Fetch all workout plans for the user
    user_workout_plans = WorkoutPlan.objects.filter(user=request.user, type='back', is_default=False).order_by('-created_at')
    default_workout_plans = WorkoutPlan.objects.filter(user=request.user, type='back', is_default=True)
    form = AddExerciseForm()
    return render(request, "workout_back.html", {
        'user_workout_plans': user_workout_plans,
        'default_workout_plans': default_workout_plans,
        'exercise_form': form
    })
@login_required
def workout_shoulders(request):
    user_profile = UserProfile.objects.get(user=request.user)
    default_exercises = [
        {"name": "overhead press", "description": "https://www.youtube.com/watch?v=Did01dFR3Lk"},
        {"name": "lateral raises", "description": "https://www.youtube.com/watch?v=XPPfnSEATJA"},
        {"name": "face pulls", "description": "https://www.youtube.com/watch?v=0Po47vvj9g4"},
        {"name": "rear delt fly", "description": "https://www.youtube.com/watch?v=nlkF7_2O_Lw"}
    ]

    # Check if default exercises already exist for the user
    existing_exercises = WorkoutPlan.objects.filter(user=request.user, is_default=True, type='shoulders')
    existing_exercise_names = [exercise.name_of_exercise for exercise in existing_exercises]

    # Create default exercises if they don't exist
    for exercise in default_exercises:
        if exercise['name'] not in existing_exercise_names:
            workout_plan = WorkoutPlan.objects.create(
                user=request.user,
                name_of_exercise=exercise['name'],
                description=exercise['description'],
                is_default=True,
                type='shoulders' 
            )
            workout_plan.calculate_sets_reps(user_profile)
            workout_plan.save()
       

    # Fetch all workout plans for the user
    user_workout_plans = WorkoutPlan.objects.filter(user=request.user, type='shoulders', is_default=False).order_by('-created_at')
    default_workout_plans = WorkoutPlan.objects.filter(user=request.user, type='shoulders', is_default=True)
    form = AddExerciseForm()
    return render(request, "workout_shoulders.html", {
        'user_workout_plans': user_workout_plans,
        'default_workout_plans': default_workout_plans,
        'exercise_form': form
    })
@login_required
def workout_arms(request):
    user_profile = UserProfile.objects.get(user=request.user)
    default_exercises = [
        {"name": "Bicep Curls", "description": "https://www.youtube.com/shorts/803JIAWBj_c"},
        {"name": "Close-Grip Bench Press", "description": "https://www.youtube.com/watch?v=DzA2xZhDGeo"},
        {"name": "Hammer Curls", "description": "https://www.youtube.com/watch?v=CFBZ4jN1CMI"},
        {"name": "Tricep Dips", "description": "https://www.youtube.com/watch?v=0326dy_-CzM"}
    ]

    # Check if default exercises already exist for the user
    existing_exercises = WorkoutPlan.objects.filter(user=request.user, is_default=True, type='arms')
    existing_exercise_names = [exercise.name_of_exercise for exercise in existing_exercises]

    # Create default exercises if they don't exist
    for exercise in default_exercises:
        if exercise['name'] not in existing_exercise_names:
            workout_plan = WorkoutPlan.objects.create(
                user=request.user,
                name_of_exercise=exercise['name'],
                description=exercise['description'],
                is_default=True,
                type='arms' 
            )
            workout_plan.calculate_sets_reps(user_profile)
            workout_plan.save()
       

    # Fetch all workout plans for the user
    user_workout_plans = WorkoutPlan.objects.filter(user=request.user, type='arms', is_default=False).order_by('-created_at')
    default_workout_plans = WorkoutPlan.objects.filter(user=request.user, type='arms', is_default=True)
    form = AddExerciseForm()
    return render(request, "workout_arms.html", {
        'user_workout_plans': user_workout_plans,
        'default_workout_plans': default_workout_plans,
        'exercise_form': form
    })
@login_required
def workout_chest(request):
    user_profile = UserProfile.objects.get(user=request.user)
    default_exercises = [
        {"name": "push-ups", "description": "https://www.youtube.com/watch?v=AhdtowFDKT0"},
        {"name": "dumbbell bench press", "description": "https://www.youtube.com/watch?v=IP4oeKh1Sd4"},
        {"name": "dumbbell flyes", "description": "https://www.youtube.com/watch?v=eozdVDA78K0"},
        {"name": "cable crossover", "description": "https://www.youtube.com/watch?v=JUDTGZh4rhg"}
    ]

    # Check if default exercises already exist for the user
    existing_exercises = WorkoutPlan.objects.filter(user=request.user, is_default=True, type='chest')
    existing_exercise_names = [exercise.name_of_exercise for exercise in existing_exercises]

    # Create default exercises if they don't exist
    for exercise in default_exercises:
        if exercise['name'] not in existing_exercise_names:
            workout_plan = WorkoutPlan.objects.create(
                user=request.user,
                name_of_exercise=exercise['name'],
                description=exercise['description'],
                is_default=True,
                type='chest' 
            )
            workout_plan.calculate_sets_reps(user_profile)
            workout_plan.save()
       

    # Fetch all workout plans for the user
    user_workout_plans = WorkoutPlan.objects.filter(user=request.user, type='chest', is_default=False).order_by('-created_at')
    default_workout_plans = WorkoutPlan.objects.filter(user=request.user, type='chest', is_default=True)
    form = AddExerciseForm()
    return render(request, "workout_chest.html", {
        'user_workout_plans': user_workout_plans,
        'default_workout_plans': default_workout_plans,
        'exercise_form': form
    })
@login_required
def add_exercise(request):
    if request.method == 'POST':
        form = AddExerciseForm(request.POST)
        if form.is_valid():
            workout_plan = form.save(commit=False)
            workout_plan.user = request.user
            workout_plan.type = request.POST.get('workout_type', 'chest')
            workout_plan.save()
            workout_type = workout_plan.type
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'workout_plan': {
                        'name_of_exercise': workout_plan.name_of_exercise,
                        'sets': workout_plan.sets,
                        'reps': workout_plan.reps,
                        'description': workout_plan.description
                    }
                })
            return redirect(f'workout_{workout_type}')
    return redirect('index')
@login_required
@csrf_exempt
def remove_exercise(request, exercise_id):
    if request.method == 'POST':
        try:
            workout_plan = WorkoutPlan.objects.get(id=exercise_id, user=request.user)
            if workout_plan.is_default:
                return JsonResponse({'success': False, 'error': 'Cannot remove default exercise'})
            workout_plan.delete()
            return redirect(f'workout_{workout_plan.type}')
        except WorkoutPlan.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Exercise does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def remove_link(request, link_id):
    if request.method == 'POST':
        link = get_object_or_404(UserLink, id=link_id, user=request.user)
        link.delete()
        return redirect('workout_abs')
    return JsonResponse({'success': False, 'error': 'Invalid request method'})      