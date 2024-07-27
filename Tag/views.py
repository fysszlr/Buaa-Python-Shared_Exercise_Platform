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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class createTag(View):
    # def get(self, request):
    #     return render(request, 'create_tag.html')

    def post(self, request):
        token = request.GET.get('token')
        print(token)
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        tagname = request.POST.get('tagname')
        userid = getUserId(request)

        if ProblemGroup.objects.filter(name=tagname).exists():
            response['success'] = False
            response['errCode'] = 500101
            return JsonResponse(response)
        else:
            tag = ProblemGroup.objects.create(name=tagname, creator=userid)
            user=UserInfo.objects.filter(id=userid)[0]
            user.problemGroups.append(tag.id)
            user.save()
            response['data'] = {'tagid': tag.id}
            return JsonResponse(response)


class addExerciseToTag(View):
    # def get(self, request):
    #     return render(request, 'add_exercise_to_tag.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        tagid = request.POST.get('tagid')
        exerciseid = request.POST.get('exerciseid')
        userid = getUserId(request)

        if ProblemGroup.objects.filter(id=tagid).exists() == False:
            response['success'] = False
            response['errCode'] = 500201
            return JsonResponse(response)
        if Problem.objects.filter(id=exerciseid).exists() == False:
            response['success'] = False
            response['errCode'] = 500202
            return JsonResponse(response)

        tag = ProblemGroup.objects.filter(id=tagid)[0]
        if tag.creator != userid:
            response['success'] = False
            response['errCode'] = 500201
            return JsonResponse(response)
        tag.problems.append(exerciseid)
        tag.save()
        return JsonResponse(response)


class getExerciseFromTag(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        user = _
        from Exercise.views import getExerciseByID
        tagid = request.GET.get('tagid')
        tag = ProblemGroup.objects.filter(id=tagid)
        if not tag.exists():
            return JsonResponse(json_response(False, 500301, {}))
        page = int(request.GET.get('page'))
        problems = []
        problems = ProblemGroup.objects.filter(id=tagid)[0].problems
        problems = sorted(problems, reverse=True)
        thispage = []
        for i in problems:
            exercise = getExerciseByID.getExercise(i)
            if exercise['isBlock'] == False:
                exercise.__delitem__('isBlock')
                tags=exercise['tag']
                newtags=[]
                for tag in tags:
                    if int(tag['tagid']) in user.problemGroups:
                        newtags.append(tag)
                exercise['tag']=newtags
                thispage.append(exercise)
        pages = (thispage.__len__() + 19) // 20
        if page > pages:
            thispage = []
        else:
            thispage = thispage[20 * (page - 1):min(20 * page, thispage.__sizeof__())]
        response = request_template.copy()
        response['data'] = {'thispage': thispage, 'pages': pages}
        return JsonResponse(response)


class getTagInfoByID(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        tagid = request.GET.get('tagid')
        tag = ProblemGroup.objects.filter(id=tagid)
        if not tag.exists():
            return JsonResponse(json_response(False, 500401, {}))
        tag = tag[0]
        user = UserInfo.objects.filter(id=tag.creator)[0]
        data={}
        data['tagid']=tagid
        data['tagname']=tag.name
        data['createusername']=user.name
        data['createavatarurl']=user.head.url
        response=request_template.copy()
        response['data'] = data
        return JsonResponse(response)


class getCurrentUserTag(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        userid = getUserId(request)
        print(userid)
        tags = []
        for i in UserInfo.objects.filter(id=userid)[0].problemGroups:
            tags.append({'tagid': i, 'tagname': ProblemGroup.objects.filter(id=i)[0].name})
        response = request_template.copy()
        response['data'] = {'tag': tags}
        return JsonResponse(response)
