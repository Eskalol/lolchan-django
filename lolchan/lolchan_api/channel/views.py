from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lolchan.lolchan_api.channel import channel_serializers
from lolchan.lolchan_core.models import Channel


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all().order_by('name')
    serializer_class = channel_serializers.Serializer