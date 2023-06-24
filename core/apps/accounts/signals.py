from .models import Account, Profile, PhoneCodeVerification
from django.db.models.signals import post_save
from django.dispatch import receiver


# Автоматическое создание профиля пользователя для новых пользователей
@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(account=instance)
        PhoneCodeVerification.objects.create(account=instance)
