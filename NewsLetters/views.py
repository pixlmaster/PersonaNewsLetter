from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import json
from NewsLetters.models import Topic, Content
from NewsLetters.serializers import SubscriberSerializer, ContentSerializer


@csrf_exempt
@swagger_auto_schema(method='post', request_body=SubscriberSerializer)
@api_view(['POST'])
def add_subscriber(request):
    serializer = SubscriberSerializer(data=request.data)
    if serializer.is_valid():
        subscriber = serializer.save()
        return JsonResponse({'id': subscriber.id, 'email': subscriber.email, 'topic': serializer.validated_data['topic'].name})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@swagger_auto_schema(method='post', request_body=ContentSerializer)
@api_view(['POST'])
def add_content(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        topic = Topic.objects.get(name=data['topic'])
        # TODO handle topic not exist exception
        content = Content.objects.create(content_text=data['content_text'], send_time=data['send_time'], topic=topic)
        return JsonResponse({'id': content.id, 'content_text': content.content_text, 'send_time': content.send_time,
                             'topic': topic.name})
