from django.test import TestCase, Client
from ..models import Jadwal_Reservasi
from django.contrib.auth.models import User
import json


class ReservasiJadwalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="foo", password="bar")
        self.jadwal_reservasi = Jadwal_Reservasi.objects.create(
            ID_jadwal='0', jam_buka=json.loads('[["10.00", "11.00"], ["11.00", "12.00"]]'),)

    def test_reserve_unauthenticated_user_redirect(self):
        response = self.client.post("/reservasi/0/")
        assert (response.status_code.__eq__(302))

    def test_get_reservation_instead_of_post(self):
        self.client.login(username="foo", password="bar")

        response = self.client.get("/reservasi/0/")
        assert (response.status_code.__eq__(404))

    def test_status_after_reservation(self):
        # assert (self.jadwal_reservasi.status.__eq__(Status_Reservasi.VACANT))
        self.client.login(username="foo", password="bar")

        response = self.client.post("/reservasi/0/")
        assert (response.status_code.__eq__(200))
