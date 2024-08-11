from UserInfo.models import UserInfo
from .models import *
from django.core import cache

def user_authenticate(token):
    user = UserInfo.objects.filter(token=token)
    if not user.exists():
        return False, None
    else:
        return True, user[0]

def admin_authenticate(token):
    user = AdminInfo.objects.filter(token=token)
    if not user.exists():
        return False, None
    else:
        return True, user[0]