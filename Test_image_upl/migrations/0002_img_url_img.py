# Generated by Django 3.0.7 on 2020-06-20 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test_image_upl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='img',
            name='url_img',
            field=models.CharField(blank=True, default='', help_text='Or insert a link to image', max_length=512),
        ),
    ]
