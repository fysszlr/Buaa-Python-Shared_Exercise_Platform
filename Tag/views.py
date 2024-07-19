from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from UserInfo.models import UserInfo
from backend.models import *
import json

# Create your views here.

class createTag(View):
    # def get(self, request):
    #     return render(request, 'create_tag.html')

    def post(self, request):
        response = request_template.copy()
        data = json.loads(request.body)
        tagname = data['tagname']
        userid = 0  # 如何获取当前用户id

        if ProblemGroup.objects.filter(name=tagname).exists():
            response['success'] = False
            response['errCode'] = 500101
            return JsonResponse(response)
        else:
            tag = ProblemGroup.objects.create(name=tagname, author=userid)
            UserInfo.objects.get(id=userid).problemGroups.append(tag.id)
            UserInfo.objects.get(id=userid).save()
            response['data'] = {'tagid': tag.id}
            return JsonResponse(response)


class addExerciseToTag(View):
    # def get(self, request):
    #     return render(request, 'add_exercise_to_tag.html')

    def post(self, request):
        response = request_template.copy()
        data = json.loads(request.body)
        tagid = data['tagid']
        exerciseid = data['exerciseid']
        userid = 0  # 如何获取当前用户id

        if ProblemGroup.objects.filter(id=tagid).exists() == False:
            response['success'] = False
            response['errCode'] = 500201
            return JsonResponse(response)
        if Problem.objects.filter(id=exerciseid).exists() == False:
            response['success'] = False
            response['errCode'] = 500202
            return JsonResponse(response)

        tag = ProblemGroup.objects.get(id=tagid)
        if tag.author != userid:
            response['success'] = False
            response['errCode'] = 500201
            return JsonResponse(response)
        tag.problems.append(exerciseid)
        tag.save()
        return JsonResponse(response)


class getExerciseFromTag(View):
    def get(self, request):
        from Exercise.views import getExerciseByID
        tagid = request.GET.get('tagid')
        page = int(request.GET.get('page'))
        problems = []
        userid = 0  # 如何获取当前用户id?
        problems = ProblemGroup.objects.get(id=tagid).problems
        problems = sorted(problems, reverse=True)
        thispage = []
        for i in problems:
            exercise = getExerciseByID.getExercise(i)
            if exercise['isBlock'] == False:
                thispage.append(exercise)
        pages = (thispage.__sizeof__() + 19) // 20
        if page > pages:
            thispage = []
        else:
            thispage = thispage[20 * (page - 1):min(20 * page, thispage.__sizeof__())]
        response = request_template.copy()
        response['data'] = {'thispage': thispage, 'pages': pages}
        return JsonResponse(response)


class getCurrentUserTag(View):
    def get(self, request):
        userid = 0  # 如何获取当前用户id?
        tags = []
        for i in UserInfo.objects.get(id=userid).problemGroups:
            tags.append({'tagid': i, 'tagname': ProblemGroup.objects.get(id=i).name})
        response = request_template.copy()
        response['data'] = {'tag': tags}
        return JsonResponse(response)
