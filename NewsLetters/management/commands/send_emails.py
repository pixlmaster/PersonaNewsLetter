from concurrent.futures import ThreadPoolExecutor, as_completed
import cachetools
from django.core.management.base import BaseCommand
from NewsLetters.consts import SENDER_EMAIL, STR_EMAIL_SENT_SUCCESSFULLY, MAX_WORKERS_SEND_EMAIL
from NewsLetters.models import Content, Subscriber
from django.core.mail import send_mail
from django.utils import timezone
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Define the LRU cache
subscriber_cache = cachetools.LRUCache(maxsize=10000)


def send_newsletters(content, subscribers):
    for subscriber in subscribers:
        try:
            send_mail(
                f"Newsletter: {content.topic.name}",
                content.content_text,
                SENDER_EMAIL,
                [subscriber.email],
                fail_silently=True
            )
            logger.info(STR_EMAIL_SENT_SUCCESSFULLY.format(subscriber.email))
        except Exception as e:
            logger.error(f"Failed to send email to {subscriber.email}: {str(e)}")


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
        subscriber_cache.clear()
        self.stdout.write(self.style.SUCCESS('Starting processing'))

        with ThreadPoolExecutor(max_workers=MAX_WORKERS_SEND_EMAIL) as executor:
            futures = {}

            for content in contents:
                subscribers = subscriber_cache.get(content.topic)

                if not subscribers:
                    subscribers = list(Subscriber.objects.filter(topic=content.topic))
                    subscriber_cache[content.topic] = subscribers

                future = executor.submit(send_newsletters, content, subscribers)
                futures[future] = content

            for future in as_completed(futures):
                content = futures[future]
                try:
                    future.result()
                    content.delete()
                    logger.info(f"Content {content.content_text} processed and deleted")
                except Exception as e:
                    logger.error(f"Error processing content {content.content_text}: {str(e)}")

        self.stdout.write(self.style.SUCCESS('Successfully sent newsletter emails.'))
