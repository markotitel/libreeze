from django.contrib import admin

from app.models import Project, Developer, ProjectDependency, LatestDependency

# Register your models here.

admin.site.register(Project)
admin.site.register(Developer)
admin.site.register(ProjectDependency)
admin.site.register(LatestDependency)