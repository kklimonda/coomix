from django.core.management.base import BaseCommand, CommandError

from rack.models import Comic


class Command(BaseCommand):
    args = '<comic_codename comic_codename ...>'
    help = 'Update all the comics with subscriptions, or the comics specified'

    def handle(self, *args, **kwargs):
        from rack.tasks import fetch_latest
        if len(args) == 0:
            comics = Comic.objects.all()
        else:
            comics = Comic.objects.filter(dosage_name__in=args)
        for comic in comics:
            fetch_latest(comic)

    def get_comics_queryset(self, comics):
        if len(comics) > 0:
            return Comic.objects.filter(dosage_name__in=comics)
        else:
            return Comic.objects.all()

    def filter_comics_qs(self, comics):
        return comics.filter(users__count=0)

    def run_dosage_manager(self, queryset):
        names = queryset.values_list('dosage_name', flat=True)
        print(names)
