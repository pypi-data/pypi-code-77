# Generated by Django 2.2.9 on 2020-05-03 09:26

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("pomodoro", "0008_project"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]
