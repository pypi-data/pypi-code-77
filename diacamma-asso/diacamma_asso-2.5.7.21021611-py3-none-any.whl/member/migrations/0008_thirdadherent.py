# Generated by Django 2.2.2 on 2019-06-22 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0012_entrylineaccount_reference_size'),
        ('member', '0007_add_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThirdAdherent',
            fields=[],
            options={
                'proxy': True,
                'default_permissions': [],
                'indexes': [],
                'constraints': [],
            },
            bases=('accounting.third',),
        ),
    ]
