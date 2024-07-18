from django.shortcuts import render
import datetime
import json

# Create your views here.

# customer/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from django.views import View
from django.contrib.auth.hashers import make_password, check_password

request_template = {
    "success": True,
    "errCode": 0,
    "data": {
    }
}

# 创建用户的视图
class UserRegisterView(View):
    def get(self, request):
        return render(request, 'create_customer.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        #avatar = request.FILES.get('avatar')
        response=request_template.copy()

        if(UserInfo.objects.filter(name=username).exists()):
            #用户已存在
            response['errCode']=100201
            response['success']=False
            return JsonResponse(response)

        # 创建并保存用户
        user=UserInfo.objects.create(name=username, password=password,log=str(datetime.datetime.now())+' 创建用户')
        user.groups.append(1)
        return JsonResponse(response)

# 获取用户信息的视图,待更改
class GetCustomerView(View):
    def get(self, request, username):
        try:
            customer = UserInfo.objects.get(name=username)
            return HttpResponse(f'Username: {customer.username}, Password: {customer.password}')
        except UserInfo.DoesNotExist:
            return HttpResponse("User does not exist")

# 登录验证视图
class UserLoginView(View):
    def get(self, request):
        return render(request, 'login_customer.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        response=request_template.copy()

        try:
            customer = UserInfo.objects.get(name=username)
            if password == customer.password:
                if BannedUser.objects.filter(user=customer.id).exists():
                    #已被封禁
                    response['errCode']=100102
                    response['success']=False
                    return JsonResponse(response)
                #成功登录
                response['data']={'token':customer.token}
                return JsonResponse(response)
            else:
                #密码错误
                response['errCode']=100101
                response['success']=False
                return JsonResponse(response)
        except UserInfo.DoesNotExist:
            #用户不存在
            response['errCode']=100101
            response['success']=False
            return JsonResponse(response)

# 管理员登录验证视图
class AdminLoginView(View):
    def get(self, request):
        return render(request, 'login_admin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        response=request_template.copy()

        try:
            admin = AdminInfo.objects.get(name=username)
            if password == admin.password:
                #成功登录
                response['data']={'token':admin.token}
                return JsonResponse(response)
            else:
                #密码错误
                response['errCode']=100301
                response['success']=False
                return JsonResponse(response)
        except AdminInfo.DoesNotExist:
            #用户不存在
            response['errCode']=100301
            response['success']=False
            return JsonResponse(response)

class getAllUsers(View):
    def get(self, request):
        response=request_template.copy()
        response['data']={'users':[]}
        for user in UserInfo.objects.all():
            userinfo={}
            userinfo['userid']=user.id
            userinfo['username']=user.name
            userinfo['avatarurl']=user.head.url
            userinfo['studentid']=user.studentId
            if BannedUser.objects.filter(user=user.id).exists():
                userinfo['isblock']=True
            else:
                userinfo['isblock']=False
            response['data']['users'].append(userinfo)
        return JsonResponse(response)

class createExercise(View):
    def get(self, request):
        return render(request, 'create_exercise.html')
    
    def post(self, request):
        response=request_template.copy()
        data = json.loads(request.body)

        if(data['type'] not in [0,1,2,10]):
            response['success']=False
            response['errCode']=400401
            return JsonResponse(response)
        for i in data['tagid']:
            if ProblemGroup.objects.filter(id=i).exists()==False:
                response['success']=False
                response['errCode']=400402
                return JsonResponse(response)
        
        #TODO:标题、正文、选项、答案的合规性审查,如何获取autor?

        exercise = Problem.objects.create(
            type=data['type'],
            name=data['title'],
            content=data['content'],
            option=data.get('option', []),
            answer=data['answer'],
            tags=data['tagid'],
            author=0#data['author']
        )
        response['data']={'exerciseid':exercise.id}
        print(exercise.__str__())
        return JsonResponse(response)
