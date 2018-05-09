# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.directories.views import ListView


app_name = '[directories]'
urlpatterns = [
    url(r'^$', ListView.as_view(), name='index'),
]