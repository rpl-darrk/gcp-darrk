from django.test import TestCase
from mengelola_sarana_olahraga.models import GOR, Sarana


class TestModels(TestCase):

    def setUp(self):
        self.gor1 = GOR.objects.create(
            id='1',
            nama='GOR RPL Keren',
            url_foto='ristek.link/GOR-RPL-Keren',
            alamat='Jalan RPL Keren Nomor 1',
            nomor_telepon='081234567890'
        )
        self.sarana1 = Sarana.objects.create(
            gor=self.gor1,
            id='1',
            nama='Lapangan RPL Indah',
            url_foto='ristek.link/GOR-RPL-Keren',
            jenis='Lapangan Basket',
            deskripsi='Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren'
        )

    def test_gor_has_same_field_with_input(self):
        self.assertEqual(self.gor1.id, "1")
        self.assertEqual(self.gor1.nama, "GOR RPL Keren")
        self.assertEqual(self.gor1.url_foto, "ristek.link/GOR-RPL-Keren")
        self.assertEqual(self.gor1.alamat, "Jalan RPL Keren Nomor 1")
        self.assertEqual(self.gor1.nomor_telepon, "081234567890")

    def test_sarana_has_same_field_with_input(self):
        self.assertEqual(self.sarana1.gor, self.gor1)
        self.assertEqual(self.sarana1.id, "1")
        self.assertEqual(self.sarana1.nama, "Lapangan RPL Indah")
        self.assertEqual(self.sarana1.url_foto, "ristek.link/GOR-RPL-Keren")
        self.assertEqual(self.sarana1.jenis, "Lapangan Basket")
        self.assertEqual(self.sarana1.deskripsi,
                         "Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren")
