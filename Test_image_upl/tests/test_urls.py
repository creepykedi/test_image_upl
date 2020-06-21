from django.test import SimpleTestCase
from django.urls import resolve, reverse
from Test_image_upl.views import *


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_upload_view_url_is_resolved(self):
        url = reverse('upload')
        self.assertEquals(resolve(url).func, upload_view)

    def test_redirect_image_url_is_resolved(self):
        url = reverse('redirect_image', args=['435575456'])
        self.assertEquals(resolve(url).func, image_view)
