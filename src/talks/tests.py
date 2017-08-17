from django.test import TestCase
from talks.models import TalkList, Talk


class TalkListTests(TestCase):
    def test_str(self):
        t = TalkList(name='MyName')
        self.assertEqual(str(t), 'MyName')


class TalkTests(TestCase):
    def test_str(self):
        t = Talk(name='MyName')
        self.assertEqual(str(t), 'MyName')
