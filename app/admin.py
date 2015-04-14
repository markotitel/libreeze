from django.contrib import admin

from app.models import RepoDependency, Developer, Project, ProjectDependency

# Register your models here.

admin.site.register(Developer)
admin.site.register(RepoDependency)
admin.site.register(Project)
admin.site.register(ProjectDependency)
