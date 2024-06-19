import cachetools
from django.core.management.base import BaseCommand

from NewsLetters.consts import SENDER_EMAIL, STR_EMAIL_SENT_SUCCESSFULLY
from NewsLetters.models import Content, Subscriber
from django.core.mail import send_mail
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)


subscriber_cache = cachetools.LRUCache(maxsize=10000)

class Command(BaseCommand):
    """
    Custom Django management command to send scheduled newsletter emails.

    Retrieves newsletter content scheduled for sending, iterates
    through each content to send emails to subscribers of its topic,
    and deletes the sent content after sending the emails.
    """

    help = 'Send scheduled newsletter emails'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        contents = Content.objects.filter(send_time__lte=now)
        # clear the cache, it's going to serve as a temp cache to save us DB calls
        subscriber_cache.clear()
        # foe each content
        for content in contents:
            # try to get from cache
            subscribers = subscriber_cache.get(content.topic)
            # if not present in cache ,find out which subscribers do we need to send data to from db
            if not subscribers:
                subscribers = Subscriber.objects.filter(topic=content.topic)
                subscriber_cache[content.topic] = subscribers
            # TODO: Implement multi threading for each subscriber list
            for subscriber in subscribers:
                send_mail(
                    f"Newsletter: {content.topic.name}",
                    content.content_text,
                    SENDER_EMAIL,
                    [subscriber.email],
                    fail_silently= True
                )
                logger.debug(STR_EMAIL_SENT_SUCCESSFULLY.format(subscriber.email))
            content.delete()
