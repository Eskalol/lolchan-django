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
        """
            Since anonymous users should be able to vote a post, they should only
            be allowed to change the "votes" field, and to prevent users from
            voting a post by 1000 up or down in one request we'll only change "votes"
            by 1
        """
        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        votes = validated_data.get('votes', self.instance.votes)
        if votes > 0:
            self.instance.votes += 1
        elif votes < 0:
            self.instance.votes -= 1
        else:
            self.instance.vote = self.instance.votes
        instance.save()
        return instance

    def create(self, validated_data):
        """
            When creating a post we are not allowed to give yourself 1000 votes,
            therefore votes is set to 0

        """
        validated_data['votes'] = 0
        return super(PostModelSerializer, self).create(validated_data)
