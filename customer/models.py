from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Create your models here.

#TODO:使用redis,使用token验证
#用户
class UserInfo(models.Model):
    #内置id
    #{subject}-chapter{chapternum}
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    studentId = models.CharField(max_length=32,default=str)    #学号
    groups = models.JSONField(default=list) #用户组id，形式为列表
    problems = models.JSONField(default=list)   #[num],自己创建的题目
    problemGroups = models.JSONField(default=list)  #[num],自己创建的题目组
    head = models.ImageField(upload_to='static/img/', default='static/img/default.png')  #头像
    log = models.JSONField(default=list)    #日志
    problemlog = models.JSONField(default=list)    #[(时间,题目id,正误)],错题日志
    token = models.CharField(max_length=512)


#管理员    
class AdminInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=512)

#用户组
class UserGroup(models.Model):
    #内置id
    name = models.CharField(max_length=32)
    creator = models.IntegerField() #创建者，用户id
    users = models.JSONField(default=list)    #[id],用户id
    problems = models.JSONField(default=list) #[num],题目组id

#题目
class Problem(models.Model):
    #内置id
    TYPE_CHOICES = [
        (0, '判断题'),
        (1, '单选题'),
        (2, '多选题'),
        (10, '填空题'),
    ]
    type = models.IntegerField(choices=TYPE_CHOICES)    #题目类型
    name = models.CharField(max_length=32)
    tags = models.JSONField(default=list)  #标签
    content = models.TextField()    #题面
    option = models.JSONField(blank=True, null=True)    #选项
    answer = models.TextField() #答案
    author = models.IntegerField()  #创建者，用户id

#题目组
class ProblemGroup(models.Model):
    #内置id
    name = models.CharField(max_length=32)
    description = models.TextField(default=str)    #描述
    creator = models.IntegerField() #创建者，用户id
    problems = models.JSONField(default=list)   #[num],题目id

#封禁用户
class BannedUser(models.Model):
    user = models.IntegerField()    #[id],用户id
    #time = models.DateTimeField()  #封禁时间

#封禁题目
class BannedProblem(models.Model):
    problem = models.IntegerField() #[id],用户组id
    #time = models.DateTimeField()  #封禁时间

@receiver(post_migrate)
def add_initial_data(sender, **kwargs):
    # 创建一个管理员账户
    if sender.name == 'customer':  # 确保只在特定应用中运行
        AdminInfo.objects.get_or_create(name='root', password='000000')
        ProblemGroup.objects.get_or_create(name='公共题目组', description='公共题目组', creator=1, problems=[])

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver