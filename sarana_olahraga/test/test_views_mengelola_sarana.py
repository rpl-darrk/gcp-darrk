import json
from django.test import Client, TestCase
from django.urls import reverse
from pengguna.models import User, Konsumen_GOR, Pengurus_GOR
from sarana_olahraga.models import GOR, Sarana, Jadwal_Reservasi


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('mengelola_sarana_olahraga:index')
        self.add_sarana_url = reverse('mengelola_sarana_olahraga:add-sarana')
        self.update_sarana_url = reverse(
            'mengelola_sarana_olahraga:update-sarana', args=['1'])
        self.delete_sarana_url = reverse(
            'mengelola_sarana_olahraga:delete-sarana', args=['1'])

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

        self.user_pengurus1 = User.objects.create_user(
            email="pengurus1@email.com",
            username="pengurus1",
            password="pengurus1",
        )

        self.pengurus1 = Pengurus_GOR.objects.create(
            user=self.user_pengurus1, nama="pengurus1", nomor_telepon="123456", akun_bank="0123124213")

        self.gor1 = GOR.objects.create(
            ID_gor='1',
            nama='GOR RPL Keren',
            url_foto='ristek.link/GOR-RPL-Keren',
            alamat='Jalan RPL Keren Nomor 1',
            nomor_telepon='081234567890',
            pengurus=self.pengurus
        )

        self.gor2 = GOR.objects.create(
            ID_gor='2',
            nama='GOR RPL Kece',
            url_foto='ristek.link/GOR-RPL-Keren',
            alamat='Jalan RPL Keren Nomor 1',
            nomor_telepon='081234567890',
            pengurus=self.pengurus1
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

    def test_index_GET_pengurus(self):
        self.client.login(username="pengurus", password="pengurus")
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response, 'base.html')
        self.assertTemplateUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')

    def test_index_GET_not_login(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 302)

        self.assertTemplateNotUsed(
            response, 'base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')

    def test_add_sarana_GET_pengurus(self):
        self.client.login(username="pengurus", password="pengurus")
        response = self.client.get(self.add_sarana_url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response, 'base.html')
        self.assertTemplateUsed(
            response, 'mengelola_sarana_olahraga/form.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')

    def test_add_sarana_GET_not_login(self):
        response = self.client.get(self.add_sarana_url)

        self.assertEqual(response.status_code, 302)

        self.assertTemplateNotUsed(
            response, 'base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')

    def test_add_sarana_POST_pengurus(self):
        self.client.login(username="pengurus", password="pengurus")
        response = self.client.post(self.add_sarana_url, {
            'nama': 'Lapangan RPL Indah 2',
            'url_foto': 'ristek.link/GOR-RPL-Keren',
            'jenis': 'Lapangan Basket',
            'deskripsi': 'Lapangan RPL Indah merupakan lapangan kedua yang ada di GOR RPL Keren'
        })
        new_project = Sarana.objects.get(ID_sarana__exact=2)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Sarana.objects.all()), 2)

        self.assertEqual(new_project.gor, self.gor1)
        self.assertEqual(new_project.ID_sarana, '2')
        self.assertEqual(new_project.id_jadwal_reservasi.ID_jadwal, 2)
        self.assertEqual(new_project.nama, 'Lapangan RPL Indah 2')
        self.assertEqual(new_project.url_foto, 'ristek.link/GOR-RPL-Keren')
        self.assertEqual(new_project.jenis, 'Lapangan Basket')
        self.assertEqual(new_project.deskripsi,
                         'Lapangan RPL Indah merupakan lapangan kedua yang ada di GOR RPL Keren')

        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')

    def test_add_sarana_POST_not_login(self):
        response = self.client.post(self.add_sarana_url, {
            'nama': 'Lapangan RPL Indah 2',
            'url_foto': 'ristek.link/GOR-RPL-Keren',
            'jenis': 'Lapangan Basket',
            'deskripsi': 'Lapangan RPL Indah merupakan lapangan kedua yang ada di GOR RPL Keren'
        })
        new_project = Sarana.objects.filter(ID_sarana__exact=2).first()
        self.assertEqual(new_project, None)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Sarana.objects.all()), 1)

        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')

    def test_update_sarana_GET_pengurus(self):
        self.client.login(username="pengurus", password="pengurus")
        response = self.client.get(self.update_sarana_url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response, 'base.html')
        self.assertTemplateUsed(
            response, 'mengelola_sarana_olahraga/form.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')

    def test_update_sarana_GET_pengurus_invalid(self):
        self.client.login(username="pengurus1", password="pengurus1")
        response = self.client.get(self.update_sarana_url)

        self.assertEqual(response.status_code, 302)

        self.assertTemplateNotUsed(
            response, 'base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')

    def test_update_sarana_GET_not_login(self):
        response = self.client.get(self.update_sarana_url)

        self.assertEqual(response.status_code, 302)

        self.assertTemplateNotUsed(
            response, 'base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')

    def test_update_sarana_POST_pengurus(self):
        self.client.login(username="pengurus", password="pengurus")
        response = self.client.post(self.update_sarana_url, {
            'nama': 'Lapangan RPL Indah 1',
            'url_foto': 'ristek.link/GOR-RPL-Keren',
            'jenis': 'Lapangan Basket',
            'deskripsi': 'Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren'
        })
        new_project = Sarana.objects.get(ID_sarana__exact=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Sarana.objects.all()), 1)

        self.assertEqual(new_project.gor, self.gor1)
        self.assertEqual(new_project.ID_sarana, '1')
        self.assertEqual(new_project.nama, 'Lapangan RPL Indah 1')
        self.assertEqual(new_project.url_foto, 'ristek.link/GOR-RPL-Keren')
        self.assertEqual(new_project.jenis, 'Lapangan Basket')
        self.assertEqual(new_project.deskripsi,
                         'Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren')

        self.assertTemplateNotUsed(
            response, 'base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')

    def test_update_sarana_POST_not_login(self):
        response = self.client.post(self.update_sarana_url, {
            'nama': 'Lapangan RPL Indah 1',
            'url_foto': 'ristek.link/GOR-RPL-Keren',
            'jenis': 'Lapangan Basket',
            'deskripsi': 'Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren'
        })
        new_project = Sarana.objects.get(ID_sarana__exact=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Sarana.objects.all()), 1)

        self.assertEqual(new_project.gor, self.gor1)
        self.assertEqual(new_project.ID_sarana, '1')
        self.assertEqual(new_project.nama, 'Lapangan RPL Indah')
        self.assertEqual(new_project.url_foto, 'ristek.link/GOR-RPL-Keren')
        self.assertEqual(new_project.jenis, 'Lapangan Basket')
        self.assertEqual(new_project.deskripsi,
                         'Lapangan RPL Indah merupakan lapangan pertama yang ada di GOR RPL Keren')

        self.assertTemplateNotUsed(
            response, 'base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')

    def test_delete_sarana_POST_pengurus(self):
        self.client.login(username="pengurus", password="pengurus")
        response = self.client.post(self.delete_sarana_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Sarana.objects.all()), 0)

        self.assertTemplateNotUsed(
            response, 'base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')

    def test_delete_sarana_POST_not_login(self):
        response = self.client.post(self.delete_sarana_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Sarana.objects.all()), 1)

        self.assertTemplateNotUsed(
            response, 'base.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/index.html')
        self.assertTemplateNotUsed(
            response, 'mengelola_sarana_olahraga/form.html')
