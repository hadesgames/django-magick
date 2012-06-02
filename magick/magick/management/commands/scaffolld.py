"""
Copyright (c) 2011, django-groundwork authors
All rights reserved.

Redistribution and use in source and binary forms, with or without modific-
ation, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.
The names of of the django-groundwork contributors may not be used to
endorse or promote products derived from this software without specific
prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSE-
QUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import models
from placeholders import *
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        "Usage : manage.py scaffold <app> <model>"

        PROJECT_ROOT = os.getcwd()


        for iaf in xrange(1):

            app = args[0] # App name is the first parameter
            model_names = args[1:] # Models which need to be scaffolded will follow

            model_instances = [ models.get_model(app, x) for x in model_names ]

            FORMS_DIR = os.path.join( PROJECT_ROOT, app, 'forms')
            CONTROLLERS_DIR = os.path.join( PROJECT_ROOT, app, 'controllers')
            VIEWS_DIR = os.path.join( PROJECT_ROOT , app, 'views')

            urls = ""
            # url config
            for model_instance in model_instances:
                urls = URL_IMPORTS % {'model': model_instance._meta.object_name.lower()}

            urls += URL_HEAD

            # Generate CRUD urls for each model
            for model_instance in model_instances:
                urls += URL_CRUD_CONFIG % {'model': model_instance._meta.object_name.lower(), 'modelClass': model_instance._meta.object_name }

            urls += URL_END

            # write to urls.py
            f = open( os.path.join (PROJECT_ROOT , app, 'routes.py') , 'a')
            f.write(urls)
            f.close()

            # append to root urlconf
            f = open( os.path.join (PROJECT_ROOT , 'routes.py') , 'a')
            f.write( "\nurlpatterns += patterns ('',\n    (r'^%(app)s/', include('%(app)s.routes')),\n)\n" % {'app': app } )
            f.close()



            # forms
            for model_instance in model_instances:
                forms_content = FORMS_IMPORTS
                forms_content += FORMS_MODELFORM_CONFIG % { 'modelClass' : model_instance._meta.object_name }
                formspath = os.path.join (FORMS_DIR, '%ss.py' % model_instance._meta.object_name.lower())
                f = open( formspath , 'w')
                f.write(forms_content)
                f.close()


            # views

            for model_instance in model_instances:
                views_content = VIEWS_IMPORTS
                views_content += VIEWS_CREATE
                views_content += VIEWS_LIST
                views_content += VIEWS_VIEW
                views_content += VIEWS_UPDATE

                views_content = views_content %  {'model':model_instance._meta.object_name.lower(), 'modelClass': model_instance._meta.object_name, 'app': app }

                viewspath = os.path.join (CONTROLLERS_DIR, '%ss_controller.py' % model_instance._meta.object_name.lower())
                f = open( viewspath, 'w')
                f.write(views_content)
                f.close()


            # Templates

            print "Generate base template? [Y/N]?"
            yn = raw_input()
            if yn.lower() == 'y':
                f = open(os.path.join(VIEWS_DIR, 'base.html') , 'w')
                f.write(TEMPLATES_BASE)
                f.close()

            for model_instance in model_instances:
                template_dir = os.path.join(VIEWS_DIR, model_instance._meta.object_name.lower() + 's')
                if not os.path.exists(template_dir):
                    os.makedirs(template_dir)
                print template_dir


                f = open(os.path.join( VIEWS_DIR, model_instance._meta.object_name.lower() + 's', 'new.html'),'w')
                f.write( TEMPLATES_CREATE  %  { 'modelClass' : model_instance._meta.object_name } )
                f.close()

                f = open(os.path.join( VIEWS_DIR, model_instance._meta.object_name.lower() + 's', 'index.html') ,'w')
                f.write( TEMPLATES_LIST  %  { 'modelClass' : model_instance._meta.object_name ,'model' : model_instance._meta.object_name.lower(), 'app' : app} )
                f.close()

                f = open(os.path.join( VIEWS_DIR, model_instance._meta.object_name.lower() + 's', 'edit.html') ,'w')
                f.write( TEMPLATES_EDIT  %  { 'modelClass' : model_instance._meta.object_name } )
                f.close()

                f = open(os.path.join( VIEWS_DIR, model_instance._meta.object_name.lower() + 's', 'show.html') , 'w')
                f.write( TEMPLATES_VIEW  %  { 'modelClass' : model_instance._meta.object_name,  'model' : model_instance._meta.object_name.lower()} )
                f.close()
""""        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly
            print "Usage : manage.py scaffold <app> <model>"
"""
