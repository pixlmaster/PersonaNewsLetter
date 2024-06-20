from django.test import TestCase, Client
from django.urls import reverse
from .models import Subscriber, Topic


class AddSubscriberViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(name='Tech News')
        self.url = reverse('add_subscriber')

    def test_add_subscriber_success(self):
        data = {
            'email': 'test@example.com',
            'topic': self.topic.name
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subscriber.objects.count(), 1)

    def test_add_subscriber_invalid_data(self):
        data = {
            'email': '',
            'topic': self.topic.id
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
