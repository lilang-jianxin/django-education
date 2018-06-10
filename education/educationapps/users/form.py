#-*- coding:utf-8 -*-
___author__ = 'jianxin',
description = ''
__date__ = '2018/6/9'
from  django import forms
from captcha.fields import CaptchaField
class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(required=True,min_length=6)
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})

