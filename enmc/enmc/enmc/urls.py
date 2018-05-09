"""enmc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve


from apps.equipments.views import index
from enmc.settings import MEDIA_ROOT
import xadmin


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    url(r'^(?:index.html)?$', index, name='index'),
    url(r'^users/', include('apps.users.urls', namespace='users')),
    url(r'^directories/', include('apps.directories.urls', namespace='directories')),
    url(r'^equipments/', include('apps.equipments.urls', namespace='equipments')),
    url(r'^applications/', include('apps.applications.urls', namespace='applications')),
    url(r'^search/', include('apps.search.urls', namespace='search')),

    # 配置上传文件的访问处理
    url(r'^upload/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]