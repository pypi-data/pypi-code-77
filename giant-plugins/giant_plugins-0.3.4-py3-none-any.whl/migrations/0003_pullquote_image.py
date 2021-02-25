# Generated by Django 2.2 on 2020-08-19 03:42

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('giant_plugins', '0002_heroimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='pullquote',
            name='image',
            field=filer.fields.image.FilerImageField(help_text='Here you can set an optional image to be displayed with the quote', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.FILER_IMAGE_MODEL),
        ),
    ]
