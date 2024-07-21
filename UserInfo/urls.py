from django.urls import path
from . import views

urlpatterns = [
    path('getCurrentUserInfo/', views.GetCurrentUserInfoView, name='getCurrentUserInfo'),
    path('updataAvatar/', views.UpdateAvatarView, name='updataAvatar'),
    path('updataStudentId/', views.UpdateStudentIdView, name='updataStudentId'),
]