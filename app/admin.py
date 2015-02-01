from django.contrib import admin

from app.models import Project, Developer, MavenDependency

# Register your models here.

admin.site.register(Project)
admin.site.register(Developer)
admin.site.register(MavenDependency)
