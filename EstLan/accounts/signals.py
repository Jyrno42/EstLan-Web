import logging
from django.core.cache import cache
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import User


def reset_user_avatar(user):
    logging.info('reset avatar cache: %s', user.id)
    cache.delete(User.AVATAR_CACHE_KEY % user.id)

@receiver(pre_save, sender=User)
def clear_avatar_post_email_change(sender, instance, **kwargs):
    if instance.id:
        old_user = User.objects.get(pk=instance.id)
        if old_user.email != instance.email:
            reset_user_avatar(instance)
