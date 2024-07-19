from django.urls import path
from . import views

urlpatterns = [
    path('addWrongLog/', views.addWrongLog.as_view(), name='add_wrong_log'),
    path('addRightLog/', views.addRightLog.as_view(), name='add_right_log'),
]
