"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from customer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Auth/register/', UserRegisterView.as_view(), name='register_user'),
    path('Auth/login/', UserLoginView.as_view(), name='login_user'),
    path('Auth/adminLogin/', AdminLoginView.as_view(), name='login_admin'),
    path('Admin/getAllUser/', getAllUsers.as_view(), name='admin_get_all_users'),
    path('Exercise/createExercise/', createExercise.as_view(), name='create_exercise'),
    path('Exercise/updateExercise/', updateExercise.as_view(), name='create_exercise'),
    path('Exercise/getReachableExercise/', getReachableExercise.as_view(), name='get_Reachable_exercise'),
    path('Exercise/getExerciseByID/', getExerciseByID.as_view(), name='get_exercise_by_id'),
    path('Exercise/searchExercise/', searchExercise.as_view(), name='search_exercise'),
    path('Tag/createTag/', createTag.as_view(), name='create_tag'),
    path('Tag/addExerciseToTag/', addExerciseToTag.as_view(), name='add_exercise_to_tag'),
    path('Tag/getExerciseFromTag/', getExerciseFromTag.as_view(), name='get_exercise_from_tag'),
    path('Tag/getCurrentUserTag/', getCurrentUserTag.as_view(), name='get_current_user_tag'),
    path('Group/createGroup/', createGroup.as_view(), name='create_group'),
    path('Group/deleteGroup/', deleteGroup.as_view(), name='delete_group'),
    path('Group/joinGroup/', joinGroup.as_view(), name='join_group'),
    path('Group/exitGroup/', exitGroup.as_view(), name='exit_group'),
    path('Group/addTagToGroup/', addTagToGroup.as_view(), name='add_tag_to_group'),
    path('Group/getTagFromGroup/', getTagFromGroup.as_view(), name='get_tag_from_group'),
    path('Group/getCurrentUserGroup/', getCurrentUserGroup.as_view(), name='get_current_user_group'),
    path('Log/addWrongLog/', addWrongLog.as_view(), name='add_wrong_log'),
    path('Log/addRightLog/', addRightLog.as_view(), name='add_right_log'),
]
