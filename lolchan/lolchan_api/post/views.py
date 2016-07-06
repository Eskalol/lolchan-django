from rest_framework.permissions import AllowAny
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from lolchan.lolchan_api.post import post_serializers
from lolchan.lolchan_core.models import Post


class PostViewVote(APIView):

    serialiser_class = post_serializers.VoteSerializer
    permission_classes = (AllowAny, )

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        serializer = self.serialiser_class(post)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        serializer = self.serialiser_class(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
