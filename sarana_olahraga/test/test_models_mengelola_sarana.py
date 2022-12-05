import json
from django.test import TestCase
from sarana_olahraga.models import GOR, Sarana, Jadwal_Reservasi
from reservasi_sarana.models import Sewa_Sarana
from datetime import datetime


class TestModels(TestCase):

    def setUp(self):
        self.gor1 = GOR.objects.create(
            ID_gor='1',
            nama='GOR RPL Keren',
            url_foto='ristek.link/GOR-RPL-Keren',
            alamat='Jalan RPL Keren Nomor 1',
            nomor_telepon='081234567890'
        )
        self.jadwal_reservasi_1 = Jadwal_Reservasi.objects.create(
            hari_buka=json.loads(
                "[true, true, true, true, true, false, false]"),
            jam_buka=json.loads('[["10.00", "11.00"], ["11.00", "12.00"]]'),
            status_book=json.loads(
                "[[true, true, false, true, true, true, true], [true, true, true, true, true, true, true]]"),
        )
        self.sarana1 = Sarana.objects.create(
            gor=self.gor1,
            id_jadwal_reservasi=self.jadwal_reservasi_1,
            ID_sarana='1',
            nama='Lapangan RPL Indah',
            url_foto='ristek.link/GOR-RPL-Keren',
            jenis='Lapangan Basket',
            deskripsi='Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren'
        )
        self.sewa_sarana_1 = Sewa_Sarana.objects.create(
            ID_sewa="1",
            datetime=datetime.now(),
            sarana=self.sarana1,
            status=0,
            jam_booking=["10.00-11.00", 0],
        )

    def test_gor_has_same_field_with_input(self):
        self.assertEqual(self.gor1.ID_gor, "1")
        self.assertEqual(self.gor1.nama, "GOR RPL Keren")
        self.assertEqual(self.gor1.url_foto, "ristek.link/GOR-RPL-Keren")
        self.assertEqual(self.gor1.alamat, "Jalan RPL Keren Nomor 1")
        self.assertEqual(self.gor1.nomor_telepon, "081234567890")

    def test_sarana_has_same_field_with_input(self):
        self.assertEqual(self.sarana1.gor, self.gor1)
        self.assertEqual(self.sarana1.id_jadwal_reservasi,
                         self.jadwal_reservasi_1)
        self.assertEqual(self.sarana1.ID_sarana, "1")
        self.assertEqual(self.sarana1.nama, "Lapangan RPL Indah")
        self.assertEqual(self.sarana1.url_foto, "ristek.link/GOR-RPL-Keren")
        self.assertEqual(self.sarana1.jenis, "Lapangan Basket")
        self.assertEqual(self.sarana1.deskripsi,
                         "Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren")
        self.assertEqual(self.sarana1.get_sewa_sarana().get(sarana__sewasarana__ID_sewa__exact="1"),
                         self.sewa_sarana_1)
