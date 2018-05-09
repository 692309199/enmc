# -*- coding: utf-8 -*-
import hashlib,time
from datetime import datetime

from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.core import serializers

from .models import Country, Room, Cabinet, Service, EquipmentType, Equipment, Status
from .forms import CountryDetailForms, RoomDetailForms, CabinetDetailForms, EquipmentDetailForms

from pure_pagination import Paginator, PageNotAnInteger


class EquipmentGetDataView(View):
    def get(self, request):
        rooms = Room.objects.all()
        cabinets = Cabinet.objects.all()

        country = request.GET.get('country', '')
        if country != '':
            rooms = rooms.filter(country_id=country)
            data = serializers.serialize('json', rooms)

        room = request.GET.get('room', '')
        if room != '':
            cabinets = cabinets.filter(room_id=room)
            data = serializers.serialize('json', cabinets)

        return HttpResponse(data, content_type='application/json')


class ListView(View):
    def get(self, request):
        countrys = Country.objects.all()
        rooms = Room.objects.all()
        cabinets = Cabinet.objects.all()
        equipment_types = EquipmentType.objects.all()
        statuses = Status.objects.all()
        all_equipments = Equipment.objects.all()

        # 根据地区筛选
        country_id = request.GET.get('country', '')
        if country_id:
            all_equipments = all_equipments.filter(country_id=country_id)
            rooms = rooms.filter(country_id=country_id)
            cabinets = cabinets.filter(country_id=country_id)

        # 根据机房筛选
        room_id = request.GET.get('room', '')
        if room_id:
            all_equipments = all_equipments.filter(room_id=room_id)
            cabinets = cabinets.filter(room_id=room_id)

        # 根据机柜筛选
        cabinet_id = request.GET.get('cabinet', '')
        if cabinet_id:
            all_equipments = all_equipments.filter(cabinet_id=cabinet_id)

        # 根据设备类型筛选
        equipment_type_id = request.GET.get('type', '')
        if equipment_type_id:
            all_equipments = all_equipments.filter(equipment_type_id=equipment_type_id)

        # 根据设备状态筛选
        status_id = request.GET.get('status', '')
        if status_id:
            all_equipments = all_equipments.filter(status_id=status_id)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'ip':
                all_equipments = all_equipments.order_by('-ip')
            elif sort == 'hostname':
                all_equipments = all_equipments.order_by('-hostname')
            elif sort == 'cpu':
                all_equipments = all_equipments.order_by('-cpu')
            elif sort == 'memory':
                all_equipments = all_equipments.order_by('-memory')
            elif sort == 'disk':
                all_equipments = all_equipments.order_by('-disk')
            elif sort == 'port':
                all_equipments = all_equipments.order_by('-ssh_port')
            elif sort == 'type':
                all_equipments = all_equipments.order_by('-equipment_type')

        equipment_num = all_equipments.count()

        # 设备信息分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_equipments, 10, request=request)

        equipments = p.page(page)
        return render(request, 'equipments_list.html', {'all_equipments': all_equipments,
                                                        'equipments': equipments,
                                                        'countrys': countrys,
                                                        'rooms': rooms,
                                                        'cabinets': cabinets,
                                                        'equipment_types': equipment_types,
                                                        'statuses': statuses,
                                                        'equipment_num': equipment_num,
                                                        'country_id': country_id,
                                                        'room_id': room_id,
                                                        'cabinet_id': cabinet_id,
                                                        'equipment_type_id': equipment_type_id,
                                                        'status_id': status_id,
                                                        'sort': sort})


class EquipmentDetailView(View):
    def get(self, request):
        equipmentid = request.GET.get('equipmentid', '')
        todo = request.GET.get('todo', 'detail')

        # 编辑现有的设备
        if equipmentid != '' and todo == 'detail':
            try:
                equipment = Equipment.objects.get(equipmentid=equipmentid)
            except Exception as e:
                return HttpResponseRedirect("/equipments/")
            equipment_types = EquipmentType.objects.all()
            statuses = Status.objects.all()
            services = Service.objects.filter(equipment_id=equipmentid)

            return render(request, 'equipments_detail.html', {'equipment': equipment,
                                                              'equipment_types': equipment_types,
                                                              'statuses': statuses,
                                                              'services': services,
                                                              'todo': todo})

        # 克隆设备
        elif equipmentid != '' and todo == 'clone':
            try:
                equipment = Equipment.objects.get(equipmentid=equipmentid)
            except Exception as e:
                return HttpResponseRedirect("/equipments/")
            equipment_types = EquipmentType.objects.all()
            statuses = Status.objects.all()
            md5 = hashlib.md5(str(time.time()).encode("utf-8"))
            new_equipmentid = 'E' + md5.hexdigest()[0:17]
            equipment.equipmentid = new_equipmentid
            equipment.sn = None
            equipment.ip = None
            equipment.remark = None

            return render(request, 'equipments_detail.html', {'equipment': equipment,
                                                              'equipment_types': equipment_types,
                                                              'statuses': statuses,
                                                              'todo': todo})

        # 添加新设备
        elif equipmentid == '' and todo == 'add':
            country = request.GET.get('country', '')
            room = request.GET.get('room', '')
            cabinet = request.GET.get('cabinet', '')
            if country == '' or room == '' or cabinet == '':
                return HttpResponseRedirect("/equipments/")

            equipment = Equipment()
            equipment.country_id = country
            equipment.room_id = room
            equipment.cabinet_id = cabinet

            equipment_types = EquipmentType.objects.all()
            statuses = Status.objects.all()
            md5 = hashlib.md5(str(time.time()).encode("utf-8"))
            new_equipmentid = 'E' + md5.hexdigest()[0:17]
            equipment.equipmentid = new_equipmentid

            return render(request, 'equipments_detail.html', {'equipment': equipment,
                                                              'equipment_types': equipment_types,
                                                              'statuses': statuses,
                                                              'todo': todo})

        else:
            return HttpResponseRedirect("/equipments/")


    def post(self, request):
        equipmentid = request.POST.get('equipmentid', '')
        print(request.POST.get('remark', ''))

        todo = request.POST.get('todo', '')

        if todo == 'detail':
            try:
                equipment = Equipment.objects.get(equipmentid=equipmentid)
            except Exception as e:
                return HttpResponseRedirect("/equipments/")

            equipment_detail_form = EquipmentDetailForms(request.POST, instance=equipment)
            if equipment_detail_form.is_valid() and equipmentid:
                addtime = Equipment.objects.get(equipmentid=equipmentid).addtime
                equipment = equipment_detail_form.save(commit=False)
                equipment.equipmentid = equipmentid
                equipment.addtime = addtime
                equipment.updatetime = datetime.now()
                equipment.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                msg = ''
                for i in equipment_detail_form.errors:
                    m = equipment_detail_form.errors.get(i)
                    msg = msg + i+ ': ' + m + '\\n'

                return HttpResponse('{"status":"fail", "msg":"' + msg + '"}', content_type='application/json')

        elif todo == 'clone' or todo == 'add':
            equipment = Equipment()
            equipment_detail_form = EquipmentDetailForms(request.POST, instance=equipment)
            if equipment_detail_form.is_valid() and equipmentid:
                equipment = equipment_detail_form.save(commit=False)
                equipment.equipmentid = equipmentid
                equipment.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                msg = ''
                for i in equipment_detail_form.errors:
                    m = equipment_detail_form.errors.get(i)
                    msg = msg + i + ': ' + m + '\\n'

                return HttpResponse('{"status":"fail", "msg":"' + msg + '"}', content_type='application/json')
        else:
            return HttpResponseRedirect("/equipments/")



class EquipmentDeleteView(View):
    def post(self, request):
        equipmentid = request.POST.get('equipmentid', '')
        if equipmentid != '':
            services = Service.objects.filter(equipment_id=equipmentid)
            if not services:
                try:
                    equipment = Equipment.objects.get(equipmentid=equipmentid)
                    equipment.delete()
                    return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
                except Exception as e:
                    return HttpResponse('{"status":"fail", "msg":"请求错误"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"请先删除服务"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"请求错误"}', content_type='application/json')


class ServiceDetailView(View):
    def get(self, request):
        equipmentid = request.GET.get('equipmentid', '')
        serviceid = request.GET.get('serviceid', '')
        protocols = ['tcp', 'udp']

        if equipmentid != '':
            try:
                equipment = Equipment.objects.get(equipmentid=equipmentid)
            except Exception as e:
                return HttpResponseRedirect("/equipments/")
        if serviceid != '':
            try:
                service = Service.objects.get(serviceid=serviceid)
            except Exception as e:
                return HttpResponseRedirect("/equipments/")
        else:
            service = Service()

        return render(request, 'service_detail.html', {'equipmentid': equipmentid,
                                                       'serviceid': serviceid,
                                                        'service': service,
                                                       'protocols':protocols})

    def post(self, request):
        serviceid = request.POST.get('serviceid', '')
        equipment_id = request.POST.get('equipmentid', '')
        name = request.POST.get('name', '')
        install = request.POST.get('install', '')
        config = request.POST.get('config', '')
        start = request.POST.get('start', '')
        version = request.POST.get('version', '')
        port = request.POST.get('port', '')
        protocol = request.POST.get('protocol', '')
        user = request.POST.get('user', '')
        password = request.POST.get('password', 'None')
        remark = request.POST.get('remark', '')

        # 判断要添加到的设备是否存在
        try:
            equipment = Equipment.objects.get(equipmentid=equipment_id)
        except Exception as e:
            return HttpResponseRedirect("/equipments/")

        # 判断服务ID是否存在
        if serviceid == '':
            try:
                serviceid = Service.objects.all().last().serviceid[1:4]
            except Exception as e:
                serviceid = 0
            serviceid = int(serviceid) + 1
            serviceid = 'S' + str(serviceid)
            service = Service()
        else:
            try:
                service = Service.objects.get(serviceid=serviceid)
            except Exception as e:
                return HttpResponseRedirect("/equipments/")

        service.serviceid = serviceid
        service.equipment_id = equipment_id
        service.name = name
        service.install = install
        service.config = config
        service.start = start
        service.version = version
        service.port = port
        service.protocol = protocol
        service.user = user
        service.password = make_password(password)
        service.remark = remark
        service.save()
        return HttpResponseRedirect("/equipments/equipment_detail/?equipmentid=" + equipment_id)


class ServiceDeleteView(View):
    def get(self, request):
        serviceid = request.GET.get('serviceid', '')
        equipment_id = request.GET.get('equipmentid', '')

        # 判断要添加到的设备是否存在
        try:
            equipment = Equipment.objects.get(equipmentid=equipment_id)
        except Exception as e:
            return HttpResponseRedirect("/equipments/")

        # 判断服务是否存在
        try:
            service = Service.objects.get(serviceid=serviceid)
        except Exception as e:
            return HttpResponseRedirect("/equipments/")

        service.delete()
        return HttpResponseRedirect("/equipments/equipment_detail/?equipmentid=" + equipment_id)


# 编辑地区
class CountryDetailView(View):
    def post(self, request):
        countryid = request.POST.get('countryid', '')

        try:
            country = Country.objects.get(countryid=countryid)
        except Exception as e:
            country = Country(countryid=countryid)

        country_detail_form = CountryDetailForms(request.POST, instance=country)
        if country_detail_form.is_valid():
            country_detail_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class CountryDeleteView(View):
    def post(self, request):
        countryid = request.POST.get('countryid', '')

        try:
            country = Country.objects.get(countryid=countryid)
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"没有找到你要删除的地区"}', content_type='application/json')

        rooms = Room.objects.filter(country_id=countryid)
        if not rooms:
            country.delete()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"请先删除这个地区的所有机房"}', content_type='application/json')


# 编辑机房
class RoomDetailView(View):
    def get(self, request):
        countryid = request.GET.get('countryid', '')

        if countryid == '':
            return HttpResponseRedirect("index")

        rooms = Room.objects.filter(country_id=countryid)
        cabinets = Cabinet.objects.all()
        md5 = hashlib.md5(str(time.time()).encode("utf-8"))
        new_roomid = 'R' + md5.hexdigest()[0:7]
        return render(request, 'rooms_detail.html', {'rooms': rooms,
                                                     'cabinets': cabinets,
                                                     'new_roomid': new_roomid,
                                                     'countryid': countryid})

    def post(self, request):
        roomid = request.POST.get('roomid', '')

        try:
            room = Room.objects.get(roomid=roomid)
        except Exception as e:
            room = Room(roomid=roomid)

        room_detail_form = RoomDetailForms(request.POST, instance=room)
        if room_detail_form.is_valid():
            room_detail_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class RoomDeleteView(View):
    def post(self, request):
        roomid = request.POST.get('roomid', '')

        try:
            room = Room.objects.get(roomid=roomid)
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"没有找到你要删除的机房"}', content_type='application/json')

        cabinets = Cabinet.objects.filter(room_id=roomid)
        if not cabinets:
            room.delete()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"请先删除这个机房的所有机柜"}', content_type='application/json')


# 编辑机柜
class CabinetDetailView(View):
    def get(self, request):
        roomid = request.GET.get('roomid', '')
        countryid = request.GET.get('countryid', '')

        if roomid == '' or countryid == '':
            return HttpResponseRedirect("index")

        cabinets = Cabinet.objects.filter(room_id=roomid)
        md5 = hashlib.md5(str(time.time()).encode("utf-8"))
        new_cabinetid = 'J' + md5.hexdigest()[0:11]
        return render(request, 'cabinets_detail.html', {'cabinets': cabinets,
                                                        'new_cabinetid': new_cabinetid,
                                                        'countryid': countryid,
                                                        'roomid': roomid})

    def post(self, request):
        cabinetid = request.POST.get('cabinetid', '')

        try:
            cabinet = Cabinet.objects.get(cabinetid=cabinetid)
        except Exception as e:
            cabinet = Cabinet(cabinetid=cabinetid)

        cabinet_detail_form = CabinetDetailForms(request.POST, instance=cabinet)
        if cabinet_detail_form.is_valid():
            cabinet_detail_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class CabinetDeleteView(View):
    def post(self, request):
        cabinetid = request.POST.get('cabinetid', '')

        try:
            cabinet = Cabinet.objects.get(cabinetid=cabinetid)
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"没有找到你要删除的机柜"}', content_type='application/json')

        equipments = Equipment.objects.filter(cabinet_id=cabinetid)
        if not equipments:
            cabinet.delete()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"请先删除这个机柜的所有设备"}', content_type='application/json')


def index(request):
    countrys = Country.objects.all()
    rooms = Room.objects.all()
    md5 = hashlib.md5(str(time.time()).encode("utf-8"))
    new_countryid = 'G' + md5.hexdigest()[0:3]
    return render(request, 'index.html', {'countrys': countrys,
                                          'rooms': rooms,
                                          'new_countryid': new_countryid})