from django.test import TestCase

from talk.factories import TalkFactory
from talk.models import Talk


class TalkTests(TestCase):
    def test_talk_create(self):
        TalkFactory()
        self.assertEqual(1, Talk.objects.count())
