from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import AccessMixin,LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.list import ListView
from django.core.serializers import serialize
from django.views.generic import TemplateView,View
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from permission.models import Permission
from wssh.models import *

class Index(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = 'webterminal/terminal.html'
    permission_required = 'wssh.can_connect_serverinfo'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        try:
            groups = Permission.objects.get(user__username=self.request.user.username)
        except ObjectDoesNotExist:
            #print("*" * 10, self.request.user.username, groups)
            return context
        context['groups'] = ServerGroup.objects.filter(name__in = [group.name for group in groups.groups.all()])
        print("*" * 10, self.request.user.username, context['groups'])
        return context

#class CredentialCreate(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
class CredentialCreate(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    permission_required = 'wssh.can_add_credential'
    template_name = 'comm/credentialcreate.html'
    def post(self,request):
        #QueryDict转化成字典
        data = request.POST.dict()
        print("================",type(data),data)
        fields = [field.name for field in Credential._meta.get_fields()]
        [data.pop(field) for field in list(data.keys()) if field not in fields]
        if not request.user.has_perm('wssh.can_add_credential'):
            raise PermissionDenied(_('Your has not permission to add credential'))
        obj = Credential.objects.create(**data)
        obj.save()
        return redirect("/wssh/")

class CredentialList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Credential
    template_name = "comm/credentiallist.html"
    permission_required = 'wssh.can_view_credential'
    raise_exception = True

class CredentialDetailApi(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = "wssh.can_view_credential"

    def post(self,request):
        id = request.POST.get('id',None)
        if id != None:
            obj = Credential.objects.get(id=id)
            if obj:
                return JsonResponse({'status':True,'message':json.loads(serialize('json',obj))[0]['fields']})
            else:
                return JsonResponse({'status':False,'message':'Request object not exist!'})
        else:
            return JsonResponse({'status':False,'message':'Method not allowed!'})

class ServerCreate(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = "comm/servercreate.html"
    permission_required = 'wssh.can_add_serverinfo'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(ServerCreate, self).get_context_data(**kwargs)
        context['credentials'] = Credential.objects.all()
        return context


class ServerlList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = ServerInfor
    template_name = 'comm/serverlist.html'
    permission_required = 'wssh.can_view_serverinfo'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(ServerlList, self).get_context_data(**kwargs)
        context['credentials'] = Credential.objects.all()
        return context

class GroupCreate(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = "comm/servercreate.html"
    permission_required = 'wssh.can_add_serverinfo'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(GroupCreate, self).get_context_data(**kwargs)
        context['servers'] = ServerInfor.objects.all()
        return context

class GroupList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = ServerInfor
    template_name = 'comm/serverlist.html'
    permission_required = 'wssh.can_view_serverinfo'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(ServerlList, self).get_context_data(**kwargs)
        context['servers'] = ServerInfor.objects.all()
        return context