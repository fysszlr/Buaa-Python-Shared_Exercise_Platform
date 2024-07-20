from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

import Exercise
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
import json


def generate_token(user):
    return str(AccessToken.for_user(user))


def json_response(success, errCode, data):
    response = request_template.copy()
    response['success'] = success
    response['errCode'] = errCode
    response['data'] = data
    return response


class GetAllUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = []
        for user in User.objects.all():
            flag = False
            for it in BannedUser.objects.all():
                if user.id == it.user_id:
                    flag = True
            now = {
                "userid": user.id,
                "username": user.username,
                "avatarurl": user.head,
                "studentid": str(user.studentId) + "_EMPTY",
                "isblock": flag
            }
            users.append(now)
        return JsonResponse(json_response(True, 0, {"users": users}))


class BlockUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        userid = data["userid"]
        user = User.objects.get(id=userid)
        if user is not None:
            BannedUser.objects.create(user_id=userid)
            return JsonResponse(json_response(True, 0, {}))
        else:
            return JsonResponse(json_response(False, 200201, {}))


class UnblockUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        userid = data["userid"]
        user = User.objects.get(id=userid)
        if user is not None:
            BannedUser.objects.filter(user_id=userid).delete()
            return JsonResponse(json_response(True, 0, {}))
        else:
            return JsonResponse(json_response(False, 200301, {}))


# 补充page参数缺失情况
class GetAllExercise(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = json.loads(request.body)
        page = data["page"]
        pages = len(Problem.objects.get()) // 20
        thispage = []
        for problem in Problem.objects.all()[20 * page:20 * page + 20]:
            flag = False
            for it in BannedProblem.objects.all():
                if problem.id == it.problem_id:
                    flag = True
            now = {
                'exerciseid': problem.id,
                'createrusername': problem.name,
                'type': problem.type,
                'title': problem.name,
                'content': problem.content,
                'option': problem.option,
                'answer': problem.answer,
                'tag': problem.tags,
                'is_block': flag
            }
            thispage.append(now)
        return JsonResponse(json_response(True, 0, thispage))

class BlockExercise(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = json.loads(request.body)
        exerciseid = data["exerciseid"]
        for problem in Problem.objects.all():
            if problem.id == exerciseid:
                BannedProblem.objects.create(problem_id=exerciseid)
                return JsonResponse(json_response(True, 0, {}))
        return JsonResponse(json_response(False, 200501, {}))

class UnblockExercise(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = json.loads(request.body)
        exerciseid = data["exerciseid"]
        for problem in Problem.objects.all():
            if problem.id == exerciseid:
                BannedProblem.objects.filter(problem_id=exerciseid).delete()
                return JsonResponse(json_response(True, 0, {}))
        return JsonResponse(json_response(False, 200601, {}))

class GetAllAdmin(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        admins = []
        for admin in AdminInfo.objects.all():
            now = {
                'adminid': admin.id,
                'adminname': admin.name,
            }
            admins.append(now)
        return JsonResponse(json_response(True, 0, admins))

class CreateAdmin(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = json.loads(request.body)
        admin_name = data["adminname"]
        password = data["password"]
        for admin in AdminInfo.objects.all():
            if admin.admin == admin_name:
                return JsonResponse(json_response(False, 200801, {}))
        AdminInfo.objects.create(admin_name=admin_name, password=password)
        return JsonResponse(json_response(True, 0, {}))

class DeleteAdmin(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        data = json.loads(request.body)
        admin_id = data["adminid"]
        admin = AdminInfo.objects.get(id=admin_id)
        if admin is None:
            return JsonResponse(json_response(False, 200901, {}))
        if admin.name == 'root':
            return JsonResponse(json_response(False, 200902, {}))
        AdminInfo.objects.filter(name=admin.name).delete()
        return JsonResponse(json_response(True, 0, {}))

