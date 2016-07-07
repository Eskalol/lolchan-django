from django.http import Http404
from rest_framework import generics
from django.db.models import Q, FieldDoesNotExist

from lolchan.lolchan_api.comment import comment_serializers
from lolchan.lolchan_core.models import Comment
from lolchan.lolchan_api.permission import permission


class CommentViewList(generics.mixins.ListModelMixin,
                      generics.GenericAPIView):
    serializer_class = comment_serializers.CommentModelSerializer

    def __validate_order(self, order):
        if not order:
            return True
        try:
            Comment._meta.get_field_by_name(order[1:] if order[0] == '-' else order)
        except FieldDoesNotExist:
            return False
        return True

    def get_queryset(self):
        channel = self.request.query_params.get('channel', None)
        post = self.request.query_params.get('post', None)
        order = self.request.query_params.get('order', None)
        if not self.__validate_order(order):
            order = None
        queryset_list = Comment.objects.all()
        if channel:
            queryset_list = queryset_list.filter(post__channel__name=channel)
        if post:
            queryset_list = queryset_list.filter(post__title=post)
        if not queryset_list:
            raise Http404
        if order:
            return queryset_list.order_by(order)
        return queryset_list

    def get(self, request, *args, **kwargs):
        """
        Gets a list of comments

        channel filter - will match with name of the channel that
            the comments belongs to
        post filter - will match with title of the post that
            the comments belongs to
        order - the sorting order of the returned list
            you can sort by "text" and "publish_date" in ascending and descending order.

        ---
        parameters:
            - name: channel
              required: false
              paramType: query
              type: String
              description: name of channel
            - name: post
              required: false
              paramType: query
              type: String
              description: post title
            - name: order
              required: false
              paramType: query
              type: String
              description: sort order(text, publish_date)

        """
        return self.list(request, *args, **kwargs)


class CommentView(generics.mixins.DestroyModelMixin,
                  generics.mixins.CreateModelMixin,
                  generics.mixins.RetrieveModelMixin,
                  generics.GenericAPIView):
    serializer_class = comment_serializers.CommentModelSerializer
    permission_classes = (permission.CommentViewPermission, )

    def get_object(self):
        pk = self.request.query_params.get('id', None)
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
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
                  description: The id of a comment
            """
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates a comment


        ---
        parameters:
            - name: post
              required: true
              paramType: form
              type: int
              description: post id that the comment belongs to
            - name: text
              required: true
              paramType: form
              type: string
              description: comment text
        """
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        deletes a comment by id

        ---
        parameters:
            - name: id
              required: true
              paramType: query
              type: int
              description: The id of the comment to delete
        """
        return self.destroy(request, *args, **kwargs)