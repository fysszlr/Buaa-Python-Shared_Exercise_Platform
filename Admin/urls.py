from django.urls import path
from . import views

urlpatterns = [
    path('getAllUser/', views.GetAllUser, name="getAllUser"),
    path('blockUser/', views.BlockUser, name="blockUser"),
    path('unblockUser/', views.UnblockUser, name="unblockUser"),
    path('getAllExercise', views.GetAllExercise, name="getAllExercise"),
    path('blockExercise/', views.BlockExercise, name="blockExercise"),
    path('unblockExercise/', views.UnblockExercise, name="unblockExercise"),
    path('getAllAdmin/', views.GetAllAdmin, name="getAllAdmin"),
    path('createAdmin/', views.CreateAdmin, name="createAdmin"),
    path('deleteAdmin/', views.DeleteAdmin, name="deleteAdmin"),
]
