# -*- coding: utf-8 -*-

from django.db import models
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

    draft = models.BooleanField(_("Draft"), default=True)
    publish_date = models.DateTimeField(_("Publish Date"), default=datetime.datetime.utcnow)

    def __unicode__(self):
        return u"%s Article: %s" % ("Published" if not self.draft else 'Draft', self.title)

