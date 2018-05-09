# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *

app_name = '[search]'
urlpatterns = [
    # 查询Mother
    # url(r'^search_mother/$', SearchMotherView.as_view(), name='search_mother'),
]
