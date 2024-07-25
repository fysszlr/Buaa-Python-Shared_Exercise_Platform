from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from Auth.views import json_response
from UserInfo.models import UserInfo
from backend.authentications import user_authenticate
from backend.models import *
from UserInfo.views import getUserId
import json
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from PIL import Image
import pytesseract
import os
import fitz
# Create your views here.

# coding=utf-8
# 以下代码用于调用文本检测接口。
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import TextScanRequest
import json
import uuid
import datetime
AccessKey_ID='LTAI5tRQUi1ex9w6LKR6wegt'#os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID']
AccessKey_Secret='ML9sivkp9eTYRTJxRhPzwBmmPEKYTe'#os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
def check_text(text:list):
    pass
    clt = client.AcsClient(AccessKey_ID, AccessKey_Secret)
    region_provider.modify_point('Green', 'cn-shanghai', 'green.cn-shanghai.aliyuncs.com')
    request = TextScanRequest.TextScanRequest()
    request.set_accept_format('JSON')
    tasks=[]
    for i in text:
        task={"dataId": str(uuid.uuid1()),
            "content":i,
            "time":datetime.datetime.now().microsecond
            }
        tasks.append(task)
    request.set_content(bytearray(json.dumps({"tasks": tasks, "scenes": ["antispam"]}), "utf-8"))
    response = clt.do_action_with_exception(request)
    result = json.loads(response)
    if 200 == result["code"]:
        taskResults = result["data"]
        for taskResult in taskResults:
            if (200 == taskResult["code"]):
                sceneResults = taskResult["results"]
                cnt=400204
                for sceneResult in sceneResults:
                    suggestion = sceneResult["suggestion"]
                    if suggestion!='pass':
                        return cnt
                    cnt+=1
            else:
                return 400205
    else:
        return 400205
    return 0

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class createExercise(View):
    # def get(self, request):
    #     return render(request, 'create_exercise.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        print(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        data = json.loads(request.body)

        if data['type'] not in [0, 1, 2, 10]:
            response['success'] = False
            response['errCode'] = 400101
            return JsonResponse(response)
        print(data)
        for i in data['tag']:
            if ProblemGroup.objects.filter(id=i).exists() == False:
                response['success'] = False
                response['errCode'] = 400102
                return JsonResponse(response)

        ans=check_text([data['title'],data['content'],data['option'],data['answer']])
        if ans!=0:
            response['success'] = False
            response['errCode'] = ans
            return JsonResponse(response)

        exercise = Problem.objects.create(
            type=data['type'],
            name=data['title'],
            content=data['content'],
            option=data.get('option', []),
            answer=data['answer'],
            tags=data['tag'],
            author= getUserId(request)
        )
        response['data'] = {'exerciseid': exercise.id}
        return JsonResponse(response)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class updateExercise(View):
    def get(self, request):
        return render(request, 'create_exercise.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        data = json.loads(request.body)
        exerciseid = data['exerciseid']
        data = data['newdata']
        userid = getUserId(request)

        if Problem.objects.filter(id=exerciseid)[0].author != userid:
            response['success'] = False
            response['errCode'] = 400201
            return JsonResponse(response)
        if data['type'] not in [0, 1, 2, 10]:
            response['success'] = False
            response['errCode'] = 400202
            return JsonResponse(response)
        for i in data['tag']:
            if ProblemGroup.objects.filter(id=i).exists() == False:
                response['success'] = False
                response['errCode'] = 400403
                return JsonResponse(response)

        ans=check_text([data['title'],data['content'],data['option'],data['answer']])
        if ans!=0:
            response['success'] = False
            response['errCode'] = ans
            return JsonResponse(response)

        # 更新数据
        exercise = Problem.objects.get(id=exerciseid)
        exercise.type = data['type']
        exercise.name = data['title']
        exercise.content = data['content']
        exercise.option = data.get('option', [])
        exercise.answer = data['answer']
        exercise.tags = data['tag']
        exercise.save()
        response['data'] = {'exerciseid': exercise.id}
        return JsonResponse(response)


class getReachableExercise(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        page = int(request.GET.get('page'))
        problems = set(int)
        userid = getUserId(request)
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
            exercise=getExerciseByID.getExercise(i)
            exercise.remove('isBlock')
            thispage.append(exercise)

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
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
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
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        page = int(request.GET.get('page'))
        type = int(request.GET.get('type'))
        pattern = request.GET.get('pattern')
        problems = set(int)
        userid = getUserId(request)
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
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class OCR(View):
    # def get(self, request):
    #     return render(request,'index.html')
    def post(self, request):
        print('i am here 123')
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        print('i am here too')
        # 获取上传的文件
        uploaded_file = request.FILES.get('file')
        page = request.GET.get('page', 1)

        response=request_template.copy()

        if not uploaded_file:
            response['success']=False
            response['errCode']=400602
            return JsonResponse(response)

        # 保存上传的文件
        file_path = os.path.join('Exercise/ocr', uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        if uploaded_file.name[-4:] == '.pdf':
            try:
                pdf_document = fitz.open(file_path)
                pdfpage = pdf_document.load_page(page)
                text = pdfpage.get_text().split()
                os.remove(file_path)  # 处理完毕后删除文件
            except Exception as e:
                response['success'] = False
                response['errCode'] = 400602
                return JsonResponse(response)
            response['data'] = {'text': text}
            return JsonResponse(response)

        # 打开图像并进行OCR识别
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang="chi_sim+eng")
            os.remove(file_path)  # 处理完毕后删除文件
        except Exception as e:
            response['success']=False
            response['errCode']=400602
            return JsonResponse(response)

        # 返回OCR结果
        response['data'] = {'text': text}
        return JsonResponse(response)