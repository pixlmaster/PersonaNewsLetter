# serializers.py

from rest_framework import serializers
from .models import Subscriber, Topic, Content


def validate_topic(value):
    try:
        topic = Topic.objects.get(name=value)
    except Topic.DoesNotExist:
        raise serializers.ValidationError(f'Topic "{value}" does not exist.')
    return topic


class SubscriberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    topic = serializers.CharField()

    def create(self, validated_data):
        return Subscriber.objects.create(**validated_data)


class ContentSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(write_only=True)

    class Meta:
        model = Content
        fields = ['content_text', 'send_time', 'topic_name']

    def create(self, validated_data):
        topic = validated_data.pop('topic_name')
        validated_data['topic'] = topic
        return Content.objects.create(**validated_data)
