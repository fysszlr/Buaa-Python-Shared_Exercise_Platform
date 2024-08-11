from django.urls import path
from . import views

urlpatterns = [
    path('getAllUser/', views.GetAllUser.as_view(), name="getAllUser"),
    path('blockUser/', views.BlockUser.as_view(), name="blockUser"),
    path('unblockUser/', views.UnblockUser.as_view(), name="unblockUser"),
    path('getAllExercise/', views.GetAllExercise.as_view(), name="getAllExercise"),
    path('blockExercise/', views.BlockExercise.as_view(), name="blockExercise"),
    path('unblockExercise/', views.UnblockExercise.as_view(), name="unblockExercise"),
    path('getAllAdmin/', views.GetAllAdmin.as_view(), name="getAllAdmin"),
    path('createAdmin/', views.CreateAdmin.as_view(), name="createAdmin"),
    path('deleteAdmin/', views.DeleteAdmin.as_view(), name="deleteAdmin"),
]
