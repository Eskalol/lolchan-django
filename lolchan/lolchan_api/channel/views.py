from django.http import Http404
from django.db.models import FieldDoesNotExist
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status


from lolchan.lolchan_api.channel import channel_serializers
from lolchan.lolchan_core.models import Channel
from lolchan.lolchan_api.permission import permission


class ChannelViewList(APIView):
    def get(self, request, *args, **kwargs):
        channels = Channel.objects.all().order_by('name')
        serializer = channel_serializers.Serializer(channels, many=True)
        return Response(serializer.data)


class ChannelViewListOrder(APIView):
    def get(self, request, order, *args, **kwargs):
        field = order
        if order[0] == '-':
            field = order[1:]
        try:
            Channel._meta.get_field_by_name(field)
        except FieldDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Exception': '{}: field does not exist'.format(order)})
        channels = Channel.objects.all().order_by(order)
        serializer = channel_serializers.Serializer(channels, many=True)
        return Response(serializer.data)


class ChannelViewDetail(ViewSet):
    serializer_class = channel_serializers.Serializer
    permission_classes = (permission.IsAuthenticatedOrReadOnly, )

    def get_object(self, pk):
        try:
            return Channel.objects.get(pk=pk)
        except Channel.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        channel = self.get_object(pk)
        serializer = self.serializer_class(channel)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        channel = self.get_object(pk)
        serializer = self.serializer_class(channel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        channel = self.get_object(pk)
        channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)