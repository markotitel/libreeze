__author__ = 'nmilinkovic'

from django.core.management.base import BaseCommand, CommandError
from app.models import MavenRepoDependency

class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Updating...'
