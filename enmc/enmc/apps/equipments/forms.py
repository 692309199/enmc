# -*- coding: utf-8 -*-
from django import forms

from apps.search.views import SearchEquipment
from apps.equipments.models import Country, Room, Cabinet, Equipment


class ServiceDetailForms(forms.ModelForm):

    class Meta:
        fields = ['name']


class EquipmentDetailForms(forms.ModelForm):
    def clean_ip(self):
        equipment_type = self.cleaned_data.get('equipment_type')
        mother = self.cleaned_data.get('mother')
        ip = self.cleaned_data.get('ip')
        cabinet = self.cleaned_data.get('cabinet').pk

        if equipment_type.name == 'VM' and mother != '':
            equipment = SearchEquipment.ip(mother)
            if equipment.equipment_type_id != '3':
                raise forms.ValidationError(mother + '不存在或者不是ALONE')
            if equipment.cabinet_id != cabinet:
                raise forms.ValidationError(mother + '与' + ip + '不再同一个机柜')

        if mother == '' and equipment_type.name == 'VM':
            raise forms.ValidationError('你选择的设备类型为VM，请填写宿主机IP地址。')

        if mother != '' and equipment_type.name != 'VM':
            raise forms.ValidationError('请设置设备类型为VM。')

        return ip

    class Meta:
        model = Equipment
        fields = '__all__'
        exclude = ['addtime', 'updatetime']


class CountryDetailForms(forms.ModelForm):

    class Meta:
        model = Country
        fields = '__all__'


class RoomDetailForms(forms.ModelForm):

    class Meta:
        model = Room
        fields = '__all__'


class CabinetDetailForms(forms.ModelForm):

    class Meta:
        model = Cabinet
        fields = '__all__'
