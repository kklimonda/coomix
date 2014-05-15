import copy
import importlib
import os
import re

from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import File
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone, safestring
from enum import IntEnum
from functools import lru_cache


def _utc_now():
    return datetime.now().replace(tzinfo=timezone.utc)


class DosageUpdateReport(models.Model):
    class Status(IntEnum):
        success = 1
        temporary_error = 2
        error = 3

    STATUS_CHOICES = (
        (1, 'Success'),
        (2, 'Temporary Error'),
        (3, 'Error')
    )

    comic = models.ForeignKey('rack.Comic', related_name='updates')
    timestamp = models.DateTimeField(default=_utc_now)
    status = models.IntegerField(choices=STATUS_CHOICES)
    stacktrace = models.TextField()


class Comic(models.Model):
    dosage_name = models.CharField(max_length=100, primary_key=True)
    override_name = models.CharField(max_length=100, blank=True, null=True)
    site_url = models.URLField(blank=True, null=True)
    last_updated_at = models.DateTimeField(blank=True, null=True)

    @property
    def name(self):
        def normalize_string(string):
            temp = re.sub(r"(.)([A-Z][a-z]+)", r'\1 \2', string)
            return re.sub(r"([a-z0-9])([A-Z])", r'\1 \2', temp)

        # we can manually override the name of the comic, in case if the
        # dosage name isn't useful.
        if self.override_name:
            return self.override_name
        # some comics are part of networks, and dosage name consists
        # of the network, and the name of the comic.
        if '/' in self.dosage_name:
            network, name = self.dosage_name.split('/')
            network = normalize_string(network)
            name = normalize_string(name)
            return "%s (%s)" % (name, network)
        return normalize_string(self.dosage_name)

    @property
    def has_problem(self):
        latest_update_report = self.updates.order_by('-timestamp').first()
        if not latest_update_report:
            return False

        return latest_update_report.status != DosageUpdateReport.Status.success


    def __str__(self):
        return self.name


class StripImage(models.Model):
    strip = models.ForeignKey('rack.Strip', related_name='images')
    order = models.IntegerField()
    image = models.ImageField(upload_to='strips/')

    @classmethod
    def create_images(cls, images):
        objects = []
        for image in images:
            objects += (cls(**image),)
        return objects

    def get_full_media_path(self):
        return os.path.join(settings.MEDIA_URL, self.image.url)


class StripManager(models.Manager):
    def _get_dosage_image(self, dosage_name, file_name):
        # create a file path for the existing image
        dosage_image_path = os.path.join(
            settings.DOSAGE_BASEPATH, dosage_name, file_name
        )
        return open(dosage_image_path, 'rb')

    def _get_media_image_path(self, dosage_name, image):
        media_image_path = os.path.join(
            "strips/", dosage_name, image.name
        )
        return default_storage.save(media_image_path, content=image)

    def get_or_create_with_images(self, comic, data):
        """Given a Comic object and a dictionary with strip/images data, create
        a new Strip objects."""
        # we don't want to operate on data in-place
        data = copy.deepcopy(data)
        images = data.pop('images')
        # check if the strip image already exists, if so the strip has already
        # been created, and should be returned instead.

        strip_image_path = os.path.join(
            "strips/", comic.dosage_name, images[0]['file_name']
        )

        try:
            return Strip.objects.get(images__image=strip_image_path)
        except Strip.DoesNotExist:
            pass

        strip = self.create(comic=comic, url=data['url'])
        for image in images:
            image['strip'] = strip

            file_name = image.pop('file_name')
            dosage_fh = self._get_dosage_image(comic.dosage_name, file_name)
            image_file = File(file=dosage_fh, name=file_name)
            media_image_path = \
                self._get_media_image_path(comic.dosage_name, image_file)

            image['image'] = media_image_path
            image_obj = StripImage.objects.create(**image)
            strip.images.add(image_obj)
        strip.save_extra_data(data)
        return strip

    def get_by_date_descending(self):
        return self.get_queryset().order_by('added_at')


class Strip(models.Model):
    comic = models.ForeignKey("rack.Comic")
    url = models.URLField()
    added_at = models.DateTimeField(default=_utc_now)

    objects = StripManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        module_path = 'rack.quirks.%s' % (self.comic.dosage_name.lower(),)
        try:
            module = importlib.import_module(module_path)
        except ImportError:
            # if no specific quirk module, load the dummy quirk class.
            from rack.quirks import BaseQuirk
            self.quirk = BaseQuirk()
            self.template = 'generic'
        else:
            quirk_class_name = self.comic.dosage_name.lower()
            self.quirk = getattr(module, quirk_class_name)
            self.template = self.comic.dosage_name.lower()

    def __str__(self):
        return "%s strip for %s" % (self.comic.name, self.added_at)

    def save_extra_data(self, json):
        self.quirk.save_extra_strip_data(self.comic, self, json)

    def get_template_path(self):
        return self.quirk.template_path

    def get_template_context(self):
        context = {
            'strip': self
        }
        if self.quirk:
            context.update(
                self.quirk.get_extra_context(self.comic, self)
            )
        return context

    def render_template(self):
        template = self.get_template_path()
        context = self.get_template_context()
        return render_to_string(template, context)
