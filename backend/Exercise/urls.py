from django.urls import path
from . import views

urlpatterns = [
    path('createExercise/', views.createExercise.as_view(), name='create_exercise'),
    path('updateExercise/', views.updateExercise.as_view(), name='update_exercise'),
    path('getReachableExercise/', views.getReachableExercise.as_view(), name='get_reachable_exercise'),
    path('getExerciseByID/', views.getExerciseByID.as_view(), name='get_exercise_by_id'),
    path('searchExercise/', views.searchExercise.as_view(), name='search_exercise'),
    path('OCR/', views.OCR.as_view(), name='OCR'),
    path('getCommentByID/', views.GetCommentByID.as_view(), name='getCommentByID'),
    path('addComment/', views.AddComment.as_view(), name = 'addComment')
]
