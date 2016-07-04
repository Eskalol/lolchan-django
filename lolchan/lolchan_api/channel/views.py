from rest_framework import viewsets

from lolchan.lolchan_api.channel import channel_serializers
from lolchan.lolchan_core.models import Channel


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Channel.objects.all().order_by('name')
    serializer_class = channel_serializers.Serializer