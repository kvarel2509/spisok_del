# Generated by Django 3.2.9 on 2021-12-03 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todofamily', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='is_ok',
            field=models.BooleanField(default=False),
        ),
    ]