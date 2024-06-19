import logging
import threading

from django.core.management import call_command
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .ModelUtils.model_utils import handle_post_request
from .consts import STR_MESSAGE, STR_SUBSCRIBED_SUCCESSFULLY, JSON_EMAIL_KEY, JSON_TOPIC_KEY, JSON_CONTENT_TEXT_KEY, \
    JSON_SEND_TIME_KEY, STR_CONTENT_ADDED_SUCCESSFULLY, JSON_TOPIC_NAME_KEY, STR_STATUS, STR_SUCCESS, STR_ERROR, \
    ERROR_ONLY_POST_ALLOWED, STR_NEWSLETTER_TASK_TRIGGERED, STR_NEWSLETTER_TASK_ERROR
from .models import Subscriber, Content

logger = logging.getLogger(__name__)


@csrf_exempt
def add_subscriber(request):
    # create function for subscriber passed to the generic post request handler
    def create_subscriber(data, topic):
        # TODO : VALIDATE email

        subscriber = Subscriber.objects.create(email=data[JSON_EMAIL_KEY], topic=topic, topic_name=topic.name)
        return JsonResponse({ STR_MESSAGE: STR_SUBSCRIBED_SUCCESSFULLY, JSON_EMAIL_KEY: subscriber.email,
                              JSON_TOPIC_KEY: topic.name}, status=201)

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
                             JSON_TOPIC_NAME_KEY: topic.name}, status=201)

    return handle_post_request(request, create_content)


@csrf_exempt
def trigger_send_newsletters(request):
    if request.method == 'POST':
        try:
            def execute_send_emails():
                try:
                    call_command('send_emails')  # Replace with your actual management command
                except Exception as e:
                    # Handle exceptions here if needed
                    logger.error(f"{STR_NEWSLETTER_TASK_ERROR} {str(e)}")

            # Create and start a new thread to send emails async
            thread = threading.Thread(target=execute_send_emails)
            thread.start()
            # Return the response immediately that the task has started
            return JsonResponse({STR_STATUS: STR_SUCCESS, STR_MESSAGE: STR_NEWSLETTER_TASK_TRIGGERED},
                                status=200)
        except Exception as e:
            return JsonResponse({STR_STATUS: STR_ERROR, STR_MESSAGE: str(e)}, status=500)
    else:
        return JsonResponse({STR_STATUS: STR_ERROR, STR_MESSAGE: ERROR_ONLY_POST_ALLOWED}, status=405)