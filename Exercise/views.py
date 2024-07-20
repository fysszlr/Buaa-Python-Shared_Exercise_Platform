from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from UserInfo.models import UserInfo
from backend.models import *
import json
from django.core.cache import cache
# Create your views here.

class createExercise(View):
    def get(self, request):
        return render(request, 'create_exercise.html')

    def post(self, request):
        response = request_template.copy()
        data = json.loads(request.body)

        if data['type'] not in [0, 1, 2, 10]:
            response['success'] = False
            response['errCode'] = 400101
            return JsonResponse(response)
        for i in data['tagid']:
            if ProblemGroup.objects.filter(id=i).exists() == False:
                response['success'] = False
                response['errCode'] = 400102
                return JsonResponse(response)

        # TODO:标题、正文、选项、答案的合规性审查,如何获取autor?

        exercise = Problem.objects.create(
            type=data['type'],
            name=data['title'],
            content=data['content'],
            option=data.get('option', []),
            answer=data['answer'],
            tags=data['tagid'],
            author=0  # data['author']
        )
        response['data'] = {'exerciseid': exercise.id}
        return JsonResponse(response)


class updateExercise(View):
    def get(self, request):
        return render(request, 'create_exercise.html')

    def post(self, request):
        response = request_template.copy()
        data = json.loads(request.body)
        exerciseid = data['exerciseid']
        newdata = data['newdata']
        userid = 0  # 如何获取当前用户id

        if Problem.objects.filter(id=exerciseid).author != userid:
            response['success'] = False
            response['errCode'] = 400201
            return JsonResponse(response)
        if data['type'] not in [0, 1, 2, 10]:
            response['success'] = False
            response['errCode'] = 400202
            return JsonResponse(response)
        for i in data['tagid']:
            if ProblemGroup.objects.filter(id=i).exists() == False:
                response['success'] = False
                response['errCode'] = 400403
                return JsonResponse(response)

        # TODO:标题、正文、选项、答案的合规性审查,如何获取autor?

        # 更新数据
        exercise = Problem.objects.get(id=exerciseid)
        exercise.type = data['type']
        exercise.name = data['title']
        exercise.content = data['content']
        exercise.option = data.get('option', [])
        exercise.answer = data['answer']
        exercise.tags = data['tagid']
        exercise.save()
        response['data'] = {'exerciseid': exercise.id}
        return JsonResponse(response)


class getReachableExercise(View):
    def get(self, request):
        page = int(request.GET.get('page'))
        problems = set(int)
        userid = 0  # 如何获取当前用户id?
        problems = cache.get(userid)
        if not problems:
            # 从大到小排序
            problems = list(getReachableExercise.getReachableExercise(userid))
            problems = sorted(problems, reverse=True)
            cache.set(userid, problems, 60*15)#缓存15分钟
        pages = (problems.__sizeof__() + 19) // 20
        if page > pages:
            problems = []
        else:
            problems = problems[20 * (page - 1):min(20 * page, problems.__sizeof__())]
        thispage = []
        for i in problems:
            thispage.append(getExerciseByID.getExercise(i))

        response = request_template.copy()
        response['data'] = {'thispage': thispage, 'pages': pages}
        return JsonResponse(response)

    def getReachableExercise(userid):
        problems = set(int)
        # 所有共享群组
        for userGroup in UserInfo.objects.get(id=userid).groups:
            for problemGroup in UserGroup.objects.get(id=userGroup).problems:
                problems = problems.union(set(ProblemGroup.objects.get(id=problemGroup).problems))
        # 自己创建的题目
        problems = problems.union(set(UserInfo.objects.filter(id=userid).problems))
        # 去除被封禁的题目
        for bannedProblem in BannedProblem.objects.all():
            problems.remove(bannedProblem.problem)
        return problems


class getExerciseByID(View):
    def get(self, request):
        exerciseid = request.GET.get('exerciseid')
        data = getExerciseByID.getExercise(exerciseid)
        response = request_template.copy()
        response['isBlock'] = data.pop('isBlock')
        response['data'] = data  # 或者data中包含data和isblock？
        return JsonResponse(response)

    def getExercise(exerciseid):
        if Problem.objects.filter(id=exerciseid).exists() == False:
            return {}
        problem = Problem.objects.get(id=exerciseid)
        exercise = {}
        exercise['exerciseid'] = problem.id
        exercise['createusername'] = UserInfo.objects.get(id=problem.author).name
        exercise['type'] = problem.type
        exercise['title'] = problem.name
        exercise['content'] = problem.content
        exercise['option'] = problem.option
        exercise['answer'] = problem.answer
        tag = []
        for j in problem.tags:
            tag.append({'tagid': j, 'tagname': ProblemGroup.objects.get(id=j).name})
        exercise['tag'] = tag
        if BannedProblem.objects.filter(problem=problem.id).exists():
            exercise['isBlock'] = True
        else:
            exercise['isBlock'] = False
        return exercise


class searchExercise(View):
    def get(self, request):
        page = int(request.GET.get('page'))
        type = int(request.GET.get('type'))
        pattern = request.GET.get('pattern')
        problems = set(int)
        userid = 0  # 如何获取当前用户id?
        problems = list(getReachableExercise.getReachableExercise(userid))
        problems = sorted(problems, reverse=True)
        thispage = []
        for i in problems:
            exercise = getExerciseByID.getExercise(i)
            if type == 'title':
                if pattern in exercise['title']:
                    thispage.append(exercise)
            elif type == 'tag':
                if pattern in exercise['tag']['tagname']:
                    thispage.append(exercise)
        pages = (thispage.__sizeof__() + 19) // 20
        if page > pages:
            thispage = []
        else:
            thispage = thispage[20 * (page - 1):min(20 * page, thispage.__sizeof__())]

        response = request_template.copy()
        response['data'] = {'thispage': thispage, 'pages': pages}
        return JsonResponse(response)
