from django.db import models


class Img(models.Model):
    file = models.ImageField(upload_to='static/test_image_upl/images', blank=True, help_text="Upload file")
    url = models.CharField(max_length=512, default='', blank=True, help_text="Or insert a link to image")
    hash = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        if self.file:
            name = f"{self.file}"[29:]
        else:
            name = self.url
        return name

    def get_hash(self):
        if self.file:
            self.hash = hash(self.file)
        else:
            self.hash = hash(self.url)
        self.save()
