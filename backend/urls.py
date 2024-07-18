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
    path('get/<str:username>/', GetCustomerView.as_view(), name='get_customer'),
]
