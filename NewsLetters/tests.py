import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .consts import JSON_CONTENT_TEXT_KEY, JSON_SEND_TIME_KEY, JSON_TOPIC_KEY, JSON_EMAIL_KEY
from .models import Subscriber, Topic, Content


class AddSubscriberViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(name='Tech News')
        self.url = reverse('add_subscriber')

    def test_add_subscriber_success(self):
        data = {
            JSON_EMAIL_KEY: 'test@example.com',
            JSON_TOPIC_KEY: self.topic.name
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subscriber.objects.count(), 1)

    def test_add_subscriber_invalid_data(self):
        data = {
            JSON_EMAIL_KEY: '',
            JSON_TOPIC_KEY: self.topic.id
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)


class AddContentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(name='Tech News')
        self.url = reverse('add_content')

    def test_add_content_success(self):
        data = {
            JSON_CONTENT_TEXT_KEY: 'New Tech Content',
            JSON_SEND_TIME_KEY: (timezone.now() + datetime.timedelta(days=1)).isoformat(),
            JSON_TOPIC_KEY: self.topic.name
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Content.objects.count(), 1)


class TriggerSendNewslettersViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('trigger_send_newsletters')

    def test_trigger_send_newsletters_success(self):
        response = self.client.post(self.url, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_trigger_send_newsletters_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)


class GetAllTopicsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('get_all_topics')
        self.topic1 = Topic.objects.create(name='Tech News')
        self.topic2 = Topic.objects.create(name='Health News')

    def test_get_all_topics_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['topics']), 2)
