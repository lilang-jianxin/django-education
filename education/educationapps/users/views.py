# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password

from users.form import LoginForm
from users.models import UserProfile
from .form import RegisterForm
from operation.models import UserMessage
from users.models import EmailVerifyRecord
from utils.emaile_utils import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username));
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_from = LoginForm(request.POST)
        if login_from.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"login_form": login_from})
        else:
            return render(request, "login.html", {"login_form": login_from})


class LogoutView(View):
    """
       用户登出
       """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在",
                                                         "username": request.POST.get("email", ""),
                                                         "password": request.POST.get("password", "")})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()
            # 邮箱发送
            status = send_register_email(user_name, "register")
            if status is None:
                UserProfile.objects.filter(username=user_name, email=user_name).delete()
                UserMessage.objects.filter(user=user_profile.id, message='欢迎注册慕学在线网').delete()
                return render(request, "register.html",
                              {"register_form": register_form, "username": request.POST.get("email", ""),
                               "password": request.POST.get("password", "")})
            return render(request, "login.html")
        else:
            return render(request, "register.html",
                          {"register_form": register_form, "username": request.POST.get("email", ""),
                           "password": request.POST.get("password", "")})


class AciveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")
