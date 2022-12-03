from django.test import TestCase
from django.contrib.auth.models import User

class MainAuthenticateBeforeAccess(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="foo", password="bar")

    def test_authenticate_response(self):
        self.client.login(username="foo", password="bar")
        response = self.client.get("/")
        assert(response.status_code.__eq__(200))