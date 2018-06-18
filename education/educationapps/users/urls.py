___author__ = 'jianxin',
description = ''
__date__ = '2018/6/18'
from django.conf.urls import re_path
from .views import UserinfoView
urlpatterns=[
    ###用户信息
    re_path('^info/$',UserinfoView.as_view(),name='user_info')
]