# Generated by Django 3.1.3 on 2021-02-16 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20210205_0915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='current_storage_size',
        ),
        migrations.RemoveField(
            model_name='user',
            name='mail_by_secret',
        ),
        migrations.RemoveField(
            model_name='user',
            name='mail_by_user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='mail_secret',
        ),
    ]
