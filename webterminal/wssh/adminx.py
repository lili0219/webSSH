import xadmin
from .models import ServerInfor,Menu,Credential,ServerGroup
from permission.models import Permission
from xadmin import views

class CredentialAdmin(object):
    list_diplay = ['name','username','port','method','key','password','proxy','proxyserverip','proxyport','proxypassword','protocol']

class ServerInforAdmin(object):
    list_display = ['name','hostname','ip',]
    search_fields = ['ip',]

class PermissionAdmin(object):
    list_display = ['user','permissions','groups']

class MenusAdmin(object):
    ordering = ('-parent',)
    list_filter = ('name',)
    list_display = ['name', 'parent', 'show', 'url', 'priority', 'permission_id']
    fields = ['name', 'parent', 'show', 'url', 'priority', 'permission_id']

class ServerGroupAdmin(object):
    list_display = ['name','servers']

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    site_title = "Amazing Xadmin"
    site_footer = "http://www.baidu.com"
    menu_style = "accordion"

xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(ServerGroup,ServerGroupAdmin)
xadmin.site.register(ServerInfor,ServerInforAdmin)
xadmin.site.register(Credential,CredentialAdmin)
xadmin.site.register(views.CommAdminView,GlobalSetting)
xadmin.site.register(Menu,MenusAdmin)
xadmin.site.register(Permission,PermissionAdmin)