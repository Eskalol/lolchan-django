from rest_framework import serializers
from lolchan.lolchan_core.models import Post


class PostModelSerializer(serializers.ModelSerializer):
    publish_date = serializers.SerializerMethodField('get_publishdate')

    class Meta:
        model = Post
        fields = ['title', 'text', 'votes', 'publish_date', 'channel']

    def get_publishdate(self, instance):
        return instance.publish_date.isoformat()

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes('update', self, validated_data)

        self.instance.votes = validated_data.get('votes', self.instance.votes)
        instance.save()
