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
AccessKey_ID=''#os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID']
AccessKey_Secret=''#os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
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
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        data = json.loads(request.body)

        if data['type'] not in [0, 1, 2, 10]:
            response['success'] = False
            response['errCode'] = 400101
            return JsonResponse(response)
        for i in data['tag']:
            if ProblemGroup.objects.filter(id=int(i)).exists() == False:
                response['success'] = False
                response['errCode'] = 400102
                return JsonResponse(response)
        try:
            ans=check_text([data['title'],data['content'],data['option'],data['answer']])
        except:
            ans=0
        if ans!=0:
            response['success'] = False
            response['errCode'] = ans
            return JsonResponse(response)

        exercise = Problem.objects.create(
            type=int(data['type']),
            name=data['title'],
            content=data['content'],
            option=data.get('option', []),
            answer=data['answer'],
            tags=data['tag'],
            creator= getUserId(request)
        )
        for tagid in exercise.tags:
            tag=ProblemGroup.objects.filter(id=tagid)[0]
            tag.problems.append(exercise.id)
            tag.save()
        user = _
        user.problems.append(exercise.id)
        user.save()
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
        exerciseid = int(data['exerciseid'])
        data = data['newdata']
        userid = getUserId(request)

        if Problem.objects.filter(id=exerciseid)[0].creator != userid:
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
        exercise = Problem.objects.filter(id=exerciseid)[0]
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
        problems = set()
        userid = getUserId(request)
        # problems = cache.get(userid)
        # if not problems:
        # 从大到小排序
        problems = list(getReachableExercise.getReachableExercise(userid))
        problems = sorted(problems, reverse=True)
        # cache.set(userid, problems, 60*15)#缓存15分钟
        pages = (problems.__len__() + 19) // 20
        if page > pages:
            problems = []
        else:
            problems = problems[20 * (page - 1):min(20 * page, problems.__len__())]
        thispage = []
        for i in problems:
            exercise=getExerciseByID.getExercise(i)
            exercise.pop('isBlock')
            thispage.append(exercise)
            newtags=[]
            creator = UserInfo.objects.get(name=exercise['createusername'])
            for tag in exercise['tag']:
                if int(tag['tagid']) in creator.problemGroups:
                    newtags.append(tag)
            exercise['tag']=newtags


        response = request_template.copy()
        response['data'] = {'thispage': thispage, 'pages': pages}
        return JsonResponse(response)

    def getReachableExercise(userid):
        problems = set()
        # 所有共享群组
        for userGroup in UserInfo.objects.filter(id=userid)[0].groups:
            for problemGroup in UserGroup.objects.filter(id=userGroup)[0].problemGroups:
                problems = problems.union(set(ProblemGroup.objects.filter(id=problemGroup)[0].problems))
        # 自己创建的题目
        problems = problems.union(set(UserInfo.objects.filter(id=userid)[0].problems))
        # 去除被封禁的题目
        for bannedProblem in BannedProblem.objects.all():
            problems.discard(bannedProblem.problem_id)
        return problems


class getExerciseByID(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        exerciseid = int(request.GET.get('exerciseid'))
        problem = Problem.objects.filter(id=exerciseid)
        if not problem.exists():
            return JsonResponse(json_response(False, 400401, {}))
        data = getExerciseByID.getExercise(exerciseid)
        response = request_template.copy()
        #response['isBlock'] = data.pop('isBlock')
        print(data)
        isBlock=data['isBlock']
        data.pop('isBlock')
        response['data'] = {'data':data,'isBlock':isBlock}  # 或者data中包含data和isblock？
        return JsonResponse(response)

    def getExercise(exerciseid):
        if Problem.objects.filter(id=exerciseid).exists() == False:
            return {}
        problem = Problem.objects.filter(id=exerciseid)[0]
        exercise = {}
        exercise['exerciseid'] = problem.id
        exercise['createusername'] = UserInfo.objects.filter(id=problem.creator)[0].name
        exercise['type'] = problem.type
        exercise['title'] = problem.name
        exercise['content'] = problem.content
        exercise['option'] = problem.option
        exercise['answer'] = problem.answer
        tag = []
        for j in problem.tags:
            tag.append({'tagid': j, 'tagname': ProblemGroup.objects.filter(id=j)[0].name})
        exercise['tag'] = tag
        if BannedProblem.objects.filter(problem_id=problem.id).exists():
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
        type = request.GET.get('type')
        pattern = request.GET.get('pattern')
        problems = set()
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
                # if pattern in exercise['tag']['tagname']:
                for tag_dict in exercise['tag']:
                    if pattern in tag_dict['tagname']:
                        thispage.append(exercise)
        pages = (thispage.__len__() + 19) // 20
        if page > pages:
            thispage = []
        else:
            thispage = thispage[20 * (page - 1):min(20 * page, thispage.__len__())]

        response = request_template.copy()
        response['data'] = {'thispage': thispage, 'pages': pages}
        return JsonResponse(response)
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class OCR(View):
    # def get(self, request):
    #     return render(request,'index.html')
    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        # 获取上传的文件
        uploaded_file = request.FILES.get('file')
        page = int(request.POST.get('page', 1))

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
                pdfpage = pdf_document.load_page(page-1)
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
        
class GetCommentByID(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        exerciseid = int(request.GET.get('exerciseid'))
        response=request_template.copy()
        comment = []
        for com in Comment.objects.all():
            if com.problem_id != exerciseid:
                continue
            user = UserInfo.objects.get(id = com.create_user_id)
            now = {
                'createusername': user.name,
                'createavatarurl': request.build_absolute_uri(user.head.url) if user.head else "",
                'time': datetime.datetime.fromtimestamp(float(com.time) + 28800).strftime('%Y-%m-%d %H:%M:%S'),
                'content': com.content,
            }
            comment.append(now)
        tmp = []
        for it in range(len(comment)-1 ,-1, -1):
            tmp.append(comment[it])
        comment = tmp
        response['data'] = {'comment' : comment}
        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class AddComment(View):
    def post(self, request):
        token = request.GET.get('token')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        exerciseid = int(request.POST.get('exerciseid'))
        comment = request.POST.get('comment')
        response = request_template.copy()
        
        flag = False
        for exer in Problem.objects.all():
            if exerciseid == exer.id:
                flag = True
                break
        
        if not flag:
            response['success']=False
            response['errCose'] = 400801
            return JsonResponse(response)
                
        Comment.objects.create(problem_id = exerciseid, create_user_id = user.id, time = datetime.datetime.now().timestamp(), content = comment)
        return JsonResponse(response)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        