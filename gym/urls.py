from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('gym_fitness/', views.gym_fitness, name='gym_fitness'),
    path('nutrition/', views.nutrition, name='nutrition'),
    path('resources/', views.resources, name='resources'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('log_food/', views.log_food, name='log_food'),
    path('view_food_log/', views.view_food_logs, name='view_food_log'),
    path('delete_food_log/<int:log_id>/', views.delete_food_log, name='delete_food_log'),
    path('workout/abs/', views.workout_abs, name='workout_abs'),
    path('workout/legs/', views.workout_legs, name='workout_legs'),
    path('workout/back/', views.workout_back, name='workout_back'),
    path('workout/shoulders/', views.workout_shoulders, name='workout_shoulders'),
    path('workout/arms/', views.workout_arms, name='workout_arms'),
    path('workout/chest/', views.workout_chest, name='workout_chest'),
    path('add_exercise/', views.add_exercise, name='add_exercise'),
    path('remove_exercise/<int:exercise_id>/', views.remove_exercise, name='remove_exercise'),
    path('remove_link/<int:link_id>/', views.remove_link, name='remove_link'),
]