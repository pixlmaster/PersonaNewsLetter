from django.core.management.base import BaseCommand
from NewsLetters.models import Content, Subscriber
from django.core.mail import send_mail
from django.utils import timezone


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
        for content in contents:
            subscribers = Subscriber.objects.filter(topic=content.topic)
            for subscriber in subscribers:
                # TODO : Configure sending email
                pass
                # send_mail(
                #     f"Newsletter: {content.topic.name}",
                #     content.content_text,
                #     'xyzl@example.com',
                #     [subscriber.email],
                # )
            content.delete()
