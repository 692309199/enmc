# -*- coding: utf-8 -*-

import xadmin
from xadmin import views

from .models import UserProfile


class UserProfileAdmin(object):
    list_display = ('username', 'role', 'is_active', 'is_superuser', 'email', 'mobile', 'is_staff')
    list_filter = ('role', 'is_active', 'is_superuser', 'is_staff')
    search_fields = ('username', 'role', 'is_active', 'is_superuser', 'email', 'mobile')


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobaSettings(object):
    site_title = u'网管系统'
    site_footer = u'运维部'
    menu_style = 'accordion'


xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobaSettings)