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
from backend.authentications import user_authenticate, admin_authenticate


def generate_token(user):
    return str(AccessToken.for_user(user))


def json_response(success, errCode, data):
    response = request_template.copy()
    response['success'] = success
    response['errCode'] = errCode
    response['data'] = data
    return response


class GetAllUser(APIView):

    def get(self, request):
        token = request.GET.get('token')
        auth, _ = admin_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        users = []
        for user in UserInfo.objects.all():
            flag = False
            for it in BannedUser.objects.all():
                if user.id == it.user_id:
                    flag = True
            now = {
                "userid": user.id,
                "username": user.name,
                "avatarurl": request.build_absolute_uri(user.head.url) if user.head else "",
                "studentid": str(user.studentId),
                "isblock": flag
            }
            users.append(now)
        return JsonResponse(json_response(True, 0, {"users": users}))


class BlockUser(APIView):
    def post(self, request):
        token = request.GET.get('token')
        auth, _ = admin_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        userid = request.POST.get('userid')
        user = UserInfo.objects.get(id=userid)
        
        if user is not None:
            BannedUser.objects.create(user_id=userid)
            user.token=''
            user.save()
            return JsonResponse(json_response(True, 0, {}))
        else:
            return JsonResponse(json_response(False, 200201, {}))


class UnblockUser(APIView):
    def post(self, request):
        token = request.GET.get('token')
        auth, _ = admin_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        userid = request.POST.get('userid')
        user = UserInfo.objects.get(id=userid)
        if user is not None:
            BannedUser.objects.filter(user_id=userid).delete()
            return JsonResponse(json_response(True, 0, {}))
        else:
            return JsonResponse(json_response(False, 200301, {}))


# 补充page参数缺失情况
class GetAllExercise(APIView):

    def get(self, request):
        token = request.GET.get('token')
        auth, _ = admin_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))

        page = int(request.GET.get('page'))
        if page < 1:
            page = 1
        problems = Problem.objects.all()
        pages = (len(problems) + 19) // 20
        if not problems.exists() or page > pages:
            return JsonResponse(json_response(True, 0, {'pages': pages, 'thispage': []}))

        thispage = []
        total = len(problems)
        for problem in Problem.objects.all()[20 * page - 20:min(20 * page, total)]:
            flag = False
            for it in BannedProblem.objects.all():
                if problem.id == it.problem_id:
                    flag = True
            tags=[]
            for tagid in problem.tags:
                tagname=ProblemGroup.objects.filter(id=tagid)[0].name
                tags.append({'tagid':tagid,'tagname':tagname})
            now = {
                'exerciseid': problem.id,
                'createusername': UserInfo.objects.filter(id=problem.creator)[0].name,
                'type': problem.type,
                'title': problem.name,
                'content': problem.content,
                'option': problem.option,
                'answer': problem.answer,
                'tag': tags,#problem.tags,
                'isBlock': flag
            }
            thispage.append(now)
        return JsonResponse(json_response(True, 0, {'pages': pages, 'thispage': thispage}))


class BlockExercise(APIView):
    def post(self, request):
        token = request.GET.get('token')
        auth, _ = admin_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))

        exerciseid = int(request.POST.get('exerciseid'))
        #return JsonResponse(json_response(False, 200401, str(exerciseid)))
        for problem in Problem.objects.all():
            if problem.id == exerciseid:
                BannedProblem.objects.create(problem_id=exerciseid)
                return JsonResponse(json_response(True, 0, {}))
        return JsonResponse(json_response(False, 200501, {}))


class UnblockExercise(APIView):
    def post(self, request):
        token = request.GET.get('token')
        auth, _ = admin_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))

        exerciseid = int(request.POST.get('exerciseid'))
        for problem in Problem.objects.all():
            if problem.id == exerciseid:
                BannedProblem.objects.filter(problem_id=exerciseid).delete()
                return JsonResponse(json_response(True, 0, {}))
        return JsonResponse(json_response(False, 200601, {}))


class GetAllAdmin(APIView):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = admin_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        admins = []
        for admin in AdminInfo.objects.all():
            if admin.name == 'root':
                continue
            now = {
                'adminid': admin.id,
                'adminname': admin.name,
            }
            admins.append(now)
        print(json_response(True, 0, admins))
        return JsonResponse(json_response(True, 0, {'admins':admins}))


class CreateAdmin(APIView):
    def post(self, request):
        token = request.GET.get('token')
        auth, _ = admin_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))

        admin_name = request.POST.get('adminname')
        password = request.POST.get('password')
        for admin in AdminInfo.objects.all():
            if admin.name == admin_name:
                return JsonResponse(json_response(False, 200801, {}))
        AdminInfo.objects.create(name=admin_name, password=password)
        return JsonResponse(json_response(True, 0, {}))


class DeleteAdmin(APIView):
    def post(self, request):
        token = request.GET.get('token')
        auth, _ = admin_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))

        admin_id = request.POST.get('adminid')
        admin = AdminInfo.objects.get(id=admin_id)
        if admin is None:
            return JsonResponse(json_response(False, 200901, {}))
        if admin.name == 'root':
            return JsonResponse(json_response(False, 200902, {}))
        AdminInfo.objects.filter(name=admin.name).delete()
        return JsonResponse(json_response(True, 0, {}))
