from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Subscriber, Content, Topic
import json


@csrf_exempt
def add_subscriber(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        topic = Topic.objects.get(name=data['topic'])
        # TODO handle topic not exist exception
        subscriber = Subscriber.objects.create(email=data['email'], topic=topic)
        # TODO handle duplicate entry exception
        return JsonResponse({'id': subscriber.id, 'email': subscriber.email, 'topic': topic.name})


@csrf_exempt
def add_content(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        topic = Topic.objects.get(name=data['topic'])
        # TODO handle topic not exist exception
        content = Content.objects.create(content_text=data['content_text'], send_time=data['send_time'], topic=topic)
        return JsonResponse({'id': content.id, 'content_text': content.content_text, 'send_time': content.send_time,
                             'topic': topic.name})
