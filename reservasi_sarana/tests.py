from django.test import TestCase, Client
from .views import *
from .models import *
from pengguna.models import *
from sarana_olahraga.models import *


class ReservasiSaranaTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_verifikasiPembayaran(self):
        user_konsumen = User.objects.create_user(
            email="konsumen@email.com",
            username="konsumen",
            password="konsumen",
        )
        konsumen = Konsumen_GOR.objects.create(
            user=user_konsumen, nama="konsumen", nomor_telepon="12345", status_loyalty="loyalty")

        user_pengurus = User.objects.create_user(
            email="pengurus@email.com",
            username="pengurus",
            password="pengurus",
        )
        pengurus = Pengurus_GOR.objects.create(
            user=user_pengurus, nama="pengurus", nomor_telepon="67890", akun_bank="0123124213")

        gor = GOR.objects.create(ID_gor="1",  nama="nama",
                                 url_foto="url_foto", alamat="alamat", no_telepon="no_telepon", pengurus=pengurus)
        sarana = Sarana.objects.create(ID_sarana="1",  nama="nama",
                                       url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=gor)
        sewa_sarana = Sewa_Sarana.objects.create(
            ID_sewa="1", biaya=120000.00, sarana=sarana, status="Menunggu pembayaran", konsumen=konsumen, pengurus=pengurus)
        detail = Detail_Pembayaran.objects.create(
            sewa_sarana=sewa_sarana, status="Menunggu verifikasi bukti pembayaran")

        self.client.login(username="pengurus", password="pengurus")
        response = self.client.post("/reservasi/verifikasi-pembayaran/1")

        sewa_sarana = Sewa_Sarana.objects.get(ID_sewa="1")
        detail = Detail_Pembayaran.objects.get(sewa_sarana=sewa_sarana)

        self.assertEqual(sewa_sarana.status, "Berhasil dibayar")
        self.assertEqual(detail.status, "Pembayaran terverifikasi")
        self.assertEqual(response.status_code, 302)

    def test_pembatalanReservasiKonsumen(self):
        user_konsumen = User.objects.create_user(
            email="konsumen@email.com",
            username="konsumen",
            password="konsumen",
        )
        konsumen = Konsumen_GOR.objects.create(
            user=user_konsumen, nama="konsumen", nomor_telepon="12345", status_loyalty="loyalty")

        user_pengurus = User.objects.create_user(
            email="pengurus@email.com",
            username="pengurus",
            password="pengurus",
        )
        pengurus = Pengurus_GOR.objects.create(
            user=user_pengurus, nama="pengurus", nomor_telepon="67890", akun_bank="0123124213")

        gor = GOR.objects.create(ID_gor="1",  nama="nama",
                                 url_foto="url_foto", alamat="alamat", no_telepon="no_telepon", pengurus=pengurus)
        sarana = Sarana.objects.create(ID_sarana="1",  nama="nama",
                                       url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=gor)
        sewa_sarana = Sewa_Sarana.objects.create(
            ID_sewa="1", biaya=120000.00, sarana=sarana, status="Berhasil dibayar", konsumen=konsumen, pengurus=pengurus)

        self.client.login(username="konsumen", password="konsumen")
        response = self.client.post("/reservasi/pembatalan/1")

        pembatalan, created = Pembatalan_Sewa_Sarana.objects.get_or_create(
            sewa_sarana=sewa_sarana)
        verifikasi, created = Verifikasi_Pembatalan.objects.get_or_create(
            pembatalan=pembatalan)

        self.assertEqual(verifikasi.status, "Pembatalan diajukan")
        self.assertEqual(response.status_code, 302)

    def test_pembatalanReservasiPengurus(self):
        user_konsumen = User.objects.create_user(
            email="konsumen@email.com",
            username="konsumen",
            password="konsumen",
        )
        konsumen = Konsumen_GOR.objects.create(
            user=user_konsumen, nama="konsumen", nomor_telepon="12345", status_loyalty="loyalty")

        user_pengurus = User.objects.create_user(
            email="pengurus@email.com",
            username="pengurus",
            password="pengurus",
        )
        pengurus = Pengurus_GOR.objects.create(
            user=user_pengurus, nama="pengurus", nomor_telepon="67890", akun_bank="0123124213")

        gor = GOR.objects.create(ID_gor="1",  nama="nama",
                                 url_foto="url_foto", alamat="alamat", no_telepon="no_telepon", pengurus=pengurus)
        sarana = Sarana.objects.create(ID_sarana="1",  nama="nama",
                                       url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=gor)
        sewa_sarana = Sewa_Sarana.objects.create(
            ID_sewa="1", biaya=120000.00, sarana=sarana, status="Berhasil dibayar", konsumen=konsumen, pengurus=pengurus)

        self.client.login(username="pengurus", password="pengurus")
        response = self.client.post("/reservasi/pembatalan/1")

        sewa_sarana = Sewa_Sarana.objects.get(ID_sewa="1")
        pembatalan, created = Pembatalan_Sewa_Sarana.objects.get_or_create(
            sewa_sarana=sewa_sarana)
        verifikasi, created = Verifikasi_Pembatalan.objects.get_or_create(
            pembatalan=pembatalan)

        self.assertEqual(sewa_sarana.status, "Batal")
        self.assertEqual(verifikasi.status, "Pembatalan terverifikasi")
        self.assertEqual(response.status_code, 302)

    def test_verifikasiPembatalan(self):
        user_konsumen = User.objects.create_user(
            email="konsumen@email.com",
            username="konsumen",
            password="konsumen",
        )
        konsumen = Konsumen_GOR.objects.create(
            user=user_konsumen, nama="konsumen", nomor_telepon="12345", status_loyalty="loyalty")

        user_pengurus = User.objects.create_user(
            email="pengurus@email.com",
            username="pengurus",
            password="pengurus",
        )
        pengurus = Pengurus_GOR.objects.create(
            user=user_pengurus, nama="pengurus", nomor_telepon="67890", akun_bank="0123124213")

        gor = GOR.objects.create(ID_gor="1",  nama="nama",
                                 url_foto="url_foto", alamat="alamat", no_telepon="no_telepon", pengurus=pengurus)
        sarana = Sarana.objects.create(ID_sarana="1",  nama="nama",
                                       url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=gor)
        sewa_sarana = Sewa_Sarana.objects.create(
            ID_sewa="1", biaya=120000.00, sarana=sarana, status="Berhasil dibayar", konsumen=konsumen, pengurus=pengurus)
        pembatalan = Pembatalan_Sewa_Sarana.objects.create(
            ID_pembatalan="1", pembatal=konsumen, sewa_sarana=sewa_sarana)
        verifikasi = Verifikasi_Pembatalan.objects.create(
            pembatalan=pembatalan, pengurus=pengurus)

        self.client.login(username="pengurus", password="pengurus")
        response = self.client.post("/reservasi/verifikasi-pembatalan/1")

        sewa_sarana = Sewa_Sarana.objects.get(ID_sewa="1")
        verifikasi = Verifikasi_Pembatalan.objects.get(pembatalan=pembatalan)

        self.assertEqual(sewa_sarana.status, "Batal")
        self.assertEqual(verifikasi.status, "Pembatalan terverifikasi")
        self.assertEqual(response.status_code, 302)
