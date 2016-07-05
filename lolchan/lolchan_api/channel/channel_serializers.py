from rest_framework import serializers

from lolchan.lolchan_core.models import Channel


class Serializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ['id', 'name', 'description']
