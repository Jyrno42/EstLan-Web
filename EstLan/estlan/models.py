# -*- coding: utf-8 -*-

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


class Article(models.Model):
    title = models.CharField(_("Title"), max_length=100)

    short_text = HTMLField()
    content = HTMLField()

    cover_image = models.ImageField(_("Cover Image"), upload_to='cover_image', null=True, blank=True)

    draft = models.BooleanField(_("Draft"), default=True)
    publish_date = models.DateTimeField(_("Publish Date"), default=datetime.datetime.utcnow)

    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __unicode__(self):
        return u"%s Article: %s" % ("Published" if not self.draft else 'Draft', self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('%d-%s' % (self.pk, self.title))
        super(Article, self).save(*args, **kwargs)

