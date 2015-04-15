__author__ = 'nmilinkovic'

import logging

from django.core.management.base import BaseCommand

from app.models import RepoDependency, Project, ProjectDependency
from app.controller import check_maven_repo_dependency
from app.mail import send_update_email

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("Starting dependencies check...")

        dependencies = RepoDependency.objects.all()

        fresh_dependencies = {}

        for dependency in dependencies:

            logger.debug("Checking dependency %s..." % dependency)

            latest, release = check_maven_repo_dependency(dependency.namespace, dependency.name)
            if latest is not None:
                if dependency.latest != latest or dependency.release != release:
                    dependency.latest = latest
                    dependency.release = release
                    dependency.save()
                    logger.info("New version found for dependency %s, dependency updated." % dependency)
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

        logger.info("Dependencies check finished.")
