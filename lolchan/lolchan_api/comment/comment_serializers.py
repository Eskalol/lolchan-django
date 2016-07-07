from rest_framework import serializers
from lolchan.lolchan_core.models import Comment


class CommentModelSerializer(serializers.ModelSerializer):
    publish_date = serializers.SerializerMethodField('get_publishdate')

    class Meta:
        model = Comment
        fields = ['post', 'text', 'publish_date']

    def get_publishdate(self, instance):
        return instance.publish_date.isoformat()