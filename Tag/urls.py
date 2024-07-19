from django.urls import path
from . import views

urlpatterns = [
    path('createTag/', views.createTag.as_view(), name='create_tag'),
    path('addExerciseToTag/', views.addExerciseToTag.as_view(), name='add_exercise_to_tag'),
    path('getExerciseFromTag/', views.getExerciseFromTag.as_view(), name='get_exercise_from_tag'),
    path('getCurrentUserTag/', views.getCurrentUserTag.as_view(), name='get_current_user_tag'),

]
