from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register_user'),
    path('login/', views.UserLoginView.as_view(), name='login_user'),
    path('adminLogin/', views.AdminLoginView.as_view(), name='admin_login_user'),
    path('logout/', views.LogoutView.as_view(), name='logout_user'),
    path('adminLogout/', views.AdminLogoutView.as_view(), name='admin_logout_user'),
]