from rest_framework import serializers

from rack.models import Strip
from rack.models import StripImage


class StripImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='get_full_media_path', read_only=True)

    class Meta:
        model = StripImage
        fields = ('image', 'order',)


class StripSerializer(serializers.ModelSerializer):
    images = StripImageSerializer(many=True)
    template = serializers.CharField(source='template', read_only=True)
    extra_data = serializers.CharField(source='extra_data', read_only=True)

    class Meta:
        model = Strip
        fields = ('id', 'images', 'template',)
