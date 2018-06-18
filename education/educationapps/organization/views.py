#-*- coding:utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite
from course.models import Course
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.

class OrgView(View):
   '''
   课程机构列表功能
   '''
   pass


class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    pass

class OrgHomeView(View):
    '''
    机构首页
    '''
    pass

class OrgCourseView(View):
    '''
    机构课程列表页
    '''
    pass

class OrgDescView(View):
    '''
    机构介绍页
    '''
class OrgTeacherView(View):
    '''
        机构教师页
    '''
    pass
class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """

class TeacherListView(View):
    """
    课程讲师列表页
    """


class TeacherDetailView(View):
    pass