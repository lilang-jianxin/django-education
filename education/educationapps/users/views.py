#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect


from users.form import LoginForm
from users.models import UserProfile
# Create your views here.
class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})
    def post(self,request):
        login_from=LoginForm()
        if login_from.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user=authenticate(username=user_name,password=pass_word)
            if user is not  None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"login_form": login_from})
        else:
            return render(request, "login.html", {"login_form": login_from})
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
                user=UserProfile.objects.get(Q(username=username)|Q(email=username));
                if user.check_password(password):
                    return user
        except Exception as e:
            return None