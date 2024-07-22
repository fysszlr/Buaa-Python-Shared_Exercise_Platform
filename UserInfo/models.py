from django.db import models

# Create your models here.

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
    log = models.JSONField(default=list)    #日志[(timestamp,str),...]str->'register','login','logout'
    problemlog = models.JSONField(default=list)    #错题日志,[(timestamp,题目id,true/false(正误))]
    token = models.CharField(max_length=512)
