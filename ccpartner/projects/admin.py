from django.contrib import admin
from .models import Project, Module, Group, Application
# Register your models here.

admin.site.register(Project)
admin.site.register(Module)
admin.site.register(Group)
admin.site.register(Application)