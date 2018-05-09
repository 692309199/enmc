from django.shortcuts import render


from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic.base import View

from apps.equipments.models import Equipment


class SearchEquipment(object):
    def ip(ip):
        try:
            equipment = Equipment.objects.get(ip=ip)
        except:
            equipment = Equipment()
        return equipment


class SearchApplication(object):
    pass

