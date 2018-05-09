# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime


class Directory(models.Model):
    # 主键，这里目前分为两个分支，0001是资源的分支，0002是应用的分支。如果以后需要扩展可以使用0003
    dirid = models.CharField(primary_key=True, max_length=8, verbose_name=u'主目录ID')
    parentid = models.CharField(max_length=8, verbose_name=u'父ID')
    name = models.CharField(max_length=255, verbose_name=u'目录名称')
    tree = models.CharField(max_length=255, verbose_name=u'树串ID')
    # 存储json格式的数据，存储可用的角色，例如应用管理中的"web","db","cache","proxy","nat"等
    # 设备管理中的"switch","host","alon","vm"等
    roleset = models.CharField(max_length=255, verbose_name=u'角色集')
    addtime = models.DateTimeField(default=datetime.now, verbose_name=u'创建时间')
    updatetime = models.DateTimeField(default=datetime.now, verbose_name=u'更新时间')
    info = models.TextField(verbose_name=u'说明信息')
    log = models.TextField(verbose_name=u'日志信息')

    class Meta:
        verbose_name = u'目录信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


