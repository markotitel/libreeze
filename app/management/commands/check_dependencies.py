__author__ = 'nmilinkovic'

from django.core.management.base import BaseCommand

from app.models import RepoDependency, Project, ProjectDependency
from app.controller import check_maven_repo_dependency
from app.mail import send_update_email


class Command(BaseCommand):

    def handle(self, *args, **options):

        dependencies = RepoDependency.objects.all()

        fresh_dependencies = {}

        for dependency in dependencies:

            latest, release = check_maven_repo_dependency(dependency.namespace, dependency.name)
            if latest is not None:
                if dependency.latest != latest or dependency.release != release:
                    dependency.latest = latest
                    dependency.release = release
                    dependency.save()
                    fresh_dependencies[dependency.key()] = dependency

        projects = Project.objects.filter(send_updates=True)

        for project in projects:
            updated_dependencies = []
            project_dependencies = ProjectDependency.objects.filter(project=project)

            for project_dependency in project_dependencies:
                if project_dependency.key() in fresh_dependencies:
                    updated_dependencies.append(fresh_dependencies[project_dependency.key()])

            if updated_dependencies:
                developer_email = project.developer.email
                send_update_email(developer_email, project, updated_dependencies)
