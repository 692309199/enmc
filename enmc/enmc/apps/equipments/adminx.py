# -*- coding: utf-8 -*-

import xadmin

from .models import Country, Room, Cabinet, EquipmentType, Equipment, Service, Status


class CountryAdmin(object):
    list_display = ('name', 'countryid')
    list_filter = ('name', 'countryid')
    search_fields = ('name', 'countryid')


class RoomAdmin(object):
    list_display = ('name', 'roomid', 'country', 'roomaddress', 'isp', 'addtime', 'updatetime', 'remark')
    list_filter = ('name', 'roomid', 'country', 'isp')
    search_fields = ('name', 'roomaddress', 'isp', 'remark')


class CabinetAdmin(object):
    list_display = ('name', 'cabinetid', 'room', 'network', 'start_time', 'stop_time', 'addtime', 'updatetime', 'remark')
    list_filter = ('name', 'cabinetid', 'room', 'network')
    search_fields = ('name', 'network', 'remark')


class EquipmentTypeAdmin(object):
    list_display = ('name', 'equipment_typeid')
    list_filter = ('name', 'equipment_typeid')
    search_fields = ('name', 'equipment_typeid')


class EquipmentAdmin(object):
    list_display = ('hostname', 'equipment_type', 'ip', 'ssh_port')
    list_filter = ('hostname', 'equipment_type', 'ip', 'ssh_port')
    search_fields = ('hostname', 'equipment_type', 'ip', 'ssh_port')


class ServiceAdmin(object):
    list_display = ('name', 'port')
    list_filter = ('name', 'port')
    search_fields = ('name', 'port')


class StatusAdmin(object):
    list_display = ('status', 'id')
    list_filter = ('status', 'id')
    search_fields = ('status', 'id')


xadmin.site.register(Country, CountryAdmin)
xadmin.site.register(Room, RoomAdmin)
xadmin.site.register(Cabinet, CabinetAdmin)
xadmin.site.register(EquipmentType, EquipmentTypeAdmin)
xadmin.site.register(Equipment, EquipmentAdmin)
xadmin.site.register(Service, ServiceAdmin)
xadmin.site.register(Status,StatusAdmin)