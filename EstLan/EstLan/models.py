# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField
from tinymce.models import HTMLField

from ckeditor.fields import RichTextField

from EstLan.utils import ARTICLE_CATEGORIES_CACHE_VERSION, ARTICLE_CATEGORIES_CACHE_KEY, reset_menu_cache, reset_custom_page_cache, reset_categories_cache, reset_featured_cache, reset_comment_count_cache


class Location(models.Model):
    name = models.CharField(_("Location Name"), max_length=100)
    description = models.TextField(_("Description"))

    website = models.URLField(_("Website"), blank=True)
    email = models.EmailField(_("Email"))
    phone = models.CharField(max_length=15, blank=True)

    addr_country_code = CountryField(_("Country"))
    addr_city = models.CharField(_("City"), max_length=50)
    addr_street = models.CharField(_("Street"), max_length=100)

    map_link = models.URLField(_("Map Link"))

    def __unicode__(self):
        return u"Location: %s" % self.name


class ObjectComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')

    comment = HTMLField()

    for_content_type = models.ForeignKey(ContentType)
    for_object_id = models.PositiveIntegerField()
    for_object = generic.GenericForeignKey('for_content_type', 'for_object_id')

    timestamp = models.DateTimeField(_("Timestamp"), default=datetime.datetime.utcnow)

    def __unicode__(self):
        return u"Comment by %s for %s" % (self.user.get_name(), self.for_object)

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        return super(ObjectComment, self).save(*args, **kwargs)


class ArticleCategory(models.Model):
    name = models.CharField(_('Category name'), max_length=30)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')

    def __unicode__(self):
        return u"Category %s" % (self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('%s' % (self.name))
        return super(ArticleCategory, self).save(*args, **kwargs)

    def get_children(self):
        return ArticleCategory.objects.filter(parent_id=self.id)


class Article(models.Model):
    title = models.CharField(_("Title"), max_length=100)

    short_text = RichTextField()
    content = RichTextField()

    cover_image = models.ImageField(_("Cover Image"), upload_to='cover_image', null=True, blank=True)
    publish_date = models.DateTimeField(_("Publish Date"), default=datetime.datetime.utcnow)

    slug = models.SlugField(max_length=100, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')

    draft = models.BooleanField(_("Draft"), default=True)
    pinned = models.BooleanField(_("Pinned"), default=False)

    comments = generic.GenericRelation(ObjectComment, object_id_field='for_object_id', content_type_field='for_content_type')

    categories = models.ManyToManyField(ArticleCategory)

    def __unicode__(self):
        return u"%s Article: %s" % ("Published" if not self.draft else 'Draft', self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('%d-%s' % (self.id if self.id else 1, self.title))
        return super(Article, self).save(*args, **kwargs)

    def get_categories(self):
        cache_key = ARTICLE_CATEGORIES_CACHE_KEY % self.id
        categories = cache.get(cache_key, version=ARTICLE_CATEGORIES_CACHE_VERSION)

        if categories is None:
            categories = self.categories.all()
            categories = cache.set(cache_key, categories, version=ARTICLE_CATEGORIES_CACHE_VERSION)

        return categories


class SiteMenu(models.Model):
    tag = models.CharField(_('Tag'), max_length=16, unique=True, blank=True)

    def __unicode__(self):
        return u"Menu %s" % self.tag

class CustomPage(models.Model):
    slug = models.CharField(_('Slug'), max_length=100, unique=True, blank=True)
    title = models.CharField(_('title'), max_length=200)
    content = RichTextField(_('content'), blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', blank=True, null=True)
    menu = models.ForeignKey(SiteMenu, related_name='+')

    draft = models.BooleanField(_("Draft"), default=True)
    order = models.PositiveIntegerField()

    url = models.URLField('URL', blank=True, null=True)

    def __unicode__(self):
        return u"Page: %s at /%s" % (self.title, self.slug)

    @models.permalink
    def get_absolute_url(self):
        if self.slug:
            return ("page_slug", [self.slug,])
        else:
            return ("page", [self.id,])


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
