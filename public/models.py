from django.db import models
from django.contrib.auth.models import User


class Functions(models.Model):
    funcName     = models.CharField(max_length=80, null=True,blank=True)
    nickName     = models.CharField(max_length=80, null=True,blank=True)
    playbook     = models.CharField(max_length=80, unique=True, null=True, blank=False)

    class Meta:
        verbose_name_plural = '可执行任务（playbook）'

    def __str__(self):
        return self.playbook


class HostsLists(models.Model):
    hostname     = models.CharField(max_length=80, null=True, blank=True)
    ip           = models.CharField(max_length=80, unique=True)
    ansible_user = models.CharField(max_length=80, default='root')
    ansible_pass = models.CharField(max_length=80, blank=True, null=True, )
    ansilbe_key  = models.CharField(max_length=80, default='files/id_rsa')

    class Meta:
        verbose_name_plural = '主机列表'
    def __str__(self):
        return self.hostname


class ProjectGroups(models.Model):
    groupName    = models.CharField(max_length=80,unique=True)
    nickName     = models.CharField(max_length=80,unique=True, null=True,blank=True)
    remark       = models.TextField(blank=True)
    hostList     = models.ManyToManyField(HostsLists)
    possessFuncs = models.ManyToManyField(Functions, blank=True)

    class Meta:
        verbose_name_plural = '项目组'

    def __str__(self):
        return self.groupName


class AnsibleTasks(models.Model):
    AnsibleID   = models.CharField(max_length=80,unique=True, null=True,blank=True)
    CeleryID    = models.CharField(max_length=80,unique=True, null=True,blank=True)
    TaskUser    =  models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    GroupName   = models.CharField(max_length=80, null=True, blank=True)
    playbook    = models.CharField(max_length=80, null=True, blank=True)
    ExtraVars   = models.TextField(blank=True, null=True)
    AnsibleResult = models.TextField(blank=True)
    CeleryResult  = models.TextField(blank=True)
    Label         = models.CharField(max_length=80, null=True, blank=True)
    CreateTime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Ansible 任务'

    def __str__(self):
        return self.AnsibleID


class ExtraVars(models.Model):
    Name        = models.CharField(max_length=80,unique=True, null=True,blank=True)
    Content     = models.TextField(blank=True)
    Remark      = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = '额外参数'

    def __str__(self):
        return self.Name