from django.test import TestCase, Client
from django.contrib.messages import get_messages
from .views import *
from .models import *
from pengguna.models import *
from sarana_olahraga.models import *


class PenggunaTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user_konsumen = User.objects.create_user(
            email="konsumen@email.com",
            username="konsumen",
            password="konsumen",
        )
        self.konsumen = Konsumen_GOR.objects.create(
            user=self.user_konsumen, nama="konsumen", nomor_telepon="12345", status_loyalty="loyalty")

        self.user_pengurus = User.objects.create_user(
            email="pengurus@email.com",
            username="pengurus",
            password="pengurus",
        )
        self.pengurus = Pengurus_GOR.objects.create(
            user=self.user_pengurus, nama="pengurus", nomor_telepon="67890", akun_bank="0123124213")

    def test_getUserLogin(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_postUserLoginNone(self):
        self.client.login(username="konsumen", password="pengurus")
        data = {
            "username": "konsumen",
            "password": "pengurus"
        }
        response = self.client.post("/login/", data)
        messages = [m.message for m in get_messages(response.wsgi_request)]

        self.assertEqual(messages[0], 'Username atau Password salah')
        self.assertEqual(response.status_code, 200)

    def test_postUserLoginKonsumen(self):
        self.client.login(username="konsumen", password="pengurus")
        data = {
            "username": "konsumen",
            "password": "konsumen"
        }
        response = self.client.post("/login/", data)

        self.assertEqual(self.client.session['role'], 'KONSUMEN')
        self.assertEqual(response.status_code, 302)

    def test_postUserLoginPengurus(self):
        self.client.login(username="konsumen", password="pengurus")
        data = {
            "username": "pengurus",
            "password": "pengurus"
        }
        response = self.client.post("/login/", data)

        self.assertEqual(self.client.session['role'], 'PENGURUS')
        self.assertEqual(response.status_code, 302)

    def test_userLogout(self):
        self.client.login(username="konsumen", password="pengurus")
        data = {
            "username": "pengurus",
            "password": "pengurus"
        }
        self.client.post("/login/", data)
        response = self.client.get("/logout")

        self.assertEqual(response.status_code, 302)
