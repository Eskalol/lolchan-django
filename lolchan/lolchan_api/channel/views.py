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
    serializer_class = channel_serializers.Serializer
    permission_classes = (permission.IsAuthenticatedOrReadOnly, )

    def get(self, request, *args, **kwargs):
        """
        List all channels

        """
        channels = Channel.objects.all().order_by('name')
        serializer = self.serializer_class(channels, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new channel

        ---
        parameters:
            - name: name
              type: string
              required: true
              description: channel name
            - name: description
              type: string
              required: false
              description: channel description
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChannelViewListOrder(APIView):
    def get(self, request, order, *args, **kwargs):
        """
            Get list with order

            ---
            parameters:
                - name: order
                  type: string
                  required: true
                  paramType: path
                  description: order by
            """
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

    def retrieve(self, request, pk, *args, **kwargs):
        """
            Retrieve channel

            ---
            parameters:
                - name: pk
                  type: Int
                  required: true
                  paramType: path
                  description: primary key
            """
        channel = self.get_object(pk)
        serializer = self.serializer_class(channel)
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        """
            Update channel

            ---
            parameters:
                - name: pk
                  type: Int
                  required: true
                  paramType: path
                  description: primary key
                - name: name
                  type: string
                  required: false
                  description: channel name
                - name: description
                  type: string
                  required: false
                  description: channel description
            """
        channel = self.get_object(pk)
        serializer = self.serializer_class(channel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        """
            Destroy channel

            ---
            parameters:
                - name: pk
                  type: Int
                  required: true
                  paramType: path
                  description: primary key
            """
        channel = self.get_object(pk)
        channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)