from django.test import TestCase, Client
from .views import *
from .models import *
from pengguna.models import *
from sarana_olahraga.models import *

class ReservasiSaranaTest(TestCase):
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
        self.pengurus = Pengurus_GOR.objects.create(user=self.user_pengurus, nama="pengurus", nomor_telepon="67890", akun_bank="0123124213")

        self.jadwal_reservasi = Jadwal_Reservasi.objects.create(hari_buka="[]", jam_buka="[[]]", status_book="[[]]")

        self.sarana = Sarana.objects.create(ID_sarana="1", id_jadwal=self.jadwal_reservasi)

        self.sewa_sarana = Sewa_Sarana.objects.create(ID_sewa="1", konsumen=self.konsumen, pengurus=self.pengurus)

    def testCekRiwayatReservasi(self):
        self.client.login(username="konsumen", password="konsumen")
        response = self.client.get("/reservasi/riwayat-reservasi")
        self.assertEqual(response.status_code, 200)