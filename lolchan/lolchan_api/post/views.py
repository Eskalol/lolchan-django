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
        """
        Gets a list of posts.

        Text filter - will match with a post title,
            text, and name of channel that it belongs to.
        Pk filter - will match with a primary key of a post

        ---
        parameters:
            - name: text
              required: false
              paramType: query
              type: int
              description: text to match
            - name: pk
              required: false
              paramType: query
              type: int
              description: primary key to match

        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates a new post

        When creating a post we are not allowed to give yourself 1000 votes,
            therefore votes is set to 0
        ---
        parameters:
            - name: channel
              required: true
              paramType: form
              type: int
              description: channel id that the post belongs to
            - name: title
              required: true
              paramType: form
              type: string
              description: post title
            - name: text
              required: true
              paramType: form
              type: string
              description: post text
        """
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
        """
            Gets a post by id

            ---
            parameters:
                - name: id
                  required: true
                  paramType: query
                  type: int
                  description: The id of a post
            """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Updates a post

        Since anonymous users should be able to vote a post, they should only
        be allowed to change the "votes" field, and to prevent users from
        voting a post by 1000 up or down in one request we'll only change "votes"
        by 1

        if > 0 votes increments by 1
        if < 0 votes decrements by 1
        if 0 votes will stay the same
        ---
        parameters:
            - name: id
              required: true
              paramType: query
              type: int
              description: The id of the post to edit
            - name: channel
              required: false
              paramType: form
              type: int
              description: channel id that post belongs to(will not be changed)
            - name: title
              required: false
              paramType: form
              type: string
              description: post title(will not be changed)
            - name: text
              required: false
              paramType: form
              type: string
              description: post text(will not be changed)
            - name: votes
              required: true
              paramType: form
              type: int
              description: number of votes
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        deletes a post by id

        ---
        parameters:
            - name: id
              required: true
              paramType: query
              type: int
              description: The id of the post to delete
        """
        return self.destroy(request, *args, **kwargs)
