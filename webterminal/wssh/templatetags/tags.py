from django import template
from wssh.models import Menu
from wssh import models
from django.utils.safestring import mark_safe
import django

register = template.Library()

@register.simple_tag
def menu_list():
    """
    获取菜单
    :return:
    """
    menu_html = ''
    menu_dict = dict()
    menu_query = Menu.objects.order_by('priority')
    for query in menu_query:
        if query.parent != None:
            if str(query.parent) not in  menu_dict:
                menu_dict[str(query.parent)] = {}
            menu_dict[str(query.parent)][str(query.name)] = {}
            menu_dict[str(query.parent)][str(query.name)] = {
                'url':query.url,
                'show':query.show
            }
            #menu_dict[query.parent][query.name]['url'] = query.url
            #menu_dict[query.parent][query.name]['show'] = query.show
        else:
            menu_dict[str(query.name)] = {
                'url':query.url,
                'show':query.show
            }
            #menu_dict[query.name]['url'] = query.url
            #menu_dict[query.name]['show'] = query.show
    for k,v in menu_dict.items():
        if 'show' in menu_dict[k] and menu_dict[k]['show'] == True:
            menu_html += """<li class="treeview">
                    <a href="%s">
                        <i class="fa fa-table"></i> <span>%s</span>
                        <span class="pull-right-container">
                              <i class="fa fa-angle-left pull-right"></i>
                        </span>
                    </a>
                    <ul class="treeview-menu">"""%(menu_dict[k]['url'],k)
            for k1 in v:
                if k1 == 'show' or k1 == 'url':
                    continue
                #print("*"*10,menu_dict,type(k),type(k1),k,k1)
                menu_html += """<li><a href="%s"><i class="fa fa-circle-o"></i>%s</a></li>"""%(menu_dict[k][k1]['url'],k1)

            menu_html += """</ul></li>"""
    return mark_safe(menu_html)

@register.simple_tag
def render_table_form(table_name):
    table_form = """<div class="box-body">"""

    if hasattr(models,table_name):
        #获取全部的字段名称
        fields = [field for field in getattr(models,table_name)._meta.fields]
        for field in fields:
            #print("===============", type(field))
            if field == None or field.name == 'id':
                continue
            if hasattr(field,"choices") and len(field.choices) > 0:
                table_form += """
                <div class="form-group">
                    <label class="col-sm-2 control-label">%s</label>
                    <div class="col-sm-10">
                    <select class="form-control" name="%s">
                """%(field.name,field.name)
                for index,choice in enumerate(field.choices):
                    table_form +="""<option id="%s">%s</option>"""%(index,choice[1])
                table_form += """</select></div></div>"""
            elif isinstance(field,django.db.models.fields.TextField):
                table_form += """<div class="form-group">
                  <label class="col-sm-2 control-label">%s</label>
                  <div class="col-sm-10">
                  <textarea class="form-control" rows="5" placeholder="Enter Key..." name="%s"></textarea>
                </div></div>"""%(field.name,field.name)
            elif isinstance(field,django.db.models.fields.BooleanField):
                table_form += """<div class="form-group">
                    <label class="col-sm-2 control-label">%s</label>
                  <div class="col-sm-10">
                    <input type="radio" name="%s" value="True">是
                    <input type="radio" name="%s" value="False">否
                  </div>
              </div>"""%(field.name,field.name,field.name)
            else:
                table_form += """<div class="form-group">
                  <label class="col-sm-2 control-label">%s</label>
                  <div class="col-sm-10">
                    <input class="form-control"  placeholder="%s" name="%s">
                  </div>
                </div>"""%(field.name,field.name,field.name)
    table_form += """<div class="pull-right">
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
              </div>"""
    return mark_safe(table_form)

@register.simple_tag
def render_table_data(table_name):
    table_html = ""
    if hasattr(models,table_name):
        table_html = """<!-- Content Header (Page header) -->
           <section class="content-header">
           <h1>
           %s
           <small>advanced tables</small>
           </h1>
           <ol class="breadcrumb">
           <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
           <li><a href="#">Tables</a></li>
           <li class="active">%s</li>
           </ol>
           </section>

           <!-- Main content -->
           <section class="content">
           <div class="row">
           <div class="col-xs-12">

             <div class="box">
               <div class="box-header">
                <h3 class="pull-left">%s</h3>
                 <div class="btn-group  pull-right">
                    <button type="button" class="btn btn-info">Action</button>
                    <button type="button" class="btn btn-info dropdown-toggle" data-toggle="dropdown">
                    <span class="caret"></span>
                    <span class="sr-only">Toggle Dropdown</span>
                    </button>
                    <ul class="dropdown-menu" role="menu">
                        <li><a href="/credentialcreate/">Add</a></li>
                        <li><a href="/credentialdetailapi/">Detail</a></li>
                    </ul>
                </div>
               </div>
               
               <!-- /.box-header -->
               <div class="box-body">
               <table id="example1" class="table table-bordered table-striped">
                   <thead>""" % (table_name, table_name,table_name)
        #获取全部的字段名称
        fields = [field for field in getattr(models,table_name)._meta.fields]
        table_html += """<tr>"""
        for field in fields:
            #print("===============", type(field))
            if field == None or field.name == 'id':
                continue
            table_html += "<th>%s</th>"%field.name
        table_html += """</tr></thead>"""
        table_html += """<tbody>"""
        objs = getattr(models,table_name).objects.all()
        for obj in objs:
            table_html += """<tr>"""
            for field in fields:
                if field.name == "id":
                    continue
                table_html += """<td>%s</td>"""%getattr(obj,str(field.name),None)
            table_html += """</tr>"""
        table_html += """</tbody></table>"""
        table_html += """</div></div></div></div></section>"""
    return mark_safe(table_html)

@register.simple_tag
def get_related_servers(group):
    servergroups = models.ServerGroup.objects.get(name=group)
    serverlist = servergroups.servers.all()
    print("="*10,serverlist)
    return serverlist


