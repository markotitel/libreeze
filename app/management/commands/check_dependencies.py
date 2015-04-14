__author__ = 'nmilinkovic'

from django.core.management.base import BaseCommand

from app.models import RepoDependency
from app.controller import check_maven_repo_dependency


class Command(BaseCommand):

    def handle(self, *args, **options):

        dependencies = RepoDependency.objects.all()

        fresh_dependencies = []

        for dependency in dependencies:
            latest, release = check_maven_repo_dependency(dependency.group_id, dependency.artifact_id)
            if latest is not None:
                if dependency.latest != latest or dependency.release != release:
                    # Update dependency
                    dependency.latest = latest
                    dependency.release = release
                    dependency.save()
                    fresh_dependencies.append(dependency)

        for dependency in fresh_dependencies:
            print dependency
