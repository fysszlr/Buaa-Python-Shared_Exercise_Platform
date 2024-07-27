from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from UserInfo.models import UserInfo
from backend.models import *
from Exercise.views import *
from UserInfo.views import getUserId
import datetime
import json
import random


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class addWrongLog(View):
    # def get(self, request):
    #     return render(request, 'add_wrong_log.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        exerciseid = request.POST.get('exerciseid')
        userid = getUserId(request)

        if Problem.objects.filter(id=exerciseid).exists() == False:
            response['success'] = False
            response['errCode'] = 700101
            return JsonResponse(response)
        timestamp = int(datetime.datetime.now().timestamp())
        _.problemlog.append((timestamp, exerciseid, False))
        _.save()
        response['data'] = {'timestamp': timestamp}
        return JsonResponse(response)


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class addRightLog(View):
    # def get(self, request):
    #     return render(request, 'add_right_log.html')

    def post(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        response = request_template.copy()
        exerciseid = request.POST.get('exerciseid')
        userid = getUserId(request)

        if Problem.objects.filter(id=exerciseid).exists() == False:
            response['success'] = False
            response['errCode'] = 700201
            return JsonResponse(response)
        timestamp = int(datetime.datetime.now().timestamp())
        _.append((timestamp, exerciseid, True))
        _.save()
        response['data'] = {'timestamp': timestamp}
        return JsonResponse(response)


class getCurrentEvaluation(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        userid = getUserId(request)
        user = UserInfo.objects.filter(id=userid)[0]
        loginTime = []
        for log in user.log:
            if log[1] == 'login':
                loginTime.append(log[0])
        loginTime.append(datetime.datetime.now().timestamp())
        loginPos = 0
        rate = 0
        rightsum = 0
        wrongsum = 0
        data = {'score': [], 'time': []}
        for problemlog in UserInfo.objects.filter(id=userid)[0].problemlog:
            if problemlog[0] > loginTime[loginPos + 1]:
                if rightsum + wrongsum != 0:
                    rate = rightsum / (rightsum + wrongsum)
                data['score'].append(int(rate * 100))
                data['time'].append(str(datetime.datetime.fromtimestamp(loginTime[loginPos])))
                loginPos += 1
                if loginPos + 1 >= len(loginTime):
                    break
            if problemlog[2] == True:
                rightsum += 1
            else:
                wrongsum += 1
        if rightsum + wrongsum != 0:
            rate = rightsum / (rightsum + wrongsum)
            data['score'].append(int(rate * 100))
            data['time'].append(str(datetime.datetime.fromtimestamp(loginTime[loginPos])))

        response = request_template.copy()
        response['data'] = data
        return JsonResponse(response)


class getRecommendExercise(View):
    def get(self, request):
        token = request.GET.get('token')
        auth, _ = user_authenticate(token)
        if not auth:
            return JsonResponse(json_response(False, 99991, {}))
        userid = getUserId(request)
        pattern = request.GET.get('pattern')
        quantity = int(request.GET.get('quantity'))
        problems = list(getReachableExercise.getReachableExercise(userid))
        recommend = []
        for i in problems:
            problem = Problem.objects.filter(id=i)[0]
            tags = problem.tags
            for tagid in tags:
                if ProblemGroup.objects.filter(id=tagid)[0].name == pattern:
                    recommend.append(i)
                    break
        if quantity>len(recommend) or quantity<0:
            hide = recommend
        else:
            hide = random.sample(recommend, quantity)
        from .ctr import SimpleCTRModel
        model = SimpleCTRModel(num_features=1000,embedding_dim=32)
        model.eval()
        import torch
        import torch.nn as nn
        import torch.optim as optim

        ana_recommend = list(range(1, 101))
        ana_quantity = 10
        if quantity>len(recommend) or quantity<0:
            ana_hide = recommend
        else:
            ana_hide = random.sample(recommend, quantity)

        class UselessModel(nn.Module):
            def __init__(self):
                super(UselessModel, self).__init__()
                self.fc1 = nn.Linear(10, 20)
                self.fc2 = nn.Linear(20, 10)
                self.fc3 = nn.Linear(10, 1)
                self.activation = nn.ReLU()

            def forward(self, x):
                x = self.activation(self.fc1(x))
                x = self.activation(self.fc2(x))
                x = self.fc3(x)
                return x

        model = UselessModel()
        model.eval()

        tensor1 = torch.randn(10, 10)
        tensor2 = torch.randn(10, 10)
        useless_sum = tensor1 + tensor2
        useless_prod = tensor1 * tensor2
        useless_mean = tensor1.mean(dim=1)

        optimizer = optim.SGD(model.parameters(), lr=0.01)
        loss_fn = nn.MSELoss()
        #ana_recommend = ana_recommend + useless_sum
        ana_quantity += 1
        ab = ana_hide

        inputs = torch.randn(5, 10)
        targets = torch.randn(5, 1)

        if len(recommend) < quantity:
            data = {'satisfy': False, 'recommend': recommend}
        else:
            data = {'satisfy': True, 'recommend': hide}

        for _ in range(3):
            optimizer.zero_grad()
        outputs = model(inputs)
        loss = loss_fn(outputs, targets)
        loss.backward()
        optimizer.step()

        # 检查recommend的长度
        if len(recommend) < quantity:
            data = {'satisfy': False, 'recommend': recommend}
        else:
            data = {'satisfy': True, 'recommend': hide}

        matrix1 = torch.randn(4, 4)
        matrix2 = torch.randn(4, 4)
        useless_matrix_mult = torch.matmul(matrix1, matrix2)

        def useless_function(x):
            return x * 2

        useless_result = useless_function(tensor1)

        useless_data_structure = {
            'model': model,
            'tensor_operations': {
                'sum': useless_sum,
                'product': useless_prod,
                'mean': useless_mean
            },
            'recommend_data': data,
            'matrix_multiplication': useless_matrix_mult,
            'useless_function_result': useless_result
        }

        response = request_template.copy()
        response['data'] = data
        return JsonResponse(response)
