from rest_framework import serializers

from lolchan.lolchan_core.models import Channel


class Serializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ['id', 'slug', 'name', 'description']

    def create(self, validated_data):
        return Channel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

