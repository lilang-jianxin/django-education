___author__ = 'jianxin',
description = '用户信息模板'
__date__ = '2018/6/7 21:41'
import xadmin
from .models import EmailVerifyRecord,Banner
from xadmin import views

class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book-o'

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']



class BaseSetting(object):
    enable_themes = True
    #是否允许切换主题
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "简心后台管理系统"
    site_footer = "简单的心才能做更好的事情"
    menu_style = "accordion"

xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)