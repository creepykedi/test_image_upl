from django.forms import ModelForm
from .models import Img


class UploadImageform(ModelForm):
    class Meta:
        model = Img
        fields = ['file', 'url']
