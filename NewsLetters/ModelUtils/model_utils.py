import json
from sqlite3 import IntegrityError

from django.http import JsonResponse

from NewsLetters.consts import ERROR_INVALID_JSON, ERROR_TOPIC_NOT_EXIST, ERROR_MISSING_FIELD, ERROR_DATA_INTEGRITY, \
    ERROR_ONLY_POST_ALLOWED, METHOD_POST, JSON_TOPIC_KEY, STR_ERROR, RESPONSE_BAD_REQUEST_RESPONSE_BAD_REQUEST_400, \
    RESPONSE_BAD_REQUEST_400, RESPONSE_INTERNAL_SERVER_ERROR_500, RESPONSE_METHOD_NOT_ALLOWED_405
from NewsLetters.models import Topic


def parse_request_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        raise ValueError(ERROR_INVALID_JSON)


def get_topic_by_name(topic_name):
    try:
        return Topic.objects.get(name=topic_name)
    except Topic.DoesNotExist:
        raise ValueError(ERROR_TOPIC_NOT_EXIST.format(topic_name))


def handle_post_request(request, create_function):
    if request.method == METHOD_POST:
        try:
            data = parse_request_body(request)
            topic = get_topic_by_name(data[JSON_TOPIC_KEY])
            return create_function(data, topic)
        except KeyError as e:
            return JsonResponse({STR_ERROR: ERROR_MISSING_FIELD.format(e)}, status=RESPONSE_BAD_REQUEST_400)
        except ValueError as e:
            return JsonResponse({STR_ERROR: str(e)}, status=RESPONSE_BAD_REQUEST_400)
        except IntegrityError:
            return JsonResponse({STR_ERROR: ERROR_DATA_INTEGRITY}, status=RESPONSE_BAD_REQUEST_400)
        except Exception as e:
            return JsonResponse({STR_ERROR: str(e)}, status=RESPONSE_INTERNAL_SERVER_ERROR_500)
    else:
        return JsonResponse({STR_ERROR: ERROR_ONLY_POST_ALLOWED}, status=RESPONSE_METHOD_NOT_ALLOWED_405)
