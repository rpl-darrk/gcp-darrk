import json
from datetime import datetime, timedelta, timezone
from django.test import Client, TestCase
from django.urls import reverse
from sarana_olahraga.models import GOR, Sarana, Jadwal_Reservasi
from reservasi_sarana.models import Sewa_Sarana


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.get_jadwal_url = reverse(
            'jadwal_reservasi:get_jadwal_reservasi', args=['1', '1'])
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
            datetime=datetime.today()-timedelta(days=1),
            sarana=self.sarana1,
            status=0,
            jam_booking=["10.00-11.00", 0],
        )
        self.sewa_sarana_2 = Sewa_Sarana.objects.create(
            ID_sewa="2",
            datetime=datetime.now(),
            sarana=self.sarana1,
            status=0,
            jam_booking=["10.00-11.00", 0],
        )

    def test_get_jadwal_reservasi_GET(self):
        response = self.client.get(self.get_jadwal_url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response, 'melihat_jadwal_reservasi/index.html')
        self.assertTemplateUsed(response, 'base.html')

        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')

    def test_get_jadwal_reservasi_POST(self):
        response = self.client.post(self.get_jadwal_url, data={})
        self.assertEqual(response.status_code, 302)

        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/css.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/scripts.html')
        self.assertTemplateNotUsed(
            response, 'melihat_jadwal_reservasi/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')
