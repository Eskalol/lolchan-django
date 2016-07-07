from rest_framework.permissions import AllowAny
from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from lolchan.lolchan_api.post import post_serializers
from lolchan.lolchan_core.models import Post
from lolchan.lolchan_api.permission import permission


class PostListFilterView(generics.mixins.ListModelMixin,
                         generics.mixins.CreateModelMixin,
                         generics.GenericAPIView):
    serializer_class = post_serializers.PostModelSerializer
    permission_classes = (permission.PostViewPermission, )

    def get_queryset(self):
        pk = self.request.query_params.get('id', None)
        if pk:
            queryset_list = Post.objects.filter(pk=pk)
        else:
            queryset_list = Post.objects.all()
            query_text = self.request.query_params.get('text', None)
            if query_text:
                queryset_list = queryset_list.filter(
                    Q(title__icontains=query_text) |
                    Q(text__icontains=query_text) |
                    Q(channel__name__icontains=query_text)
                ).distinct()
        if not queryset_list:
            raise Http404
        return queryset_list

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostUpdateDestroyView(generics.mixins.UpdateModelMixin,
                            generics.mixins.RetrieveModelMixin,
                            generics.mixins.DestroyModelMixin,
                            generics.GenericAPIView):

    serializer_class = post_serializers.PostModelSerializer
    permission_classes = (permission.PostViewUpdateDestroy, )

    def get_object(self):
        pk = self.request.query_params.get('id', None)
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
