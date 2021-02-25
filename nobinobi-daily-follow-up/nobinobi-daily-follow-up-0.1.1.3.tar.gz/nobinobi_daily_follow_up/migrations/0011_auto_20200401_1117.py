#      Copyright (C) 2020 <Florian Alu - Prolibre - https://prolibre.com
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Generated by Django 2.2 on 2020-04-01 09:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nobinobi_daily_follow_up', '0010_add_intermediary_departure_arrival_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nobinobi_child.Child', verbose_name='Child'),
        ),
    ]
