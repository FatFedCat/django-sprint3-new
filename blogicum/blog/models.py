from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import BaseModel

User = get_user_model()

MAX_LENGTH = 256


class TitleModel(models.Model):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок',
    )

    class Meta:
        abstract = True


class Category(TitleModel, BaseModel):
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class PostManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )


class Post(TitleModel, BaseModel):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    objects = PostManager()

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
