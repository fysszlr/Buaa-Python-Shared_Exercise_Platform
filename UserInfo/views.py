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
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991,{}))
        for it in UserInfo.objects.all():
            if it.token == token:
                user = it

        assert (user is not None)
        response_data = {
            'username': user.name,
            'avatar': request.build_absolute_uri(user.head.url) if user.head else "",
            'studentid': user.studentId,
        }
        return JsonResponse(json_response(True, 0, response_data))

# 有问题
class UpdateAvatarView(APIView):
    def post(self, request):
        token = request.POST.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991,{}))
        for it in UserInfo.objects.all():
            if it.token == token:
                user = it
        assert (user is not None)

        head = request.FILES.get('newavatar')
        user.head = head
        user.save()
        return JsonResponse(json_response(True, 0, {"avatarurl":request.build_absolute_uri(user.head.url) if user.head else ""}))

class UpdateStudentIdView(APIView):
    def post(self, request):
        token = request.POST.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991,{}))
        for it in UserInfo.objects.all():
            if it.token == token:
                user = it
        assert (user is not None)

        new_student_id = request.POST.get('newstudentid')
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