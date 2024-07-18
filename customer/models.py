from django.db import models

# Create your models here.

#用户
class UserInfo(models.Model):
    #内置id
    #{subject}-chapter{chapternum}
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    studentId = models.CharField(max_length=32,null=True,blank=True)    #学号
    groups = models.JSONField(default=[0]) #用户组id，形式为列表
    problems = models.JSONField(default=list)   #[num],自己创建的题目
    head = models.ImageField(upload_to='static/img/', default='static/img/default.png')  #头像
    log = models.JSONField(default=list)    #日志
    problemlog = models.JSONField(default=list)    #[(时间,题目id,正误)],错题日志
    token = models.CharField(max_length=512)


#管理员    
class AdminInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)

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
    name = models.CharField(max_length=32)
    tags = models.JSONField(default=list)  #标签
    content = models.TextField()    #题面
    answer = models.TextField() #答案
    author = models.IntegerField()  #创建者，用户id

#题目组
class ProblemGroup(models.Model):
    #内置id
    name = models.CharField(max_length=32)
    description = models.TextField()    #描述
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

# python manage.py makemigrations
# python manage.py migrate