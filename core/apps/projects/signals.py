import os
from django.core.cache import caches
from django.conf import settings
from .models import Category, Attachment, Link, LikeDislike, Comment, Project
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save
from django.core.exceptions import ObjectDoesNotExist, ValidationError


@receiver(post_delete, sender=Category)
def auto_delete_icon_on_delete(sender, instance, **kwargs):
    """
    Удаляет файлы/фото из дериктории после удаления файла из модели. И удаляет дерикторию если она пустая
    """
    caches['category_cache'].clear()

    if instance.icon:
        if os.path.isfile(instance.icon.path):
            if not instance.icon.path == '\\'.join([str(settings.MEDIA_ROOT), 'categories\default_category_icon.png']):
                os.remove(instance.icon.path)
            dir_name = '/'.join([str(settings.MEDIA_ROOT), 'categories', str(instance.slug)])
            if os.path.exists(dir_name) and os.path.isdir(dir_name):
                if not os.listdir(dir_name):
                    os.rmdir(dir_name)


@receiver(pre_save, sender=Category)
def auto_delete_icon_on_change(sender, instance, **kwargs):
    """
    Удаляет файлы/фото из дериктории после изменения файла в модели
    """
    if instance.pk is None:
        return False

    try:
        category = sender.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return False

    if category.icon:
        old_file = category.icon
        if old_file:
            new_file = instance.icon
            if not old_file == new_file:
                if not old_file.path == '\\'.join([str(settings.MEDIA_ROOT), 'categories\default_category_icon.png']):
                    if os.path.isfile(old_file.path):
                        os.remove(old_file.path)


@receiver(post_save, sender=Category)
def auto_clear_category_cache(sender, instance, created, **kwargs):
    """
    Удаляем кэш категорий
    """
    caches['category_cache'].clear()


@receiver(post_delete, sender=Attachment)
def auto_delete_file_on_delete_attachment(sender, instance, **kwargs):
    """
    Удаляет файлы/фото из директории после удаления файла из модели. И удаляет директорию если она пустая
    """
    caches['project_cache'].clear()
    if instance.uploaded_file:
        if os.path.isfile(instance.uploaded_file.path):
            os.remove(instance.uploaded_file.path)
            dir_name = '/'.join([str(settings.MEDIA_ROOT), 'projects', str(instance.project.pk), 'attachments', ])
            dir_name_project = '/'.join([str(settings.MEDIA_ROOT), 'projects', str(instance.project.pk)])
            if os.path.exists(dir_name) and os.path.isdir(dir_name):
                if not os.listdir(dir_name):
                    os.rmdir(dir_name)
                    if os.path.exists(dir_name_project) and os.path.isdir(dir_name_project):
                        if not os.listdir(dir_name_project):
                            os.rmdir(dir_name_project)


@receiver(pre_save, sender=Attachment)
def auto_delete_file_on_change_attachment(sender, instance, **kwargs):
    """
    Удаляет файлы/фото из директории после изменения файла в модели
    Не даёт сохранить больше определенного количества файлов
    """
    if instance.pk is None:
        return False

    try:
        old_object = sender.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        if sender.objects.filter(
                project=instance.project).count() >= settings.MAX_NUMBER_OF_ATTACHMENTS_PER_PROJECT:
            raise ValidationError(
                "Максимальное количество файлов %s " % settings.MAX_NUMBER_OF_ATTACHMENTS_PER_PROJECT)
        return False
    if old_object.uploaded_file:
        old_file = old_object.uploaded_file
        new_file = instance.uploaded_file
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
                if not new_file:
                    dir_name = '/'.join(
                        [str(settings.MEDIA_ROOT), 'projects', str(instance.project.pk), 'attachments'])
                    dir_name_project = '/'.join([str(settings.MEDIA_ROOT), 'projects', str(instance.project.pk)])
                    if os.path.exists(dir_name) and os.path.isdir(dir_name):
                        if not os.listdir(dir_name):
                            os.rmdir(dir_name)
                            if os.path.exists(dir_name_project) and os.path.isdir(dir_name_project):
                                if not os.listdir(dir_name_project):
                                    os.rmdir(dir_name_project)


@receiver(post_save, sender=Attachment)
def auto_clear_cache_after_attachment_save(sender, instance, created, **kwargs):
    """
    Очищаем кэш
    """
    caches['project_cache'].clear()


@receiver(pre_save, sender=Link)
def auto_stop_save_if_over_limit_link(sender, instance, **kwargs):
    """
    Не даёт сохранить больше определенного ссылок
    """
    if instance.pk is None:
        return False

    try:
        obj = sender.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        if sender.objects.filter(
                project=instance.project).count() >= settings.MAX_NUMBER_OF_LINKS_PER_PROJECT:
            raise ValidationError(
                "Максимальное количество ссылок %s " % settings.MAX_NUMBER_OF_LINKS_PER_PROJECT)
        return False


@receiver(post_delete, sender=Link)
def auto_clear_cache_after_link_delete(sender, instance, **kwargs):
    """
    Чистим кэш
    """
    caches['project_cache'].clear()


@receiver(post_save, sender=Link)
def auto_clear_cache_after_link_save(sender, instance, created, **kwargs):
    """
    Очищаем кэш
    """
    caches['project_cache'].clear()


@receiver(pre_save, sender=LikeDislike)
def auto_vote_count_on_save(sender, instance, **kwargs):
    """
    Автоматически считаем лайки, дизлайки и общий рейтинг до сохранения
    """
    if instance.pk is None:
        return False

    obj = instance.content_object
    if obj is None:
        raise ValidationError("Объекта не существует")

    try:
        prev_like = sender.objects.get(pk=instance.pk)
        if prev_like.vote > 0 and instance.vote < 0:
            obj.rating -= 2
            obj.likes_count -= 1
            obj.dislikes_count += 1
            obj.save()
        if prev_like.vote < 0 and instance.vote > 0:
            obj.rating += 2
            obj.likes_count += 1
            obj.dislikes_count -= 1
            obj.save()

    except ObjectDoesNotExist:
        obj.rating += instance.vote
        if instance.vote > 0:
            obj.likes_count += 1
        else:
            obj.dislikes_count += 1
        obj.save()


@receiver(post_delete, sender=LikeDislike)
def auto_vote_count_on_delete(sender, instance, **kwargs):
    """
    Пересчитывает количество лайков и дизлайков у объекта после удаления лайка
    """
    obj = instance.content_object
    if obj is None:
        return False

    obj.rating -= instance.vote
    if instance.vote > 0:
        obj.likes_count -= 1
    else:
        obj.dislikes_count -= 1
    obj.save()


@receiver(post_delete, sender=Comment)
def auto_check_replies_after_delete(sender, instance, **kwargs):
    """
    Проверяет есть ли ответы на комментарий после удаления ответа
    """
    if instance.parent is not None:
        if Comment.objects.filter(parent=instance.parent):
            instance.parent.is_replied = True
            instance.parent.save()
        else:
            instance.parent.is_replied = False
            instance.parent.save()


@receiver(post_save, sender=Comment)
def auto_check_is_replied_true_after_save(sender, instance, created, **kwargs):
    """
    Устанавливаем is_replied: True если комментарий является ответом
    """
    if created:
        if instance.parent is not None:
            instance.parent.is_replied = True
            instance.parent.save()


@receiver(post_save, sender=Project)
def auto_clear_cache_after_project_save(sender, instance, created, **kwargs):
    """
    Очищаем кэш
    """
    caches['project_cache'].clear()


@receiver(post_delete, sender=Project)
def auto_clear_cache_after_project_delete(sender, instance, **kwargs):
    """
    Очищаем кэш
    """
    caches['project_cache'].clear()
