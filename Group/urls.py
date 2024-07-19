from django.urls import path
from . import views

urlpatterns = [
    path('createGroup/', views.createGroup.as_view(), name='create_group'),
    path('deleteGroup/', views.deleteGroup.as_view(), name='delete_group'),
    path('joinGroup/', views.joinGroup.as_view(), name='join_group'),
    path('exitGroup/', views.exitGroup.as_view(), name='exit_group'),
    path('addTagToGroup/', views.addTagToGroup.as_view(), name='add_tag_to_group'),
    path('getTagFromGroup/', views.getTagFromGroup.as_view(), name='get_tag_from_group'),
    path('getCurrentUserGroup/', views.getCurrentUserGroup.as_view(), name='get_current_user_group'),
]
