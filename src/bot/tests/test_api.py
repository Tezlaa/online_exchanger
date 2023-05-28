import datetime
import pytz

from django.test import TestCase
from django.conf import settings
from django.urls import reverse

from bot.models import Feedbacks


class TestApiFeedbacksTestCase(TestCase):
    def setUp(self) -> None:
        self.headers = {'token': settings.TOKEN_API}
        self.time_for_test = datetime.datetime.now(pytz.timezone('Europe/Kiev')
                                                   ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    def test_feedback_list(self):
        number_status_code = self.client.get(
            path=reverse('feedback_list'), headers=self.headers).status_code
        
        self.assertEqual(number_status_code, 200)
        
    def test_feedback_update(self):
        Feedbacks.objects.create(feedback_text='This is a test feedback!!')
    
        data = {
            'feedback_text': 'New text',
            'send': self.time_for_test
        }
        
        response_update = self.client.put(
            path=reverse('feedback_update', args=['1']),
            data=data,
            content_type='application/json',
            headers=self.headers,
        )

        self.assertEqual(response_update.status_code, 200)
        self.assertEqual(Feedbacks.objects.get(pk=1).feedback_text, 'New text')