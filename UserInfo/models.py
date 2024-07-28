from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Create your models here.

class UserInfo(models.Model):
    #内置id
    #{subject}-chapter{chapternum}
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    studentId = models.CharField(max_length=32,default=str)    #学号
    groups = models.JSONField(default=[1]) #用户组id，形式为列表
    problems = models.JSONField(default=list)   #[num],自己创建的题目
    problemGroups = models.JSONField(default=list)  #[num],自己创建的题目组
    head = models.ImageField(upload_to='static/img/', default='static/img/default.jpg')  #头像
    log = models.JSONField(default=list)    #日志[(timestamp,str),...]str->'register','login','logout'
    problemlog = models.JSONField(default=list)    #错题日志,[(timestamp,题目id,true/false(正误))]
    token = models.CharField(max_length=512)


@receiver(post_migrate)
def add_initial_data(sender, **kwargs):
    if sender.name == 'UserInfo':  # 确保只在特定应用中运行
        UserInfo.objects.get_or_create(name='系统',password='000000')
