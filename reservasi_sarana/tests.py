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
        self.pengurus = Pengurus_GOR.objects.create(
            user=self.user_pengurus, nama="pengurus", nomor_telepon="67890", akun_bank="0123124213")

        self.gor = GOR.objects.create(ID_gor="1",  nama="nama",
                                      url_foto="url_foto", alamat="alamat", nomor_telepon="nomor_telepon", pengurus=self.pengurus)

        self.jadwal_reservasi = Jadwal_Reservasi.objects.create(
            ID_jadwal='1',
            hari_buka=[True, True, True, True, True, False, False],
            jam_buka=[['10.00', '11.00'], ['11.00', '12.00']],
            status_book=[[True, True, True, True, True, True, True],
                         [True, True, True, True, True, True, True]]
        )

        self.sarana = Sarana.objects.create(ID_sarana="1",  nama="nama",
                                            url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=self.gor, id_jadwal_reservasi=self.jadwal_reservasi)

        self.sewa_sarana = Sewa_Sarana.objects.create(
            ID_sewa="1", biaya=120000.00, sarana=self.sarana, konsumen=self.konsumen, pengurus=self.pengurus, jam_booking=["10.00-11.00", 0])

    def test_verifikasiPembayaran(self):
        self.detail = Detail_Pembayaran.objects.create(
            sewa_sarana=self.sewa_sarana)

        data = {
            'ID_sewa': 1
        }

        self.client.login(username="pengurus", password="pengurus")
        response = self.client.post("/reservasi/verifikasi-pembayaran", data)

        self.sewa_sarana = Sewa_Sarana.objects.get(ID_sewa="1")
        self.detail = Detail_Pembayaran.objects.get(
            sewa_sarana=self.sewa_sarana)

        self.assertEqual(self.sewa_sarana.status,
                         str(Status_Sewa_Sarana.PAID))
        self.assertEqual(self.detail.status, str(
            Status_Detail_Pembayaran.VERIFIED))
        self.assertEqual(response.status_code, 302)

    def test_pembatalanReservasiPengurus(self):
        data = {
            'ID_sewa': 1
        }
        self.client.login(username="pengurus", password="pengurus")
        response = self.client.post("/reservasi/pembatalan", data)

        self.sewa_sarana = Sewa_Sarana.objects.get(ID_sewa="1")
        self.pembatalan, created = Pembatalan_Sewa_Sarana.objects.get_or_create(
            sewa_sarana=self.sewa_sarana)
        self.verifikasi, created = Verifikasi_Pembatalan.objects.get_or_create(
            pembatalan=self.pembatalan)

        self.assertEqual(self.sewa_sarana.status,
                         str(Status_Sewa_Sarana.CANCELLED))
        self.assertEqual(self.verifikasi.status,
                         str(Status_Verifikasi_Pembatalan.VERIFIED))
        self.assertEqual(response.status_code, 302)

    def test_pembatalanReservasiKonsumen(self):
        data = {
            'ID_sewa': 1
        }
        self.client.login(username="konsumen", password="konsumen")
        response = self.client.post("/reservasi/pembatalan", data)

        self.pembatalan, created = Pembatalan_Sewa_Sarana.objects.get_or_create(
            sewa_sarana=self.sewa_sarana)
        self.verifikasi, created = Verifikasi_Pembatalan.objects.get_or_create(
            pembatalan=self.pembatalan)

        self.assertEqual(self.verifikasi.status,
                         str(Status_Verifikasi_Pembatalan.SUBMITTED))
        self.assertEqual(response.status_code, 302)

    def test_verifikasiPembatalan(self):
        self.pembatalan = Pembatalan_Sewa_Sarana.objects.create(
            pembatal=self.konsumen, sewa_sarana=self.sewa_sarana)
        self.verifikasi = Verifikasi_Pembatalan.objects.create(
            pembatalan=self.pembatalan, pengurus=self.pengurus)

        data = {
            'ID_sewa': 1
        }
        self.client.login(username="pengurus", password="pengurus")
        response = self.client.post("/reservasi/verifikasi-pembatalan", data)

        self.sewa_sarana = Sewa_Sarana.objects.get(ID_sewa="1")
        self.verifikasi = Verifikasi_Pembatalan.objects.get(
            pembatalan=self.pembatalan)

        self.assertEqual(self.sewa_sarana.status,
                         str(Status_Sewa_Sarana.CANCELLED))
        self.assertEqual(self.verifikasi.status,
                         str(Status_Verifikasi_Pembatalan.VERIFIED))
        self.assertEqual(response.status_code, 302)

    def test_selesaikanReservasi(self):
        data = {
            'ID_sewa': 1
        }
        self.client.login(username="pengurus", password="pengurus")
        response = self.client.post("/reservasi/selesai", data)

        self.sewa_sarana = Sewa_Sarana.objects.get(ID_sewa="1")

        self.assertEqual(self.sewa_sarana.status,
                         str(Status_Sewa_Sarana.DONE))
        self.assertEqual(response.status_code, 302)

    def test_not_authenticated_response(self):
        response = self.client.post(
            "/jadwal/%s/%s/reservasi/%s" % ("1", "1", "1|10.00|11.00"))
        self.assertEqual(response.status_code, 302)

    def test_get_method_response(self):
        self.client.login(username="konsumen", password="konsumen")
        response = self.client.get(
            "/jadwal/%s/%s/reservasi/%s" % ("1", "1", "1|10.00|11.00"))
        self.assertEqual(response.status_code, 404)
