# Generated by Django 3.2.9 on 2021-12-11 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todofamily', '0004_auto_20211210_1932'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['-date_create'], 'verbose_name': 'Список задач', 'verbose_name_plural': 'Списки задач'},
        ),
        migrations.AddField(
            model_name='todo',
            name='slug',
            field=models.SlugField(blank=True, max_length=30, verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='todo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todofamily.todo', verbose_name='Задача'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.CharField(max_length=50, verbose_name='Пользователь'),
        ),
    ]
