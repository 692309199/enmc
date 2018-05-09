# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile
from .forms import LoginForms, ResetPwdForms, UserDetailForms

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class CustomBacken(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(username=username)
            if user.check_password(password):
                if user.is_active:
                    return user
        except Exception as e:
            return None


class UserListView(View):
    def get(self, request):
        all_users = UserProfile.objects.all()

        # 筛选用户类型
        user_role = request.GET.get('role', '')
        if user_role:
            all_users = all_users.filter(role=user_role)

        # 筛选超级用户
        user_super = request.GET.get('super', '')
        if user_super:
            all_users = all_users.filter(is_superuser=int(user_super))

        users_num = all_users.count()

        # 用户信息分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_users, 10, request=request)

        users = p.page(page)

        return render(request, 'users_list.html', {'all_users': all_users,
                                                   'users': users,
                                                   'users_num': users_num,
                                                   'user_role': user_role,
                                                   'user_super': user_super,
                                                   })


class UserDetailView(View):
    def get(self, request):
        user_name = request.GET.get('user', '')
        email = request.GET.get('email', '')
        mobile = request.GET.get('mobile', '')
        role = request.GET.get('role', '')
        if user_name == '':
            return render(request, 'user_detail.html')
        else:
            return render(request, 'user_detail.html',
                          {'user_name': user_name, 'email': email, 'mobile': mobile, 'role': role})

    def post(self, request):
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        pass_word2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        mobile = request.POST.get('mobile', '')
        role = request.POST.get('role', 'yunwei')
        url = request.get_full_path()

        user_detail_form = UserDetailForms(request.POST)
        if UserProfile.objects.filter(username=user_name):
            user = UserProfile.objects.get(username=user_name)
        else:
            # 如果用户不存在
            user = False

        # print(user.values()[0].get('mobile'))
        if user:
            # 假设没有修改
            is_changed = False
            # 判断两次密码是否一致,是否为空
            if pass_word != pass_word2:
                return render(request, 'user_detail.html', {'user_detail_form': user_detail_form, 'msg': '两次密码不一致',
                                                            'user_name': user_name, 'email': email,
                                                            'mobile': mobile, 'role': role})
            elif pass_word == '' or 5 < len(pass_word) < 20:
                user.password = make_password(pass_word)
                is_changed = True
            else:
                return render(request, 'user_detail.html', {'user_detail_form': user_detail_form, 'msg': '密码为6-20位',
                                                            'user_name': user_name, 'email': email,
                                                            'mobile': mobile, 'role': role})

            # 必须要判断一下email地址是否已经注册过了
            if user.email != email:
                if UserProfile.objects.filter(email=email):
                    return render(request, 'user_detail.html', {'user_detail_form': user_detail_form, 'msg': '邮箱地址已存在',
                                                                'user_name': user_name, 'email': email,
                                                                'mobile': mobile, 'role': role})
                else:
                    user.email = email
                    is_changed = True

            # 必须要判断一下手机号是否已经注册过了
            if user.mobile != mobile:
                if UserProfile.objects.filter(mobile=mobile):
                    return render(request, 'user_detail.html', {'user_detail_form': user_detail_form, 'msg': '手机号已存在',
                                                                'user_name': user_name, 'email': email,
                                                                'mobile': mobile, 'role': role})
                else:
                    user.mobile = mobile
                    is_changed = True

            # 必须要判断用户类型
            if user.role != role:
                user.role = role
                is_changed = True

            if is_changed:
                if user_detail_form.is_valid():
                    user.save()
                    return HttpResponseRedirect("/users/")
                else:
                    return render(request, 'user_detail.html', {'user_detail_form': user_detail_form,
                                                                'user_name': user_name, 'email': email,
                                                                'mobile': mobile, 'role': role})
            else:
                return HttpResponseRedirect("/users/")
        else:
            # 必须要判断一下用户是否已经注册过了
            if UserProfile.objects.filter(username=user_name):
                return render(request, 'user_detail.html', {'user_detail_form': user_detail_form, 'msg': '用户已存在',
                                                            'user_name': user_name, 'email': email,
                                                            'mobile': mobile, 'role': role})

            # 判断两次密码是否一致
            if pass_word != pass_word2:
                return render(request, 'user_detail.html', {'user_detail_form': user_detail_form, 'msg': '两次密码不一致',
                                                            'user_name': user_name, 'email': email,
                                                            'mobile': mobile, 'role': role})
            elif 6 > len(pass_word) < 20:
                return render(request, 'user_detail.html', {'user_detail_form': user_detail_form, 'msg': '密码为6-20位',
                                                            'user_name': user_name, 'email': email,
                                                            'mobile': mobile, 'role': role})

            # 必须要判断一下email地址是否已经注册过了
            if UserProfile.objects.filter(email=email):
                return render(request, 'user_detail.html', {'user_detail_form': user_detail_form, 'msg': '邮箱地址已存在',
                                                            'user_name': user_name, 'email': email,
                                                            'mobile': mobile, 'role': role})

            # 必须要判断一下手机号是否已经注册过了
            if UserProfile.objects.filter(mobile=mobile):
                return render(request, 'user_detail.html', {'user_detail_form': user_detail_form, 'msg': '手机号已存在',
                                                            'user_name': user_name, 'email': email,
                                                            'mobile': mobile, 'role': role})

            if user_detail_form.is_valid():
                user = UserProfile()
                user.username = user_name
                user.password = make_password(pass_word)
                user.email = email
                user.mobile = mobile
                user.role = role
                user.save()
                return HttpResponseRedirect("/users/")
            else:
                return render(request, 'user_detail.html', {'user_detail_form': user_detail_form,
                                                            'user_name': user_name, 'email': email,
                                                            'mobile': mobile, 'role': role})


class UserDeleteView(View):
    def post(self, request):
        user_name = request.POST.get('username', '')
        user = UserProfile.objects.get(username=user_name)
        if user:
            user.delete()
            return HttpResponseRedirect("/users/")
        else:
            return HttpResponseRedirect("/")


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ResetPwdView(View):
    def get(self, request):
        username = request.user.username
        if UserProfile.objects.get(username=username):
            return render(request, 'password_reset.html')
        else:
            return HttpResponseRedirect("/")

    def post(self, request):
        username = request.user.username
        reset_pwd_form = ResetPwdForms(request.POST)
        if reset_pwd_form.is_valid():
            pwd = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            if pwd != pwd2:
                return render(request, 'password_reset.html', {'msg': '两次密码不一致'})
            else:
                user = UserProfile.objects.get(username=username)
                user.password = make_password(pwd)
                user.save(update_fields=['last_login'])
                return HttpResponseRedirect("/")
        else:
            return render(request, 'password_reset.html', {'reset_pwd_form': reset_pwd_form, 'msg': '输入的密码无效'})


# def index(request):
#     return render(request, 'index.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")
