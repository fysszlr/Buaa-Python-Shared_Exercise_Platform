import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from UserInfo.models import UserInfo
from backend.authentications import admin_authenticate, user_authenticate
from backend.models import *
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


# Create your views here.
def generate_token(user):
    return str(AccessToken.for_user(user))


def json_response(success, errCode, data):
    response = request_template.copy()
    response['success'] = success
    response['errCode'] = errCode
    response['data'] = data
    return response


class UserRegisterView(APIView):
    def get(self, request):
        return render(request, 'create_customer.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # avatar = request.FILES.get('avatar')

        user = None
        try:
            user = UserInfo.objects.get(name=username)
        except:
            print('none')
        if user is not None:
            return JsonResponse(json_response(False, 100201, {}))
        else:
            user = UserInfo.objects.create(name=username, password=password)
            # user.head = ""
            group = UserGroup.objects.filter(id=1)[0]
            group.users.append(user.id)
            group.save()
            return JsonResponse(json_response(True, 0, {}))


class UserLoginView(APIView):
    def get(self, request):
        return render(request, 'login_customer.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = UserInfo.objects.get(name=username)
        except:
            return JsonResponse(json_response(False, 100101, {}))

        print(user.name)
        if user is not None and user.password == password:
            flag = False
            for it in BannedUser.objects.all():
                if user.id == it.user_id:
                    flag = True
                    break
            if not flag:
                token = generate_token(user)
                user.token = token
                user.save()
                return JsonResponse(json_response(True, 0, {"token": token}))
            else:
                return JsonResponse(json_response(False, 100102, {}))
        else:
            return JsonResponse(json_response(False, 100101, {}))


class AdminLoginView(APIView):
    def get(self, request):
        return render(request, 'login_admin.html')

    def post(self, request):
        adminname = request.POST.get('adminname')
        password = request.POST.get('password')
        user = AdminInfo.objects.get(name=adminname)

        if user is not None and user.password == password:
            token = generate_token(user)
            user.token = token
            user.save()
            return JsonResponse(json_response(True, 0, {"token": token}))
        else:
            return JsonResponse(json_response(False, 100301, {}))


class LogoutView(APIView):
    def post(self, request):
        token = request.GET.get('token')
        print(token)
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        user = UserInfo.objects.get(token=token)
        user.token = ''
        user.save()
        return JsonResponse(json_response(True, 0, {}))


class AdminLogoutView(APIView):
    def post(self, request):
        token = request.GET.get('token')
        auth, _ = admin_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        user = AdminInfo.objects.get(token=token)
        user.token = ''
        user.save()
        return JsonResponse(json_response(True, 0, {}))
