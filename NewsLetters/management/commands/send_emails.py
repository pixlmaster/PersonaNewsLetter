from concurrent.futures import ThreadPoolExecutor, as_completed

import cachetools
from django.core.management.base import BaseCommand

from NewsLetters.consts import SENDER_EMAIL, STR_EMAIL_SENT_SUCCESSFULLY, MAX_WORKERS_SEND_EMAIL
from NewsLetters.models import Content, Subscriber
from django.core.mail import send_mail
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)


subscriber_cache = cachetools.LRUCache(maxsize=10000)


def send_newsletters(content, subscribers):
    for subscriber in subscribers:
        try:
            send_mail(
                f"Newsletter: {content.topic.name}",
                content.content_text,
                SENDER_EMAIL,
                [subscriber.email],
                fail_silently=False
            )
            logger.info("mail sent to " + subscriber.email)
        except Exception as e:
            logger.error(f"Failed to send email to {subscriber.email}: {str(e)}")


class Command(BaseCommand):
    """
    Custom Django management command to send scheduled newsletter emails.

    Retrieves newsletter content scheduled for sending, iterates
    through each content to send emails to subscribers of its topic,
    and deletes the sent content after sending the emails.
    Since the content for each subscriber list is the same, we can easily implment
    multithreading to process each list of subscribers separately
    """

    help = 'Send scheduled newsletter emails'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        contents = Content.objects.filter()
        # clear the cache, it's going to serve as a temp cache to save us DB calls
        subscriber_cache.clear()
        self.stdout.write(self.style.SUCCESS('Starting processing'))

        logger.info("outside thread pool")
    # Create a thread pool executor
        with ThreadPoolExecutor(max_workers=MAX_WORKERS_SEND_EMAIL) as executor:
            logger.info("inside thread pool")
            # Dictionary to hold futures
            futures = {}
            # For each content
            logger.info(len(contents))
            for content in contents:
                logger.info(content.topic)
                # Try to get from cache
                subscribers = subscriber_cache.get(content.topic)
                # If not present in cache, find out which subscribers we need to send data to from DB
                if not subscribers:
                    subscribers = list(Subscriber.objects.filter(topic=content.topic))
                    subscriber_cache[content.topic] = subscribers
                logger.info(subscribers)
                # Submit each list of subscribers to the executor
                future = executor.submit(send_newsletters, content, subscribers)
                futures[future] = content
            logger.info("futures populated ")
            logger.info(futures)
            # Process the results as they complete
            for future in as_completed(futures):
                content = futures[future]
                try:
                    future.result()
                    # Delete content from the DB after sending all emails
                    content.delete()
                except Exception as e:
                    logger.error(f"Error processing content {content.id}: {str(e)}")
            logger.info("futures processed")
        self.stdout.write(self.style.SUCCESS('Successfully sent newsletter emails.'))
