from django.test import TestCase, Client
from .views import *
from .models import *
from pengguna.models import *

# Create your tests here.


class SaranaOlahragaTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_getSaranaOlaharaga(self):
        user = User.objects.create_user(
            email="user@email.com",
            username="username",
            password="password",
        )

        pengurus = Pengurus_GOR.objects.create(
            user=user, nama="pengurus", nomor_telepon="67890", akun_bank="0123124213")

        gor = GOR.objects.create(ID_gor="1",  nama="nama",
                                 url_foto="url_foto", alamat="alamat", no_telepon="no_telepon", pengurus=pengurus)
        Sarana.objects.create(ID_sarana="1",  nama="nama",
                              url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=gor)
        Sarana.objects.create(ID_sarana="2",  nama="nama",
                              url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=gor)

        self.client.login(username="username", password="password")
        response = self.client.get("/sarana/1")

        self.assertEqual(len(gor.getSaranaGor()), 2)
        self.assertEqual(response.status_code, 200)
