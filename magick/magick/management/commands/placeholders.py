# -------------------- #
# urls.py file section #
# -------------------- #


URL_IMPORTS = """from app.controllers import %(model)ss_controller"""

URL_HEAD = """
urlpatterns = patterns('',
"""

URL_CRUD_CONFIG = """    url(r'%(model)ss/create/$', %(model)ss_controller.new, name='new_%(model)s'),
    url(r'%(model)ss/$', %(model)ss_controller.index, name='%(model)ss'),
    url(r'%(model)ss/edit/(?P<id>[^/]+)/$', %(model)ss_controller.edit, name='edit_%(model)s'),
    url(r'%(model)ss/(?P<id>[^/]+)/$', %(model)ss_controller.show, name='show_%(model)s'),"""

URL_END = """
)
"""



# --------------------- #
# forms.py file section #
# --------------------- #

FORMS_IMPORTS = """from django import forms
from app.models import *"""

FORMS_MODELFORM_CONFIG = """

class %(modelClass)sForm(forms.ModelForm):

    class Meta:
        model = %(modelClass)s
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(%(modelClass)sForm, self).__init__(*args, **kwargs)

"""





# --------------------- #
# views.py file section #
# --------------------- #

VIEWS_IMPORTS = """
# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

# app specific files

from app.models import *
from app.forms import *
"""

VIEWS_CREATE = """

def new(request):
    form = %(modelClass)sForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = %(modelClass)sForm()

    t = get_template('%(model)ss/new.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

"""

VIEWS_LIST = """

def index(request):
    list_items = %(modelClass)s.objects.all()
    paginator = Paginator(list_items ,10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('%(model)ss/index.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

"""


VIEWS_UPDATE = """

def edit(request, id):
    %(model)s_instance = %(modelClass)s.objects.get(id=id)

    form = %(modelClass)sForm(request.POST or None, instance = %(model)s_instance)

    if form.is_valid():
        form.save()

    t=get_template('%(model)ss/edit.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))
"""

VIEWS_VIEW = """

def show(request, id):
    %(model)s_instance = %(modelClass)s.objects.get(id = id)

    t=get_template('%(model)ss/show.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))
"""


# ------------------------- #
# templates.py file section #
# ------------------------- #



TEMPLATES_CREATE = """{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - Create {%% endblock %%}

{%% block heading %%}<h1>  %(modelClass)s - Create </h1>  {%% endblock %%}
{%% block content %%}
<table>
<form action="" method="POST"> {%% csrf_token %%}
  {{form}}
  <tr>
    <td colspan="2" align="right"><input type="submit" value="Create"/></td>
  </tr>
</form>
</table>
{%% endblock %%}
"""

TEMPLATES_LIST = """{%% extends "base.html" %%}

{%% block title %%} <h1> %(modelClass)s </h1><h2> List </h2> {%% endblock %%}

{%% block heading %%}
<h1> %(modelClass)s</h1>
<h2> List Records</h2>
{%% endblock %%}
{%% block content %%}

<table>
<thead>
<tr><th>Record</th><th colspan="3">Actions</th></tr>
{%% for item in list_items.object_list %%}
  <tr><td>  {{item}}</td> <td><a href="{%% url show_%(model)s item.id %%}">Show</a> </td> <td><a href="{%% url edit_%(model)s item.id %%}">Edit</a></tr>
{%% endfor %%}
<tr><td colspan="3"> <a href="{%% url new_%(model)s %%}">Add New</a></td></tr>
</table>

<div align="center">
{%% if list_items.has_previous %%}
    <a href="?page={{ list_items.previous_page_number }}">Previous</a>
{%% endif %%}

<span class="current">
    Page {{ list_items.number }} of {{ list_items.paginator.num_pages }}.
</span>

{%% if list_items.has_next %%}
        <a href="?page={{ list_items.next_page_number }}">Next</a>
{%% endif %%}

</div>
{%% endblock %%}
"""


TEMPLATES_EDIT = """{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - Edit {%% endblock %%}

{%% block heading %%} <h1> %(modelClass)s</h1><h2> Edit </h2> {%% endblock %%}
{%% block content %%}
<table>
<form action="" method="POST"> {%% csrf_token %%}
  {{form}}
  <tr>
    <td colspan="2" align="right"><input type="submit" value="Save"/></td>
  </tr>
</form>
</table>
{%% endblock %%}
"""

TEMPLATES_VIEW = """{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - View {%% endblock %%}

{%% block heading %%} <h1> %(modelClass)s</h1><h2>View</h2>  {%% endblock %%}
{%% block content %%}
<table>
{{ %(model)s_instance }}
</table>
{%% endblock %%}
"""

TEMPLATES_BASE = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
{% load static_includes %}
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr">

<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
	<meta name="description" content=""/>
	<meta name="keywords" content="" />
	<meta name="author" content="" />
    <title>
        {% block title %} {% endblock %}
    </title>

    {% stylesheet_include_tag 'reset' %}
    {% stylesheet_include_tag 'bootstrap' %}

    {% javascript_include_tag 'jquery-1.7.1.min' %}
    {% javascript_include_tag 'jquery-ui-1.8.16.custom.min' %}
</head>
<body>


<div id="summary">
{% block heading %}
{% endblock %}
</div>

<div id="content">
{% block content %}


{% endblock %}
</div>

</body>
</html>
"""



