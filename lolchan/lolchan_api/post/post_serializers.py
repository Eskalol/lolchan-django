from rest_framework import serializers
from lolchan.lolchan_core.models import Post


class VoteSerializer(serializers.Serializer):
    vote = serializers.CharField(max_length=10, required='True')
    pk = serializers.IntegerField(read_only=True)

    def __init__(self, post, **kwargs):
        super(VoteSerializer, self).__init__(**kwargs)
        self.post = post

    def update(self, instance, validated_data):
        if instance.vote == 'vote-up':
            new_votes = self.votes + 1
        elif instance.vote == 'vote-down':
            new_votes = self.votes - 1
        else:
            new_votes = self.votes
        instance.votes = validated_data('votes', new_votes)
        instance.save()
        return instance

    def validate(self, attrs):
        if attrs['vote'] not in ['vote-up', 'vote-down']:
            return serializers.ValidationError('ote can either be vote-up or vote-down')
        return attrs

