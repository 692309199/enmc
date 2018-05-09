# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.users.views import UserListView, UserDetailView, UserDeleteView, LoginView, ResetPwdView, user_logout

app_name = '[users]'
urlpatterns = [
    url(r'^$', UserListView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^reset_pwd/$', ResetPwdView.as_view(), name='reset_pwd'),

    # 用户管理
    url(r'^user_detail/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^user_delete/$', UserDeleteView.as_view(), name='user_delete'),
]