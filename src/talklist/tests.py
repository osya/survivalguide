import os

from django.conf import settings
from django.test import LiveServerTestCase, RequestFactory, TestCase
# Create your tests here.
from django.urls import reverse
from selenium.webdriver.phantomjs.webdriver import WebDriver

from factory_user import UserFactory, random_string_generator
from talklist.factories import TalkListFactory
from talklist.models import TalkList
from talklist.views import TalkListListView


class TalkLIstTests(TestCase):
    def test_talklist_create(self):
        TalkListFactory()
        self.assertEqual(1, TalkList.objects.count())


class TalkListListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_no_talklists_in_context(self):
        request = self.factory.get('/')
        request.user = UserFactory(password=random_string_generator())
        response = TalkListListView.as_view()(request)
        self.assertEqual(
            list(response.context_data['object_list']),
            [],
        )

    def test_talklists_in_context(self):
        request = self.factory.get('/')
        talklist = TalkListFactory()
        request.user = talklist.user
        response = TalkListListView.as_view()(request)
        self.assertEqual(
            list(response.context_data['object_list']),
            [talklist],
        )


class CreateTalkListIntegrationTest(LiveServerTestCase):
    selenium = None

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver(
            executable_path=os.path.join(
                os.path.dirname(settings.BASE_DIR), 'node_modules', 'phantomjs-prebuilt', 'lib', 'phantom', 'bin',
                'phantomjs')) if os.name == 'nt' else WebDriver()
        cls.password = random_string_generator()
        super(CreateTalkListIntegrationTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(CreateTalkListIntegrationTest, cls).tearDownClass()

    def setUp(self):
        # `user` creation placed in setUp() rather than setUpClass(). Because when `user` created in setUpClass then
        # `test_talklist_create` passed when executed separately, but failed when executed in batch
        # TODO: investigate this magic
        self.user = UserFactory(password=self.password)

    def test_talklist_list(self):
        response = self.client.get(reverse('talklists:list'))
        self.assertEqual(response.status_code, 200)

    def test_slash(self):
        response = self.client.get(reverse('home'))
        self.assertIn(response.status_code, (301, 302))

    def test_empty_create(self):
        response = self.client.get(reverse('talklists:create'))
        self.assertIn(response.status_code, (301, 302))

    def test_talklist_create(self):
        self.assertTrue(self.client.login(username=self.user.username, password=self.password))
        cookie = self.client.cookies.get(settings.SESSION_COOKIE_NAME)
        # Replace `localhost` to 127.0.0.1 due to the WinError 10054 according to the
        # https://stackoverflow.com/a/14491845/1360307
        self.selenium.get(f'{self.live_server_url}{reverse("talklists:create")}'.replace(
            'localhost', '127.0.0.1'))
        if cookie:
            self.selenium.add_cookie({
                'name': settings.SESSION_COOKIE_NAME,
                'value': cookie.value,
                'secure': False,
                'path': '/',
                'domain': '127.0.0.1'  # it is needed for PhantomJS due to the issue
                # "selenium.common.exceptions.WebDriverException: Message: 'phantomjs' executable needs to be in PATH"
            })
        self.selenium.refresh()  # need to update page for logged in user
        self.selenium.find_element_by_id('id_name').send_keys('raw name')
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertEqual(1, TalkList.objects.count())
        self.assertEqual('raw name', TalkList.objects.first().name)

# TODO: Selenium support for PhantomJS has been deprecated, please use headless versions of Chrome or Firefox instead
