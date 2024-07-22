from django.urls import path
from . import views

urlpatterns = [
    path('getCurrentUserInfo/', views.GetCurrentUserInfoView.as_view(), name='getCurrentUserInfo'),
    path('updataAvatar/', views.UpdateAvatarView.as_view(), name='updataAvatar'),
    path('updataStudentId/', views.UpdateStudentIdView.as_view(), name='updataStudentId'),
]