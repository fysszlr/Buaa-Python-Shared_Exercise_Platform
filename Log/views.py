from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from UserInfo.models import UserInfo
from backend.models import *
import datetime
import json

# Create your views here.

class addWrongLog(View):
    # def get(self, request):
    #     return render(request, 'add_wrong_log.html')

    def post(self, request):
        response = request_template.copy()
        data = json.loads(request.body)
        exerciseid = data['exerciseid']
        userid = 0  # 如何获取当前用户id

        if Problem.objects.filter(id=exerciseid).exists() == False:
            response['success'] = False
            response['errCode'] = 700101
            return JsonResponse(response)
        timestamp = int(datetime.datetime.now().timestamp())
        UserInfo.objects.get(id=userid).problemlog.append((timestamp, exerciseid, False))
        UserInfo.objects.get(id=userid).save()
        response['data'] = {'timestamp': timestamp}
        return JsonResponse(response)


class addRightLog(View):
    # def get(self, request):
    #     return render(request, 'add_right_log.html')

    def post(self, request):
        response = request_template.copy()
        data = json.loads(request.body)
        exerciseid = data['exerciseid']
        userid = 0  # 如何获取当前用户id

        if Problem.objects.filter(id=exerciseid).exists() == False:
            response['success'] = False
            response['errCode'] = 700201
            return JsonResponse(response)
        timestamp = int(datetime.datetime.now().timestamp())
        UserInfo.objects.get(id=userid).problemlog.append((timestamp, exerciseid, True))
        UserInfo.objects.get(id=userid).save()
        response['data'] = {'timestamp': timestamp}
        return JsonResponse(response)

