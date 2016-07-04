from rest_framework import serializers

from lolchan.lolchan_core.models import Channel


class Serializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_slug')

    class Meta:
        model = Channel
        fields = ['id', 'slug', 'name', 'description', 'value']

    def get_slug(self, channel):
        return channel.slug
