# -*- coding: utf-8 -*-
from re import compile

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponseRedirect

EXEMPT_URLS=[compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings,'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect('users/login/')