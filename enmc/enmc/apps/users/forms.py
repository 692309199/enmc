# -*- coding: utf-8 -*-
from django import forms


class LoginForms(forms.Form):
    username = forms.CharField(required=True, max_length=20)
    password = forms.CharField(required=True, min_length=6, max_length=20)


class ResetPwdForms(forms.Form):
    password = forms.CharField(required=True, min_length=6, max_length=20)
    password2 = forms.CharField(required=True, min_length=6, max_length=20)


class UserDetailForms(forms.Form):
    username = forms.CharField(required=True, max_length=20)
    # password = forms.CharField(required=True, min_length=6, max_length=20)
    # password2 = forms.CharField(required=True, min_length=6, max_length=20)
    mobile = forms.CharField(max_length=11)
    email = forms.EmailField(max_length=50)
    role = forms.CharField(max_length=7)
