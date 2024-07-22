from UserInfo.models import UserInfo
from .models import *
from django.core import cache

def user_authenticate(token):
    user = UserInfo.objects.get(token=token)
    if user is None:
        return False, None
    else:
        return True, user

def admin_authenticate(token):
    user = AdminInfo.objects.get(token=token)
    if user is None:
        return False, None
    else:
        return True, user