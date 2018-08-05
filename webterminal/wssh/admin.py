from django.contrib import admin
from .models import ServerInfor,Menu,Credential,ServerGroup
from permission.models import Permission

class CredentialAdmin(admin.ModelAdmin):
    list_diplay = ['name','username','port','method','key','password','proxy','proxyserverip','proxyport','proxypassword','protocol']

class ServerInforAdmin(admin.ModelAdmin):
    list_display = ['name','hostname','ip',]
    search_fields = ['ip',]

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['user',]

class MenusAdmin(admin.ModelAdmin):
    ordering = ('-parent',)
    list_filter = ('name',)
    list_display = ['name', 'parent', 'show', 'url', 'priority', 'permission_id']
    fields = ['name', 'parent', 'show', 'url', 'priority', 'permission_id']

class ServerGroupAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(ServerGroup,ServerGroupAdmin)
admin.site.register(ServerInfor,ServerInforAdmin)
admin.site.register(Credential,CredentialAdmin)
admin.site.register(Menu,MenusAdmin)
admin.site.register(Permission,PermissionAdmin)
