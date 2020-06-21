from django.test import TestCase, Client
from django.urls import reverse
from Test_image_upl.views import resize_image
from PIL import Image
import io
from pathlib import Path


class TestViews(TestCase):
    def setUp(self):
        img_path = Path(__file__).parent.joinpath('4u8cwjoeffz11.jpg')
        self.client = Client()
        self.index = reverse('index')
        self.upload = reverse('upload')
        self.pic = open(img_path, 'rb')

    def test_index(self):
        response = self.client.get(self.index)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_upload_view(self):
        response = self.client.get(self.upload)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')

    def test_resize_image(self):
        resized = resize_image(150, 150, None, self.pic)
        img = Image.open(io.BytesIO(resized))
        self.assertEqual(img.width, 150)
        self.assertEqual(img.height, 150)

    def test_resize_size_image(self):
        resized = resize_image(None, None, 50000, self.pic)
        self.assertLessEqual(len(resized), 50000)
