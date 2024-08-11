from django.urls import path
from . import views

urlpatterns = [
    path('getCurrentUserInfo/', views.GetCurrentUserInfoView.as_view(), name='getCurrentUserInfo'),
    path('updateAvatar/', views.UpdateAvatarView.as_view(), name='updataAvatar'),
    path('updateStudentID/', views.UpdateStudentIdView.as_view(), name='updataStudentId'),
]