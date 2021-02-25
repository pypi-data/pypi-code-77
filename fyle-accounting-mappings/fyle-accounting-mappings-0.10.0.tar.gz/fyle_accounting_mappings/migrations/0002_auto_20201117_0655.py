# Generated by Django 3.0.3 on 2020-11-17 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyle_accounting_mappings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='destinationattribute',
            name='active',
            field=models.BooleanField(help_text='Indicates whether the fields is active or not', null=True),
        ),
        migrations.AddField(
            model_name='expenseattribute',
            name='active',
            field=models.BooleanField(help_text='Indicates whether the fields is active or not', null=True),
        ),
    ]
