# Generated by Django 2.2 on 2021-02-08 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giant_plugins', '0011_auto_20210129_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagecard',
            name='cta_text',
            field=models.CharField(default='Read more', max_length=50),
        ),
    ]
