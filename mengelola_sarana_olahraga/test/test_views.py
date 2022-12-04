import json
from django.test import Client, TestCase
from django.urls import reverse
from mengelola_sarana_olahraga.models import GOR, Sarana
from melihat_jadwal_reservasi.models import JadwalReservasi


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('mengelola_sarana_olahraga:index')
        self.post_sarana_url = reverse('mengelola_sarana_olahraga:post_sarana')
        self.update_sarana_url = reverse('mengelola_sarana_olahraga:update_sarana', args=['1'])
        self.delete_sarana_url = reverse('mengelola_sarana_olahraga:delete_sarana', args=['1'])
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

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'mengelola_sarana_olahraga/base.html')
        self.assertTemplateUsed(response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateUsed(response, 'mengelola_sarana_olahraga/css.html')
        self.assertTemplateUsed(response, 'mengelola_sarana_olahraga/scripts.html')

        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/form.html')

    def test_post_sarana_GET(self):
        response = self.client.get(self.post_sarana_url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'mengelola_sarana_olahraga/base.html')
        self.assertTemplateUsed(response, 'mengelola_sarana_olahraga/form.html')
        self.assertTemplateUsed(response, 'mengelola_sarana_olahraga/scripts.html')

        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/css.html')

    def test_post_sarana_POST(self):
        response = self.client.post(self.post_sarana_url, {
            'nama': 'Lapangan RPL Indah 2',
            'url_foto': 'ristek.link/GOR-RPL-Keren',
            'jenis': 'Lapangan Basket',
            'deskripsi': 'Lapangan RPL Indah merupakan lapangan kedua yang ada di GOR RPL Keren'
        })
        new_project = Sarana.objects.get(id__exact=2)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Sarana.objects.all()), 2)

        self.assertEqual(new_project.gor, self.gor1)
        self.assertEqual(new_project.id, '2')
        self.assertEqual(new_project.jadwal_reservasi.id, 2)
        self.assertEqual(new_project.nama, 'Lapangan RPL Indah 2')
        self.assertEqual(new_project.url_foto, 'ristek.link/GOR-RPL-Keren')
        self.assertEqual(new_project.jenis, 'Lapangan Basket')
        self.assertEqual(new_project.deskripsi,
                         'Lapangan RPL Indah merupakan lapangan kedua yang ada di GOR RPL Keren')

        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/base.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/form.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/css.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/scripts.html')

    def test_update_sarana_GET(self):
        response = self.client.get(self.update_sarana_url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'mengelola_sarana_olahraga/base.html')
        self.assertTemplateUsed(response, 'mengelola_sarana_olahraga/form.html')
        self.assertTemplateUsed(response, 'mengelola_sarana_olahraga/scripts.html')

        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/css.html')

    def test_update_sarana_POST(self):
        response = self.client.post(self.update_sarana_url, {
            'nama': 'Lapangan RPL Indah 1',
            'url_foto': 'ristek.link/GOR-RPL-Keren',
            'jenis': 'Lapangan Basket',
            'deskripsi': 'Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren'
        })
        new_project = Sarana.objects.get(id__exact=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Sarana.objects.all()), 1)

        self.assertEqual(new_project.gor, self.gor1)
        self.assertEqual(new_project.id, '1')
        self.assertEqual(new_project.nama, 'Lapangan RPL Indah 1')
        self.assertEqual(new_project.url_foto, 'ristek.link/GOR-RPL-Keren')
        self.assertEqual(new_project.jenis, 'Lapangan Basket')
        self.assertEqual(new_project.deskripsi,
                         'Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren')

        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/base.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/form.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/css.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/scripts.html')

    def test_delete_sarana_POST(self):
        response = self.client.post(self.delete_sarana_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Sarana.objects.all()), 0)

        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/base.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/form.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/css.html')
        self.assertTemplateNotUsed(response, 'mengelola_sarana_olahraga/scripts.html')