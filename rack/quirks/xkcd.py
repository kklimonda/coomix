import os
import shutil

from django.conf import settings

from . import BaseQuirk


class xkcd(BaseQuirk):
    template_path = "rack/comics/xkcd.html"

    @classmethod
    def _get_alt_text_source_target(cls, comic, strip):
        image_path = strip.images.all()[0].image.path
        image_basename = os.path.splitext(os.path.basename(image_path))[0]
        alt_text_source = os.path.join(
            settings.DOSAGE_BASEPATH,
            comic.dosage_name, "%s.txt" % (image_basename,)
        )
        alt_text_target = os.path.join(
            settings.MEDIA_ROOT, "strips/",
            comic.dosage_name, "%s.txt" % (image_basename,)
        )

        return (alt_text_source, alt_text_target)

    @classmethod
    def get_extra_context(cls, comic, strip):
        # xkcd provides an extra content via the alt image tag. Dosage saves
        # it as a separate .txt file, with the same basepath as the
        # image itself. Load the content of that file as a 'alt_text' context
        # variable.
        _, alt_text_target = cls._get_alt_text_source_target(comic, strip)
        context = {}
        with open(alt_text_target, 'r') as fh:
            context['alt_text'] = fh.read()
        return context

    @classmethod
    def save_extra_strip_data(cls, comic, strip, json):
        alt_text_source, alt_text_target = \
            cls._get_alt_text_source_target(comic, strip)
        shutil.copy(alt_text_source, alt_text_target)
