from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse

from Auth.views import json_response
from UserInfo.models import UserInfo
from backend.authentications import user_authenticate
from backend.models import *
from UserInfo.views import getUserId
import json

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class createGroup(View):
    # def get(self, request):
    #     return render(request, 'create_group.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        groupname = request.POST.get('groupname')
        userid = getUserId(request)

        # if UserGroup.objects.filter(name=groupname).exists():
        #     response['success']=False
        #     response['errCode']=600101
        #     return JsonResponse(response)
        # else:
        # 可重名
        # 默认加入自己
        group = UserGroup.objects.create(name=groupname, creator=userid, users=[userid])
        user = _
        user.groups.append(group.id)
        user.save()
        response['data'] = {'groupid': group.id}
        return JsonResponse(response)


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class deleteGroup(APIView):
    # def get(self, request):
    #     return render(request, 'delete_group.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        groupid = int(request.POST.get('groupid'))
        userid = getUserId(request)

        if UserGroup.objects.filter(id=groupid).exists() == False:
            response['success'] = False
            response['errCode'] = 600201
            return JsonResponse(response)
        group = UserGroup.objects.filter(id=groupid)[0]
        if group.creator != userid:
            response['success'] = False
            response['errCode'] = 600202
            return JsonResponse(response)
        # 每个用户记录中所属的用户组也需要删除
        for i in group.users:
            user = UserInfo.objects.filter(id=i)[0]
            user.groups.remove(groupid)
            user.save()
        group.delete()
        return JsonResponse(response)


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class joinGroup(View):
    # def get(self, request):
    #     return render(request, 'join_group.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        groupid = int(request.POST.get('groupid'))
        userid = getUserId(request)

        if UserGroup.objects.filter(id=groupid).exists() == False:
            response['success'] = False
            response['errCode'] = 600301
            return JsonResponse(response)
        group = UserGroup.objects.filter(id=groupid)[0]
        # if userid in group.users:
        #     response['success']=False
        #     response['errCode']=600302
        #     return JsonResponse(response)
        group.users.append(userid)
        group.save()
        user = _
        user.groups.append(groupid)
        user.save()
        return JsonResponse(response)


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class exitGroup(View):

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        groupid = int(request.POST.get('groupid'))
        userid = getUserId(request)

        if UserGroup.objects.filter(id=groupid).exists() == False:
            response['success'] = False
            response['errCode'] = 600401
            return JsonResponse(response)
        if groupid == 1:
            response['success'] = False
            response['errCode'] = 600402
            return JsonResponse(response)
        if userid == UserGroup.objects.filter(id=userid)[0].creator:
            response['success'] = False
            response['errCode'] = 600403
            return JsonResponse(response)
        group = UserGroup.objects.filter(id=groupid)[0]
        group.users.remove(userid)
        group.save()
        user = _
        user.groups.remove(int(groupid))
        user.save()
        return JsonResponse(response)


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class addTagToGroup(View):
    # def get(self, request):
    #     return render(request, 'add_tag_to_group.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        groupid = int(request.POST.get('groupid'))
        tagid = int(request.POST.get('tagid'))
        userid = getUserId(request)

        if ProblemGroup.objects.filter(id=tagid).exists() == False:
            response['success'] = False
            response['errCode'] = 600501
            return JsonResponse(response)
        tag = ProblemGroup.objects.filter(id=tagid)[0]
        if tag.creator != userid:
            response['success'] = False
            response['errCode'] = 600501
            return JsonResponse(response)

        if UserGroup.objects.filter(id=groupid).exists() == False:
            response['success'] = False
            response['errCode'] = 600502
            return JsonResponse(response)
        group = UserGroup.objects.filter(id=groupid)[0]
        if tagid not in group.problemGroups:
            group.problemGroups.append(int(tagid))
            group.save()
        return JsonResponse(response)


class getTagFromGroup(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        groupid = int(request.GET.get('groupid'))
        group = UserGroup.objects.filter(id=groupid)
        if not group.exists():
            return JsonResponse(json_response(False, 600601, {}))
        tags = []
        for i in UserGroup.objects.filter(id=groupid)[0].problemGroups:
            tag = {'tagid': i, 'tagname': ProblemGroup.objects.filter(id=i)[0].name}
            user = UserInfo.objects.filter(id=ProblemGroup.objects.filter(id=i)[0].creator)[0]
            tag['createusername'] = user.name
            tag['createavatarurl'] = user.head.url
            tags.append(tag)
        response = request_template.copy()
        data = {'tag':tags}
        group = UserGroup.objects.filter(id=groupid)[0]
        data['groupname'] = group.name
        user = UserInfo.objects.filter(id=group.creator)[0]
        data['createusername'] = user.name
        data['createavatarurl'] = user.head.url
        response['data'] = data
        return JsonResponse(response)


class getCurrentUserGroup(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        userid = getUserId(request)
        groups = [{'groupid':1,'groupname':'公共用户组','createusername':'系统','createavatarurl':'/static/img/default.jpg','iscreater':False}]
        for j in UserInfo.objects.filter(id=userid)[0].groups:
            i = int(j)
            if i == 1:
                continue
            group = UserGroup.objects.filter(id=i)[0]
            groupinfo = {'groupid': i, 'groupname': group.name}
            print(group.name,group.id,i)
            user = UserInfo.objects.filter(id=group.creator)
            print(len(user))
            user = user.first()
            #return JsonResponse({'a':str(len(user))})
            groupinfo['createusername'] = user.name
            groupinfo['createavatarurl'] = user.head.url
            groupinfo['iscreater'] = (userid == group.creator)
            groups.append(groupinfo)
        response = request_template.copy()
        response['data'] = {'group': groups}
        return JsonResponse(response)


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class getGroupInfoByID(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        groupid = int(request.GET.get('groupid'))
        group = UserGroup.objects.filter(id=groupid)
        if not group.exists():
            return JsonResponse(json_response(False, 600601, {}))
        group = group[0]
        data = {}
        data['groupid'] = groupid
        data['groupname'] = group.name
        creator = UserInfo.objects.filter(id=group.creator)[0]
        data['createusername'] = creator.name
        data['createavatarurl'] = creator.head.url
        response = request_template.copy()
        response['data'] = data
        return JsonResponse(response)
