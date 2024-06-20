import json
import logging
import threading

from django.core.management import call_command
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .ModelUtils.model_utils import handle_post_request, parse_request_body
from .consts import STR_MESSAGE, STR_SUBSCRIBED_SUCCESSFULLY, JSON_EMAIL_KEY, JSON_TOPIC_KEY, JSON_CONTENT_TEXT_KEY, \
    JSON_SEND_TIME_KEY, STR_CONTENT_ADDED_SUCCESSFULLY, JSON_TOPIC_NAME_KEY, STR_STATUS, STR_SUCCESS, STR_ERROR, \
    ERROR_ONLY_POST_ALLOWED, STR_NEWSLETTER_TASK_TRIGGERED, STR_NEWSLETTER_TASK_ERROR, METHOD_DELETE, \
    ERROR_ONLY_DELETE_ALLOWED, METHOD_POST, STR_UNSUBSCRIBED_SUCCESSFULLY, STR_EMAIL_NOT_SUBSCRIBED, \
    STR_FAILED_TO_UNSUBSCRIBE, RESPONSE_CREATED_201, RESPONSE_NOT_FOUND_404, RESPONSE_OK_200, \
    RESPONSE_INTERNAL_SERVER_ERROR_500, RESPONSE_METHOD_NOT_ALLOWED_405, ERROR_INVALID_JSON, \
    RESPONSE_BAD_REQUEST_400, JSON_TOPICS_KEY, STR_ID, STR_NAME
from .models import Subscriber, Content, Topic

logger = logging.getLogger(__name__)


@csrf_exempt
def add_subscriber(request):
    # create function for subscriber passed to the generic post request handler
    def create_subscriber(data, topic):
        # TODO : VALIDATE email

        subscriber = Subscriber.objects.create(email=data[JSON_EMAIL_KEY], topic=topic, topic_name=topic.name)
        return JsonResponse({STR_MESSAGE: STR_SUBSCRIBED_SUCCESSFULLY, JSON_EMAIL_KEY: subscriber.email,
                             JSON_TOPIC_KEY: topic.name}, status=RESPONSE_CREATED_201)

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
        return JsonResponse({STR_MESSAGE: STR_CONTENT_ADDED_SUCCESSFULLY, JSON_CONTENT_TEXT_KEY: content.content_text,
                             JSON_SEND_TIME_KEY: content.send_time,
                             JSON_TOPIC_NAME_KEY: topic.name}, status=RESPONSE_CREATED_201)

    return handle_post_request(request, create_content)


@csrf_exempt
def remove_subscriber(request):
    if request.method == METHOD_DELETE:
        try:
            data = parse_request_body(request)
            email = data.get(JSON_EMAIL_KEY)
            topic_name = data.get(JSON_TOPIC_NAME_KEY)
            subscriber = get_object_or_404(Subscriber, email=email, topic_name=topic_name)
            subscriber.delete()
            return JsonResponse({
                STR_MESSAGE: f'{STR_UNSUBSCRIBED_SUCCESSFULLY} {email}'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                STR_ERROR: ERROR_INVALID_JSON
            }, status=RESPONSE_BAD_REQUEST_400)
        except Subscriber.DoesNotExist:
            return JsonResponse({
                STR_ERROR: f'{STR_EMAIL_NOT_SUBSCRIBED} {email}'
            }, status=RESPONSE_NOT_FOUND_404)
        except Exception as e:
            return JsonResponse({
                STR_ERROR: f'{STR_FAILED_TO_UNSUBSCRIBE} {str(e)}'
            }, status=RESPONSE_INTERNAL_SERVER_ERROR_500)
    else:
        return JsonResponse({STR_ERROR: ERROR_ONLY_DELETE_ALLOWED}, status=405)


@csrf_exempt
def trigger_send_newsletters(request):
    if request.method == METHOD_POST:
        try:
            def execute_send_emails():
                try:
                    call_command('send_emails')
                except Exception as e:
                    # Handle exceptions here if needed
                    logger.error(f"{STR_NEWSLETTER_TASK_ERROR} {str(e)}")

            # Create and start a new thread to send emails async
            thread = threading.Thread(target=execute_send_emails)
            thread.start()
            # Return the response immediately that the task has started
            return JsonResponse({STR_STATUS: STR_SUCCESS, STR_MESSAGE: STR_NEWSLETTER_TASK_TRIGGERED},
                                status=RESPONSE_OK_200)
        except Exception as e:
            return JsonResponse({STR_STATUS: STR_ERROR, STR_MESSAGE: str(e)}, status=RESPONSE_INTERNAL_SERVER_ERROR_500)
    else:
        return JsonResponse({STR_STATUS: STR_ERROR, STR_MESSAGE: ERROR_ONLY_POST_ALLOWED}, status=RESPONSE_METHOD_NOT_ALLOWED_405)


def get_all_topics(request):
    try:
        topics = Topic.objects.all().values(STR_ID, STR_NAME)
        topics_list = list(topics)
        return JsonResponse({JSON_TOPICS_KEY: topics_list}, status=RESPONSE_OK_200)
    except Exception as e:
        return JsonResponse({STR_ERROR: str(e)}, status=RESPONSE_INTERNAL_SERVER_ERROR_500)