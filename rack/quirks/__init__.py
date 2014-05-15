class BaseQuirk(object):
    template_path = "rack/comics/generic.html"

    @classmethod
    def get_extra_context(cls, comic, strip):
        return {}

    @classmethod
    def save_extra_strip_data(cls, comic, strip, json):
        pass