import factory

from rack.models import DosageUpdateReport

class ComicFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'rack.Comic'

    dosage_name = factory.Sequence(lambda n: "DosageName%s" % (n,))


class StripFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'rack.Strip'

    comic = factory.SubFactory(ComicFactory)


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'core.User'


class DosageUpdateReportFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'rack.DosageUpdateReport'

    status = DosageUpdateReport.Status.success