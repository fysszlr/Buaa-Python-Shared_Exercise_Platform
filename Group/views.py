from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from Auth.views import json_response
from UserInfo.models import UserInfo
from backend.authentications import user_authenticate
from backend.models import *
from UserInfo.views import getUserId
import json

# Create your views here.
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
        UserInfo.object.filter(id=userid)[0].groups.append(group.id)
        UserInfo.object.filter(id=userid)[0].save()
        response['data'] = {'groupid': group.id}
        return JsonResponse(response)


class deleteGroup(View):
    # def get(self, request):
    #     return render(request, 'delete_group.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        groupid = request.POST.get('groupid')
        userid = getUserId(request)

        if UserGroup.objects.filter(id=groupid).exists() == False:
            response['success'] = False
            response['errCode'] = 600201
            return JsonResponse(response)
        group = UserGroup.object.filter(id=userid)[0]
        if group.creator != userid:
            response['success'] = False
            response['errCode'] = 600202
            return JsonResponse(response)
        # 每个用户记录中所属的用户组也需要删除
        for i in group.users:
            UserInfo.objects.filter(id=i)[0].groups.remove(groupid)
            UserInfo.objects.filter(id=i)[0].save()
        group.delete()
        return JsonResponse(response)


class joinGroup(View):
    # def get(self, request):
    #     return render(request, 'join_group.html')

    def post(self, request):
        token = request.POST.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        groupid = request.POST.get('groupid')
        userid = getUserId(request)

        if UserGroup.objects.filter(id=groupid).exists() == False:
            response['success'] = False
            response['errCode'] = 600301
            return JsonResponse(response)
        group = UserGroup.object.filter(id=groupid)[0]
        # if userid in group.users:
        #     response['success']=False
        #     response['errCode']=600302
        #     return JsonResponse(response)
        group.users.append(userid)
        group.save()
        UserInfo.object.filter(id=userid)[0].groups.append(groupid)
        UserInfo.object.filter(id=userid)[0].save()
        return JsonResponse(response)


class exitGroup(View):
    # def get(self, request):
    #     return render(request, 'exit_group.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        groupid = request.POST.get('groupid')
        userid = getUserId(request)

        if UserGroup.objects.filter(id=groupid).exists() == False:
            response['success'] = False
            response['errCode'] = 600401
            return JsonResponse(response)
        if groupid == 1:
            response['success'] = False
            response['errCode'] = 600402
            return JsonResponse(response)
        if userid == UserGroup.object.filter(id=userid)[0].creator:
            response['success'] = False
            response['errCode'] = 600403
            return JsonResponse(response)
        group = UserGroup.object.filter(id=userid)[0]
        group.users.remove(userid)
        group.save()
        UserInfo.object.filter(id=userid)[0].groups.remove(groupid)
        UserInfo.object.filter(id=userid)[0].save()
        return JsonResponse(response)


class addTagToGroup(View):
    # def get(self, request):
    #     return render(request, 'add_tag_to_group.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        groupid = request.POST.get('groupid')
        tagid = request.POST.get('tagid')
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
        group = UserGroup.object.filter(id=userid)[0]
        group.problemGroups.append(tagid)
        group.save()
        return JsonResponse(response)


class getTagFromGroup(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        groupid = request.GET.get('groupid')
        tags = []
        for i in UserGroup.object.filter(id=groupid)[0].problemGroups:
            tag = {'tagid': i, 'tagname': ProblemGroup.object.filter(id=i)[0].name}
            user = UserInfo.object.filter(id=ProblemGroup.object.filter(id=i)[0].creator)[0]
            tag['createrusername'] = user.name
            tag['createravatarurl'] = user.head.url
            tags.append(tag)
        response = request_template.copy()
        response['data'] = {'tag': tags}
        return JsonResponse(response)


class getCurrentUserGroup(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        userid = getUserId(request)
        groups = []
        for i in UserInfo.object.filter(id=userid)[0].groups:
            group = UserGroup.object.filter(id=i)[0]
            groupinfo = {'groupid': i, 'groupname': group.name}
            groupinfo['createrusername'] = UserInfo.objects.filter(id=group.creator)[0].name
            groupinfo['createravatarurl'] = UserInfo.objects.filter(id=group.creator)[0].head.url
            groupinfo['iscreater'] = (userid == group.creator)
            groups.append(groupinfo)
        response = request_template.copy()
        response['data'] = {'group': groups}
        return JsonResponse(response)