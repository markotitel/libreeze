from django.contrib import admin

from app.models import MavenRepoDependency, Developer, MavenProject, MavenProjectDependency

# Register your models here.

admin.site.register(MavenRepoDependency)
admin.site.register(Developer)
admin.site.register(MavenProject)
admin.site.register(MavenProjectDependency)
