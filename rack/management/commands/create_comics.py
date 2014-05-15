import subprocess
from django.core.management.base import BaseCommand, CommandError

from rack.models import Comic


class Command(BaseCommand):
    args = '<comic_codename comic_codename ...>'
    help = 'Create the specified comics.'

    def handle(self, *args, **kwargs):
        for name in args:
            Comic.objects.create(dosage_name=name)
