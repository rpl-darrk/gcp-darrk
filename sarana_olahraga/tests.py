from django.test import TestCase, Client
from .views import *
from .models import *
from pengguna.models import *

# Create your tests here.


class SaranaOlahragaTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_getSaranaOlaharaga(self):
        pengurus = Pengurus_GOR.objects.create(username="pengurus",  password="pengurus",
                                               confirm_password="pengurus", nama="pengurus", email="email@email.com", nomor_telepon="67890", akun_bank="0123124213")
        gor = GOR.objects.create(ID_gor="1",  nama="nama",
                                 url_foto="url_foto", alamat="alamat", no_telepon="no_telepon", pengurus=pengurus)
        Sarana.objects.create(ID_sarana="1",  nama="nama",
                                        url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=gor)
        Sarana.objects.create(ID_sarana="2",  nama="nama",
                                        url_foto="url_foto", jenis="jenis", deskripsi="deskripsi", gor=gor)

        response = self.client.get("sarana/1")
        self.assertEqual(gor.getSaranaGor(), gor.sarana_set.all())
        self.assertEqual(len(gor.getSaranaGor()), 2)
        self.assertEqual(response.status_code, 200)
