# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django_countries import CountryField
from tinymce.models import HTMLField

import datetime


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
    user = models.ForeignKey(User, related_name='+')

    comment = HTMLField()

    for_content_type = models.ForeignKey(ContentType)
    for_object_id = models.PositiveIntegerField()
    for_object = generic.GenericForeignKey('for_content_type', 'for_object_id')

    timestamp = models.DateTimeField(_("Timestamp"), default=datetime.datetime.utcnow)

    def __unicode__(self):
        return u"Comment by %s for %s" % (self.user.accountprofile.get_name(), self.for_object)


class Article(models.Model):
    title = models.CharField(_("Title"), max_length=100)

    short_text = HTMLField()
    content = HTMLField()

    cover_image = models.ImageField(_("Cover Image"), upload_to='cover_image', null=True, blank=True)
    publish_date = models.DateTimeField(_("Publish Date"), default=datetime.datetime.utcnow)

    slug = models.SlugField(max_length=100, unique=True, blank=True)
    author = models.ForeignKey(User, related_name='+')

    draft = models.BooleanField(_("Draft"), default=True)
    pinned = models.BooleanField(_("Pinned"), default=False)

    comments = generic.GenericRelation(ObjectComment, object_id_field='for_object_id', content_type_field='for_content_type')

    def __unicode__(self):
        return u"%s Article: %s" % ("Published" if not self.draft else 'Draft', self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('%d-%s' % (self.pk, self.title))
        super(Article, self).save(*args, **kwargs)

