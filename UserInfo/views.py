from django.shortcuts import render
from UserInfo.models import UserInfo
from django.core.cache import cache
# Create your views here.


def getUserId(request):
    token = request.GET.get('token')
    if cache.get(token) is not None:
        return cache.get(token)
    else:
        for it in UserInfo.objects.all():
            if token == it.token:
                cache.set(token, it.id, timeout=900)
                return it.id