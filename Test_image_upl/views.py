from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseBadRequest
from .forms import UploadImageform
from django.core.validators import ValidationError
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
                    imgObject = uploadform.instance
                    Img.get_hash(imgObject)

                if url:
                    uploadform.save()
                    imgObject = uploadform.instance
                    image = requests.get(url)
                    data = ContentFile(image.content)
                    Img.get_hash(imgObject)
                    imgObject.file.save(randomName, data)


def resize_image(set_width, set_height, set_size, imgbytes):
    try:
        pil_img = Image.open(imgbytes)
        if pil_img.format not in ('BMP', 'JPG', 'JPEG', 'PNG'):
            raise ValidationError("Unsupported file type")
    except ImportError:
        raise ValidationError

    width, height = pil_img.size
    Imageformat = pil_img.format
    if set_width and set_height:
        try:
            pil_img = pil_img.resize((int(set_width), int(set_height)))
        except ValueError:
            raise Exception("Invalid parameter. Parameter must be a number")

    elif set_height:
        try:
            resize_by_height = int(set_height)/height
            pil_img = pil_img.resize((int(width*resize_by_height), int(set_height)))
        except (ZeroDivisionError, ValueError) as e:
            raise Exception("Invalid parameter. Parameter must be a positive number which is not 0")

    elif set_width:
        try:
            resize_by_width = int(set_width)/width
            pil_img = pil_img.resize((int(set_width), int(height // (1 / resize_by_width))))
        except (ZeroDivisionError, ValueError) as e:
            raise Exception("Invalid parameter. Parameter must be a positive number which is not 0")

    in_mem_file = io.BytesIO()
    n = 100
    pil_img.save(in_mem_file, format=Imageformat)
    imgbytes = in_mem_file.getvalue()

    if set_size:
        try:
            while len(imgbytes) > int(set_size):
                in_mem_file = io.BytesIO()
                pil_img.save(in_mem_file, format=Imageformat, optimize=True, quality=n)
                n -= 5
                imgbytes = in_mem_file.getvalue()
                if n < 5:
                    break
        except (ZeroDivisionError, ValueError) as e:
            raise Exception("Invalid parameter. Parameter must be a positive number which is not 0")
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

    if imgbytes:
        response = HttpResponse(imgbytes, content_type='image/jpeg')
        response['Cache-Control'] = 'public, max-age=315360'
    else:
        return HttpResponseBadRequest
    return response


def upload_view(request):
    upload(request)
    return render(request, 'upload.html', {'upload_form': UploadImageform})
