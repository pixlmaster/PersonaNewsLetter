from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .ModelUtils.model_utils import handle_post_request
from .consts import STR_MESSAGE, STR_SUBSCRIBED_SUCCESSFULLY, JSON_EMAIL_KEY, JSON_TOPIC_KEY, JSON_CONTENT_TEXT_KEY, \
    JSON_SEND_TIME_KEY, STR_CONTENT_ADDED_SUCCESSFULLY, JSON_TOPIC_NAME_KEY
from .models import Subscriber, Content


@csrf_exempt
def add_subscriber(request):
    # create function for subscriber passed to the generic post request handler
    def create_subscriber(data, topic):
        # TODO : VALIDATE email

        subscriber = Subscriber.objects.create(email=data[JSON_EMAIL_KEY], topic=topic, topic_name=topic.name)
        return JsonResponse({ STR_MESSAGE: STR_SUBSCRIBED_SUCCESSFULLY, JSON_EMAIL_KEY: subscriber.email, JSON_TOPIC_KEY: topic.name}, status=201)

    return handle_post_request(request, create_subscriber)


@csrf_exempt
def add_content(request):
    # create function for content passed to the generic post request handler
    def create_content(data, topic):
        # TODO : VALIDATE CONTENT(SEND_TIME CANNOT BE IN PAST)
        content = Content.objects.create(
            content_text=data[JSON_CONTENT_TEXT_KEY],
            send_time=data[JSON_SEND_TIME_KEY],
            topic=topic
        )
        return JsonResponse({STR_MESSAGE: STR_CONTENT_ADDED_SUCCESSFULLY, JSON_CONTENT_TEXT_KEY: content.content_text, JSON_SEND_TIME_KEY: content.send_time,
                             JSON_TOPIC_NAME_KEY: topic.name}, status=201)

    return handle_post_request(request, create_content)
