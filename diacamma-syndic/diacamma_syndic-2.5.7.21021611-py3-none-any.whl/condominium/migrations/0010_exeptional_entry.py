# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-17 08:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payoff', '0006_depositslip_status'),
        ('accounting', '0004_modelentry_costaccounting'),
        ('condominium', '0009_setcost'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartitionExceptional',
            fields=[
            ],
            options={
                'verbose_name': 'exceptional class load',
                'verbose_name_plural': 'exceptional class loads',
                'proxy': True,
                'ordering': ['owner__third_id', 'set_id'],
                'default_permissions': [],
            },
            bases=('condominium.partition',),
        ),
        migrations.AddField(
            model_name='calldetail',
            name='entry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.EntryAccount', verbose_name='entry'),
        ),
        migrations.AlterField(
            model_name='expensedetail',
            name='entry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.EntryAccount', verbose_name='entry'),
        ),
    ]
