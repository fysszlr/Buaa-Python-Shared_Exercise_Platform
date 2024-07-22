from django.shortcuts import render
from UserInfo.models import UserInfo
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from .models import UserInfo
import json
from backend.models import *
from backend.authentications import user_authenticate


# Create your views here.
def json_response(success, errCode, data):
    response = request_template.copy()
    response['success'] = success
    response['errCode'] = errCode
    response['data'] = data
    return response


class GetCurrentUserInfoView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        user, _ = user_authenticate(token)
        for it in UserInfo.objects.all():
            if it.token == token:
                user = it

        assert (user is not None)
        response_data = {
            'username': user.username,
            'avatar': user.head,
            'studentid': user.studentId,
        }
        return JsonResponse(json_response(True, 0, response_data))

# 有问题
class UpdateAvatarView(APIView):
    def post(self, request):
        token = request.GET.get('token')
        user, _ = user_authenticate(token)
        for it in UserInfo.objects.all():
            if it.token == token:
                user = it
        assert (user is not None)

        data = json.loads(request.body)
        head = data['newavatar']
        user.head = head
        user.save()
        return JsonResponse(json_response(True, 0, {}))

class UpdateStudentIdView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token = request.GET.get('token')
        user = None
        for it in UserInfo.objects.all():
            if it.token == token:
                user = it
        assert (user is not None)

        data = json.loads(request.body)
        new_student_id = data['newstudentid']
        user.studentid = new_student_id
        user.save()
        return JsonResponse(json_response(True, 0, {'studentid': new_student_id}))


def getUserId(request):
    token = request.GET.get('token')
    if cache.get(token) is not None:
        return cache.get(token)
    else:
        for it in UserInfo.objects.all():
            if token == it.token:
                cache.set(token, it.id, timeout=900)
                return it.id