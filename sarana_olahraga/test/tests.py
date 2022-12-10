from django.test import TestCase, Client
from pengguna.models import *
from sarana_olahraga.models import *
from sarana_olahraga.view.views import *


class SaranaOlahragaTest(TestCase):
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
                                      url_foto="url_foto", alamat="alamat", nomor_telepon="no_telepon", pengurus=self.pengurus)

        self.jadwal_1 = initTabelJadwal()

        self.jadwal_2 = initTabelJadwal()

        self.sarana = Sarana.objects.create(ID_sarana="1",  nama="nama",
                                            url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=self.gor, id_jadwal_reservasi=self.jadwal_1)
        self.sarana_2 = Sarana.objects.create(ID_sarana="2",  nama="nama",
                                              url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=self.gor, id_jadwal_reservasi=self.jadwal_2)

    def testInitTabelJadwalCreateNewInstance(self):
        hari_buka = []
        jam_buka = [[]]
        status_book = [[False for i in range(
            len(hari_buka))] for i in range(len(jam_buka))]

        new_jadwal1 = Jadwal_Reservasi(
            hari_buka=JSONEncoder().encode(hari_buka),
            jam_buka=JSONEncoder().encode(jam_buka),
            status_book=JSONEncoder().encode(status_book)
        )

        new_jadwal2 = initTabelJadwal()
        self.assertNotEqual(new_jadwal1, new_jadwal2)

    def testForbidKonsumenToUpdateTabelJadwal(self):
        self.client.login(username="konsumen", password="konsumen")
        response = self.client.post(
            "/mengelola-sarana-olahraga/update-jadwal/1")
        self.assertEqual(response.status_code, 403)

    def testAllowPengurusToUpdateTabelJadwal(self):
        self.client.login(username="pengurus", password="pengurus")
        data = {
            'hari_buka': ['[true,true,true,true,false,true,false]'],
            'jam_buka': ['[["10.00","11.00"],["11.00","12.00"]]'],
            'status_book': ['[[True, True, True, True, True, True, True], [True, True, True, True, True, True, True]]']
        }
        response = self.client.post(
            "/mengelola-sarana-olahraga/update-jadwal/1", data)
        self.assertEqual(response.status_code, 200)

    def test_getSaranaOlaharaga(self):
        self.client.login(username="konsumen", password="konsumen")
        response = self.client.get("/sarana/1")

        self.assertEqual(len(self.gor.getSaranaGor()), 2)
        self.assertEqual(response.status_code, 200)

    def test_get_info_gor(self):
        self.client.login(username="konsumen", password="konsumen")
        response = self.client.get("/info-gor/1")
        self.assertEqual(response.status_code, 200)
