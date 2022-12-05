import json
from django.test import TestCase
from sarana_olahraga.models import GOR, Sarana, Jadwal_Reservasi


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

    def test_jadwal_reservasi_has_same_field_with_input(self):
        self.assertEqual(self.jadwal_reservasi_1.ID_jadwal, 1)
        self.assertEqual(self.jadwal_reservasi_1.hari_buka, json.loads(
            "[true, true, true, true, true, false, false]"))
        self.assertEqual(self.jadwal_reservasi_1.jam_buka, json.loads(
            '[["10.00", "11.00"], ["11.00", "12.00"]]'))
        self.assertEqual(self.jadwal_reservasi_1.status_book, json.loads(
            "[[true, true, false, true, true, true, true], [true, true, true, true, true, true, true]]"))
