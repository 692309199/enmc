# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    role = models.CharField(max_length=7, choices=(('yunwei', u'运维'), ('yanfa', u'研发'), ('yunying', u'运营')),
                            default='yunwei', verbose_name=u'用户角色')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱地址', unique=True)
    mobile = models.CharField(max_length=11, verbose_name=u'手机号码', unique=True)
    avatar = models.ImageField(max_length=100, null=True, blank=True, upload_to=u'avatar/%Y/%m', default=u'avatar/default.png',
                               verbose_name=u'用户头像')

    class Meta:
        verbose_name = u'用户信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username