from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import UploadImageform
from .models import Img
import requests
from django.core.files.base import ContentFile
import random
import string
from PIL import Image
import io
from django.core.files.storage import default_storage as storage

randomName = ''.join(random.choice(string.ascii_letters) for x in range(10)) + '.jpg'


def index(request):
    image_list = Img.objects.all()
    return render(request, 'index.html', {'image_list': image_list})


def upload(request):
    uploadform = UploadImageform(request.POST, request.FILES)
    if request.method == "POST":
        if uploadform.is_valid():
            file = uploadform.cleaned_data['file']
            url = uploadform.cleaned_data['url']

            if file or url:
                if file:
                    uploadform.save()
                    imgObject = Img.objects.get(pk=uploadform.instance.id)
                    Img.get_hash(imgObject)

                if url:
                    uploadform.save()
                    imgObject = Img.objects.get(pk=uploadform.instance.id)
                    image = requests.get(url)
                    data = ContentFile(image.content)
                    Img.get_hash(imgObject)
                    imgObject.file.save(randomName, data)


def resize_image(set_width, set_height, set_size, imgbytes):
    pil_img = Image.open(imgbytes)
    width, height = pil_img.size
    if set_width and set_height:
        pil_img = pil_img.resize((int(set_width), int(set_height)))

    elif set_height:
        assert set_height != 0
        resize_by_height = int(set_height)/height
        pil_img = pil_img.resize((int(width*resize_by_height), int(set_height)))

    elif set_width:
        assert set_width != 0
        resize_by_width = int(set_width)/width
        pil_img = pil_img.resize((int(set_width), int(height // (1 / resize_by_width))))

    in_mem_file = io.BytesIO()
    n = 100
    pil_img.save(in_mem_file, format='JPEG')
    imgbytes = in_mem_file.getvalue()
    if set_size:
        while len(imgbytes) > int(set_size):
            in_mem_file = io.BytesIO()
            pil_img.save(in_mem_file, format='JPEG', optimize=True, quality=n)
            n -= 1
            imgbytes = in_mem_file.getvalue()
            if n < 2:
                break
    return imgbytes


def image_view(request, image_hash, *args, **kwargs):
    image = get_object_or_404(Img, hash=image_hash)

    imgbytes = storage.open(image.file.name, 'rb')
    set_width = set_height = set_size = None

    if request.method == "GET":
        if "width" in request.GET:
            set_width = request.GET["width"]
        if "height" in request.GET:
            set_height = request.GET["height"]
        if "size" in request.GET:
            set_size = request.GET["size"]
        imgbytes = resize_image(set_width, set_height, set_size, imgbytes)

    response = HttpResponse(imgbytes, content_type='image/jpeg')
    response['Cache-Control'] = 'public, max-age=315360'
    return response


def upload_view(request):
    upload(request)
    return render(request, 'upload.html', {'upload_form': UploadImageform})
