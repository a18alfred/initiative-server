import os
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from core.apps.accounts.models import Account
from .managers import LikeDislikeManager
from .validators import validate_file
from slugify import slugify
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid


def upload_category_path(instance, filename):
    """
    Функция возвращает путь для сохранения иконки категории
    """
    name, extension = os.path.splitext(filename)
    return '/'.join(['categories', str(instance.slug), str(uuid.uuid4()) + extension])


class Category(models.Model):
    """
    Модель для хранения категорий проекта
    name - название категории
    icon - иконка категории
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(max_length=255, blank=False, unique=True, verbose_name='Название')

    icon = models.ImageField(blank=True, null=True, upload_to=upload_category_path,
                             default='categories/default_category_icon.png', validators=[validate_file],
                             verbose_name='Иконка для категории')

    slug = models.SlugField(max_length=255, unique=True, default='')

    def __str__(self):
        """
        Возвращает название категории
        """
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        if not self.icon:
            self.icon = 'categories/default_category_icon.png'
        self.slug = slugify(self.name, lowercase=True)
        super(Category, self).save(*args, **kwargs)


class LikeDislike(models.Model):
    """
    Модель лайк-дизлайк, которая сможет работать с любым типом контента.
    """
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    account = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='account_likes', on_delete=models.CASCADE, )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    class Meta:
        unique_together = [('account', 'object_id', 'content_type'), ]
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def save(self, *args, **kwargs):
        try:
            super(LikeDislike, self).save(*args, **kwargs)
        except Exception as e:
            print(e)


class Project(models.Model):
    """
    Основная модель проекта.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account_projects')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='category_projects',
                                 verbose_name='Категория')

    description = models.TextField(blank=False, verbose_name='Описание')
    is_personal = models.BooleanField(default=False, verbose_name="Личный проект")

    is_approved = models.BooleanField(default=False, verbose_name="Одобрена")
    is_feature = models.BooleanField(default=False, verbose_name="Всегда в топе")

    likes_count = models.IntegerField(default=0, editable=False, verbose_name='Количество лайков')
    dislikes_count = models.IntegerField(default=0, editable=False, verbose_name='Количество дизлайков')
    rating = models.IntegerField(default=0, editable=False, verbose_name='Общий рейтинг')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    votes = GenericRelation(LikeDislike, related_query_name='projects')

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ['created_at']

    def __str__(self):
        """
        Возвращает дату создания
        """
        return str(self.id)


def upload_file_path(instance, filename):
    """
    Функция возвращает путь для сохранения файлов. Файлы хранятся в media/projects/attachments/${project.pk}
    """
    name, extension = os.path.splitext(filename)
    instance.name = name
    return '/'.join(['projects', str(instance.project.pk), 'attachments', str(uuid.uuid4()) + extension])


class Attachment(models.Model):
    """
    Модель для хранения файлов проекта. Модель включает:
    project - проект к которому относится файл
    uploaded_file - ссылка на сохраненный файл на сервере
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="project_attachments")
    uploaded_file = models.FileField(blank=False, upload_to=upload_file_path,
                                     validators=[validate_file],
                                     verbose_name='загруженный файл')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название файла')

    is_feature = models.BooleanField(default=False, verbose_name="Всегда в топе")

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def save(self, *args, **kwargs):
        try:
            super(Attachment, self).save(*args, **kwargs)
        except ValidationError as validation_error:
            print(validation_error)


class Link(models.Model):
    """
    Модель для хранения внешних ссылок проекта. Модель включает:
    project - проект к которому относится ссылка
    external_link - внешняя ссылка (например на видео или какой-то файл)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_links")
    url = models.URLField(blank=False, max_length=2050, verbose_name='ссылка')

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"

    def save(self, *args, **kwargs):
        try:
            super(Link, self).save(*args, **kwargs)
        except ValidationError as validation_error:
            print(validation_error)


class Comment(models.Model):
    """
    Модель для хранения комментариев:
    project - проект к которому относится комментарий
    account - аккаунт, который написал комментарий
    content- комментарий
    parent - родитель комментария в случае если комментарий это ответ на другой комментарий
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account_comments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="project_comments")
    content = models.TextField()
    likes_count = models.IntegerField(default=0, editable=False, verbose_name='Количество лайков')
    dislikes_count = models.IntegerField(default=0, editable=False, verbose_name='Количество дизлайков')
    rating = models.IntegerField(default=0, editable=False, verbose_name='Общий рейтинг')

    is_replied = models.BooleanField(default=False, editable=False, verbose_name="Есть ответы")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_replies')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    votes = GenericRelation(LikeDislike, related_query_name='comments')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created_at']

    def children(self):
        return Comment.objects.filter(parent=self)

    def __str__(self):
        return str(self.id)
