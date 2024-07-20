from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from UserInfo.models import UserInfo
from backend.models import *
import datetime

# Create your views here.
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
        user=UserInfo.objects.create(name=username, password=password,log=[(datetime.datetime.now().timestamp(),'register')])
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
                customer.log.append((datetime.datetime.now().timestamp(),'login'))
                customer.save()
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
