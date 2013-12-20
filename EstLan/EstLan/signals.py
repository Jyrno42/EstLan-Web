import logging
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from EstLan.models import CustomPage, Article, ObjectComment
from EstLan.utils import (reset_menu_cache, reset_custom_page_cache, reset_featured_cache,
                          reset_comment_count_cache, reset_categories_cache)


@receiver(pre_save, sender=CustomPage)
def pre_custom_page_save(sender, instance, **kwargs):
    reset_menu_cache(instance.menu.tag)
    reset_custom_page_cache(instance)


@receiver(pre_delete, sender=CustomPage)
def pre_custom_page_delete(sender, instance, **kwargs):
    reset_menu_cache(instance.menu.tag)
    reset_custom_page_cache(instance)

@receiver(pre_save, sender=Article)
def pre_article_save(sender, instance, **kwargs):
    old_instance = None

    if instance.id:
        old_instance = Article.objects.get(pk=instance.id)
        reset_categories_cache(instance.id)

    if instance.pinned or (old_instance and instance.pinned != old_instance.pinned):
        reset_featured_cache()

@receiver(pre_delete, sender=Article)
def pre_article_delete(sender, instance, **kwargs):
    if instance.pinned:
        reset_featured_cache()
    reset_categories_cache(instance.id)

@receiver(pre_save, sender=ObjectComment)
def pre_object_comment_save(sender, instance, **kwargs):
    if str(instance.for_content_type) == 'article':
        reset_comment_count_cache(instance.for_object_id)

@receiver(pre_delete, sender=ObjectComment)
def pre_object_comment_delete(sender, instance, **kwargs):
    if str(instance.for_content_type) == 'article':
        reset_comment_count_cache(instance.for_object_id)
