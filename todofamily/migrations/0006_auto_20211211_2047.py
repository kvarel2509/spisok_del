# Generated by Django 3.2.9 on 2021-12-11 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todofamily', '0005_auto_20211211_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='file',
            field=models.FileField(blank=True, upload_to='file/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photo/%Y/%m/'),
        ),
    ]