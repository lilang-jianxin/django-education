"""education URL Configuration

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
import xadmin
from django.conf.urls import  url,re_path,include
from django.views.generic import TemplateView
from django.views.static import serve
from users.views import LoginView, RegisterView, LogoutView, AciveUserView, ForgetPwdView, ResetView, ModifyPwdView
from users.views import IndexView
from .settings import MEDIA_ROOT
urlpatterns = [
    # re_path('^$', TemplateView.as_view(template_name="index.html"),name='index'),
    re_path('^$', IndexView.as_view(), name='index'),
    re_path('^admin/', xadmin.site.urls),
    re_path('^login/$',LoginView.as_view(),name='login'),
    re_path('^register/$',RegisterView.as_view(),name='register'),
    re_path('^captcha/', include('captcha.urls')),
    re_path(r'^active/(?P<active_code>.*)/$', AciveUserView.as_view(), name="user_active"),
    re_path('^register/$', RegisterView.as_view(), name="register"),
    re_path('^logout/$', LogoutView.as_view(), name="logout"),
    re_path(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    re_path(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    re_path(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    # 用户相关url配置
    url(r'^users/', include(('users.urls','users'), namespace="users")),
    # 课程机构url配置
    re_path('^org/', include(('organization.urls','organization'), namespace="org")),

    # 课程相关url配置
    re_path('^course/', include(('course.urls','courses'), namespace="course")),

    # 配置上传文件的访问处理函数
    re_path('^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # url(r'^static/(?P<path>.*)$',  serve, {"document_root":STATIC_ROOT}),



    # 富文本相关url
    re_path('^ueditor/', include('DjangoUeditor.urls')),

]


#全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

