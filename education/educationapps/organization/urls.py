___author__ = 'jianxin',
description = '机构信息路由配置'
__date__ = '2018/6/18'
from django.conf.urls import re_path,include
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
from .views import TeacherListView, TeacherDetailView
urlpatterns=[
    # 课程机构列表页
    re_path(r'^list/$', OrgView.as_view(), name="org_list"),
    re_path(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    re_path(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    re_path(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    re_path(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    re_path(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),

    # 机构收藏
    re_path(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 讲师列表页
    re_path(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),

    # 讲师详情页
    re_path(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]