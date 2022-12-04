import json
from django.test import TestCase
from mengelola_sarana_olahraga.models import GOR, Sarana
from melihat_jadwal_reservasi.models import JadwalReservasi


class TestModels(TestCase):
    def setUp(self):
        self.gor1 = GOR.objects.create(
            id='1',
            nama='GOR RPL Keren',
            url_foto='ristek.link/GOR-RPL-Keren',
            alamat='Jalan RPL Keren Nomor 1',
            nomor_telepon='081234567890'
        )
        self.jadwal_reservasi_1 = JadwalReservasi.objects.create(
            hari_buka=json.loads("[true, true, true, true, true, false, false]"),
            jam_buka=json.loads('[["10.00", "11.00"], ["11.00", "12.00"]]'),
            status_book=json.loads(
                "[[true, true, false, true, true, true, true], [true, true, true, true, true, true, true]]"),
        )
        self.sarana1 = Sarana.objects.create(
            gor=self.gor1,
            jadwal_reservasi=self.jadwal_reservasi_1,
            id='1',
            nama='Lapangan RPL Indah',
            url_foto='ristek.link/GOR-RPL-Keren',
            jenis='Lapangan Basket',
            deskripsi='Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren'
        )

    def test_jadwal_reservasi_has_same_field_with_input(self):
        self.assertEqual(self.jadwal_reservasi_1.id, 1)
        self.assertEqual(self.jadwal_reservasi_1.hari_buka, json.loads("[true, true, true, true, true, false, false]"))
        self.assertEqual(self.jadwal_reservasi_1.jam_buka, json.loads('[["10.00", "11.00"], ["11.00", "12.00"]]'))
        self.assertEqual(self.jadwal_reservasi_1.status_book, json.loads(
                "[[true, true, false, true, true, true, true], [true, true, true, true, true, true, true]]"))
