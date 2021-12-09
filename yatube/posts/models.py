from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    title = models.CharField('Имя', max_length=200, unique=True)
    slug = models.SlugField('Адрес', unique=True)
    description = models.TextField('Описание')
    def __str__(self):
        return self.title

class Post(models.Model):
    class Meta:
        ordering = ['-pub_date']

    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts'
    )
