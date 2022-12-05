from django.test import SimpleTestCase
from django.urls import resolve, reverse
from sarana_olahraga.view.views_mengelola_sarana import index, post_sarana, update_sarana, delete_sarana


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('mengelola_sarana_olahraga:index')
        resolve_url = resolve(url)
        self.assertEqual(resolve_url.func, index)
        self.assertEqual(resolve_url.url_name, 'index')
        self.assertEqual(resolve_url.app_names, ['mengelola_sarana_olahraga'])
        self.assertEqual(resolve_url.namespaces, ['mengelola_sarana_olahraga'])
        self.assertEqual(resolve_url.route, 'mengelola_sarana_olahraga/')

    def test_post_url_is_resolved(self):
        url = reverse('mengelola_sarana_olahraga:post_sarana')
        resolve_url = resolve(url)
        self.assertEqual(resolve_url.func, post_sarana)
        self.assertEqual(resolve_url.url_name, 'post_sarana')
        self.assertEqual(resolve_url.app_names, ['mengelola_sarana_olahraga'])
        self.assertEqual(resolve_url.namespaces, ['mengelola_sarana_olahraga'])
        self.assertEqual(resolve_url.route,
                         'mengelola_sarana_olahraga/post_sarana/')

    def test_update_url_is_resolved(self):
        url = reverse('mengelola_sarana_olahraga:update_sarana', args=['1'])
        resolve_url = resolve(url)
        self.assertEqual(resolve_url.func, update_sarana)
        self.assertEqual(resolve_url.url_name, 'update_sarana')
        self.assertEqual(resolve_url.app_names, ['mengelola_sarana_olahraga'])
        self.assertEqual(resolve_url.namespaces, ['mengelola_sarana_olahraga'])
        self.assertEqual(
            resolve_url.route, 'mengelola_sarana_olahraga/update_sarana/<str:id_sarana>')

    def test_delete_url_is_resolved(self):
        url = reverse('mengelola_sarana_olahraga:delete_sarana', args=['1'])
        resolve_url = resolve(url)
        self.assertEqual(resolve_url.func, delete_sarana)
        self.assertEqual(resolve_url.url_name, 'delete_sarana')
        self.assertEqual(resolve_url.app_names, ['mengelola_sarana_olahraga'])
        self.assertEqual(resolve_url.namespaces, ['mengelola_sarana_olahraga'])
        self.assertEqual(
            resolve_url.route, 'mengelola_sarana_olahraga/delete_sarana/<str:id_sarana>')
