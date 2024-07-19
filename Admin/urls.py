from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register_user'),
    path('login/', views.UserLoginView.as_view(), name='login_user'),
    path('adminLogin/', views.AdminLoginView.as_view(), name='login_admin'),
    path('getAllUser/', views.getAllUsers.as_view(), name='admin_get_all_users'),

]