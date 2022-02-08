from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Todo(models.Model):
    is_from = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Кто создал задачу?',
                                related_name='is_from_user')
    is_to = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Для кого задача?',
                              related_name='is_to_user')
    content = models.TextField(verbose_name='Задача')
    slug = models.SlugField(max_length=30, verbose_name='Слаг', blank=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/', blank=True, verbose_name='Фото')
    file = models.FileField(upload_to='file/%Y/%m/', blank=True, verbose_name='Файл')
    date_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)
    data_deadline = models.DateTimeField(blank=True, null=True, verbose_name='Срок исполнения')
    is_public = models.BooleanField(default=True)
    is_ok = models.BooleanField(default=False)
    is_negative = models.BooleanField(default=False)
    is_scan = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk} - {self.content}'

    def get_absolute_url(self):
        return reverse('show_todo', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Список задач'
        verbose_name_plural = 'Списки задач'
        ordering = [
            '-date_create'
        ]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь', related_name='user_is_from')
    content = models.TextField(verbose_name='Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, verbose_name='Задача')

    def __str__(self):
        return f'{self.todo} - {self.content}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['date']


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatar/', blank=True)
    number = models.IntegerField(verbose_name='Номер телефона', unique=True, blank=True, null=True)
    mail = models.EmailField(verbose_name='Эл.почта', unique=True, blank=True)