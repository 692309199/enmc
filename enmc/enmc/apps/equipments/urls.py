# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.equipments.views import *

app_name = '[equipments]'
urlpatterns = [
    url(r'^$', ListView.as_view(), name='index'),

    # 设备管理
    url(r'^equipment_detail/$', EquipmentDetailView.as_view(), name='equipment_detail'),
    url(r'^equipment_delete/$', EquipmentDeleteView.as_view(), name='equipment_delete'),

    # 编辑服务
    url(r'^service_detail/$', ServiceDetailView.as_view(), name='service_detail'),
    url(r'^service_delete/$', ServiceDeleteView.as_view(), name='service_delete'),

    # 编辑地区
    url(r'^country_detail/$', CountryDetailView.as_view(), name='country_detail'),
    url(r'^country_delete/$', CountryDeleteView.as_view(), name='country_delete'),
    # 编辑机房
    url(r'^room_detail/$', RoomDetailView.as_view(), name='room_detail'),
    url(r'^room_delete/$', RoomDeleteView.as_view(), name='room_delete'),
    # 编辑机柜
    url(r'^cabinet_detail/$', CabinetDetailView.as_view(), name='cabinet_detail'),
    url(r'^cabinet_delete/$', CabinetDeleteView.as_view(), name='cabinet_delete'),

    # 动态获取地区、机房、机柜信息
    url(r'^equipment_getdata/$', EquipmentGetDataView.as_view(), name='equipment_getdata'),
]
