# -*- coding:utf-8 -*-
import json
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import PageNotAnInteger,Paginator
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
from users.form import ForgetForm,ModifyPwdForm
from utils.mixin_utils import LoginRequiredMixin
from .form import UserInfoForm
from operation.models import UserCourse,UserFavorite
from organization.models import CourseOrg,Teacher
from course.models import Course
from .models import Banner
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

class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            user=UserProfile.objects.filter(email=email)
            if not user:
                return render(request, "forgetpwd.html",{"msg":"您尚未注册，请您注册"})
            status=send_register_email(email, "forget")
            return render(request, "forgetpwd.html",{"msg":status})
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})

class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    """
       修改用户密码
       """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.filter(email=email)
            if user:
                user[0].password = make_password(pwd2)
                user[0].save()
                return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})

class UserinfoView(LoginRequiredMixin,View):
    '''
    用户个人信息
    '''
    def get(self,request):
        return render(request, 'usercenter-info.html', {})
    def post(self,request):
        user_info_form=UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors,ensure_ascii=False),content_type="'application/json'")

class UploadImageView(LoginRequiredMixin,View):
    '''
    用户头像上传
    '''
    def post(self,request):
        from .form import UploadImageForm
        image_form=UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(json.dumps({"status":"success"},ensure_ascii=False), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status":"failure"},ensure_ascii=False), content_type='application/json')

class UpdatePwdView(LoginRequiredMixin,View):
    '''
    用户个人中心修改密码
    '''
    def post(self,req):
        modify_form=ModifyPwdForm(req.POST)
        if modify_form.is_valid():
            pw1=req.POST.get("password1","")
            pw2 = req.POST.get("password2", "")
            if pw1!=pw2:
                return HttpResponse(HttpResponse(json.dumps({"status":"failure","msg":"密码不一致"},ensure_ascii=False), content_type='application/json'))
            user=req.user
            user.password=make_password(pw1)
            user.save()
            return HttpResponse(json.dumps({"status":"success"},ensure_ascii=False), content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors,ensure_ascii=False),content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin,View):
    '''
    发送邮箱验证码
    '''
    pass

class UpdateEmailView(LoginRequiredMixin,View):
    '''
    修改邮箱
    '''
    pass
class MyCourseView(LoginRequiredMixin,View):
    '''
    我的课程
    '''
    def get(self,req):
        user_course=UserCourse.objects.filter(user=req.user)
        return render(req,'usercenter-mycourse.html',{"user_courses":user_course})

class MyFavOrgView(LoginRequiredMixin,View):
    '''
    我收藏的课程机构
    '''
    def get(self,request):
        org_list=[]
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list
        })


class MyFavTeacherView(LoginRequiredMixin,View):
    '''
    我收藏的授课讲师
    '''

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list
        })


class MyFavCourseView(LoginRequiredMixin,View):
    '''
    我收藏的课程
    '''

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list
        })

class MymessageView(LoginRequiredMixin,View):
    '''
    我的消息
    '''

    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "messages": messages
        })


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
class IndexView(View):
    #慕学在线网 首页
    def get(self, request):
        #取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })