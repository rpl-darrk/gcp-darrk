from django.test import LiveServerTestCase, TestCase, tag
from django.urls import reverse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth.models import User

class MainAuthenticateBeforeAccess(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="foo", password="bar")

@tag("functional")
class FunctionalTestCase(LiveServerTestCase):
    """Base class for functional test cases with selenium."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Change to another webdriver if desired (and update CI accordingly).
        options = webdriver.chrome.options.Options()
        # These options are needed for CI with Chromium.
        options.headless = True  # Disable GUI.
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.selenium = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


class MainTestCase(TestCase):
    def test_authenticate_response(self):
        self.client.login(username="foo", password="bar")
        response = self.client.get("/")
        assert(response.status_code.__eq__(200))
