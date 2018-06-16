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
from django.urls import re_path, include
from django.views.generic import TemplateView

from users.views import LoginView, RegisterView, LogoutView, AciveUserView, ForgetPwdView, ResetView, ModifyPwdView

urlpatterns = [
    re_path('^$', TemplateView.as_view(template_name="index.html"),name='index'),
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

]
