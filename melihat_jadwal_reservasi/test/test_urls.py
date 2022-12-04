from django.test import SimpleTestCase
from django.urls import resolve, reverse
from melihat_jadwal_reservasi.views import get_jadwal_reservasi


class TestUrls(SimpleTestCase):

    def test_update_url_is_resolved(self):
        url = reverse('melihat_jadwal_reservasi:get_jadwal_reservasi', args=['1', '1'])
        resolve_url = resolve(url)
        self.assertEqual(resolve_url.func, get_jadwal_reservasi)
        self.assertEqual(resolve_url.url_name, 'get_jadwal_reservasi')
        self.assertEqual(resolve_url.app_names, ['melihat_jadwal_reservasi'])
        self.assertEqual(resolve_url.namespaces, ['melihat_jadwal_reservasi'])
        self.assertEqual(resolve_url.route, 'melihat_jadwal_reservasi/<str:id_gor>/<str:id_sarana>/')
