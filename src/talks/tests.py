import random
import string

import factory
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client, LiveServerTestCase, RequestFactory, TestCase

from selenium.webdriver.chrome.webdriver import WebDriver
from talks.models import Talk, TalkList
from talks.views import TalkListListView


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'Agent %03d' % n)
    email = factory.LazyAttributeSequence(lambda o, n: f'{o.username}{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password')


class TalkListFactory(factory.DjangoModelFactory):
    class Meta:
        model = TalkList

    user = factory.SubFactory(UserFactory, password=random_string_generator())
    name = factory.Sequence(lambda n: 'TalkList %03d' % n)


class TalkFactory(factory.DjangoModelFactory):
    class Meta:
        model = Talk

    talk_list = factory.SubFactory(TalkListFactory)
    name = factory.Sequence(lambda n: 'Talk %03d' % n)


class TalkLIstTests(TestCase):
    def test_str(self):
        talk_list = TalkListFactory()
        self.assertEqual(str(talk_list), talk_list.name)


class TalkTests(TestCase):
    def test_str(self):
        talk = TalkFactory()
        self.assertEqual(str(talk), talk.name)


class TalkListListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_no_talk_lists_in_context(self):
        request = self.factory.get('/')
        request.user = UserFactory(password=random_string_generator())
        response = TalkListListView.as_view()(request)
        self.assertEquals(list(response.context_data['object_list']), [], )

    def test_talk_lists_in_context(self):
        request = self.factory.get('/')
        talk_list = TalkListFactory()
        request.user = talk_list.user
        response = TalkListListView.as_view()(request)
        self.assertEquals(list(response.context_data['object_list']), [talk_list], )


class CreateTalkListIntegrationTest(LiveServerTestCase):
    selenium = None

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.password = random_string_generator()
        cls.user = UserFactory(password=cls.password)
        cls.client = Client()
        super(CreateTalkListIntegrationTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(CreateTalkListIntegrationTest, cls).tearDownClass()

    def test_create_talk_list(self):
        self.assertTrue(self.client.login(username=self.user.username, password=self.password))
        cookie = self.client.cookies.get(settings.SESSION_COOKIE_NAME)
        # Replace `localhost` to 127.0.0.1 due to the WinError 10054 according to the
        # https://stackoverflow.com/a/14491845/1360307
        self.selenium.get(
            f'{self.live_server_url}{reverse("talks:talk_lists:create")}'.replace('localhost', '127.0.0.1'))
        if cookie:
            self.selenium.add_cookie({
                'name': settings.SESSION_COOKIE_NAME,
                'value': cookie.value,
                'secure': False,
                'path': '/'})
        self.selenium.refresh()  # need to update page for logged in user
        self.selenium.find_element_by_id('id_name').send_keys('MyName')
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertEqual(TalkList.objects.first().name, 'MyName')
