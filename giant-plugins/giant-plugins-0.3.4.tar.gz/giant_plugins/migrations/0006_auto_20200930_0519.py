# Generated by Django 2.2 on 2020-09-30 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giant_plugins', '0005_auto_20200916_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentwidthvideo',
            name='alt_text',
            field=models.CharField(blank=True, default=models.CharField(blank=True, max_length=128), max_length=128),
        ),
        migrations.AddField(
            model_name='contentwidthvideo',
            name='display_image',
            field=models.BooleanField(default=True),
        ),
    ]
