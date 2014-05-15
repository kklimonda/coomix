from rest_framework import routers
from rest_framework import viewsets
from rest_framework.views import APIView

from rack.models import Strip
from rack.models import StripImage
from rack.serializers import StripSerializer
from rack.serializers import StripImageSerializer


class StripViewSet(viewsets.ModelViewSet):
    queryset = Strip.objects.all()
    serializer_class = StripSerializer


class StripImageViewSet(viewsets.ModelViewSet):
    queryset = StripImage.objects.all()
    serializer_class = StripImageSerializer


router = routers.DefaultRouter()
router.register('strips', StripViewSet)
router.register('images', StripImageViewSet)
