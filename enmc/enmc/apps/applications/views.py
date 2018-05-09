# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.base import View


class ListView(View):
    def get(self, request):
        return render(request, 'applications_list.html')

    def post(self, request):
        pass