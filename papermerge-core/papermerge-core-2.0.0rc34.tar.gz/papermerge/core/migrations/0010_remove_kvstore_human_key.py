# Generated by Django 3.0.6 on 2020-06-02 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_kvstore_kvstorenode_kvstorepage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kvstore',
            name='human_key',
        ),
    ]
