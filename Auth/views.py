import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from UserInfo.models import UserInfo
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
        # data = json.loads(request.body)
        # username = data['username']
        # password = data['password']
        username = request.POST.get('username')
        password = request.POST.get('password')
        # avatar = request.FILES.get('avatar')

        user = UserInfo.objects.get(username=username)
        if user is not None:
            return JsonResponse(json_response(False, 100201, {}))
        else:
            UserInfo.objects.create(username=username, password=password)
            return JsonResponse(json_response(True, 0, {}))


class UserLoginView(APIView):
    def get(self, request):
        return render(request, 'login_customer.html')

    def post(self, request):
        # data = json.loads(request.body)
        # username = data['username']
        # password = data['password']
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = AdminInfo.objects.get(name=username)

        print(user)
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
        # data = json.loads(request.body)
        # adminname = data['adminname']
        # password = data['password']
        adminname = request.POST.get('adminname')
        password = request.POST.get('password')
        user = AdminInfo.objects.get(name=adminname)

        print(user)
        if user is not None and user.password == password:
            token = generate_token(user)
            user.token = token
            user.save()
            return JsonResponse(json_response(True, 0, {"token": token}))
        else:
            return JsonResponse(json_response(False, 100301, {}))

class LogoutView(APIView):
    def post(self, request):
        response = request_template.copy()
        token = request.GET.get('token')
        user = UserInfo.objects.get(token=token)
        return JsonResponse(json_response(True, 0, {}))

class AdminLogoutView(APIView):
    def post(self, request):
        response = request_template.copy()
        token = request.GET.get('token')
        user = AdminInfo.objects.get(token=token)
        return JsonResponse(json_response(True, 0, {}))
