from django.test import TestCase
from mengelola_sarana_olahraga.forms import SaranaForm


class TestForms(TestCase):

    def test_sarana_form_valid_data(self):
        form = SaranaForm(data={
            'nama': 'Lapangan RPL Indah 2',
            'url_foto': 'ristek.link/GOR-RPL-Keren',
            'jenis': 'Lapangan Basket',
            'deskripsi': 'Lapangan RPL Indah merupakan lapangan kedua yang ada di GOR RPL Keren'
        })

        self.assertTrue(form.is_valid())

    def test_sarana_form_no_data(self):
        form = SaranaForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
