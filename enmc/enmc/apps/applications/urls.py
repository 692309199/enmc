# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.applications.views import ListView

app_name = '[applications]'
urlpatterns = [
    url(r'^$', ListView.as_view(), name='index'),
]