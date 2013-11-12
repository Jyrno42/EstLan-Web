# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils import timezone


class NotClosedObjectsManager(models.Manager):
    """ Utility manager that excludes items that have non-null closed_by value
    """
    def get_query_set(self):
        return super(NotClosedObjectsManager, self).get_query_set().filter(closed_by=None)

class ClosableModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    created_timestamp = models.DateTimeField(default=timezone.now)

    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', null=True, blank=True)
    closed_timestamp = models.DateTimeField(null=True, blank=True)

    all_objects = models.Manager()
    objects = NotClosedObjectsManager()

    class Meta:
        abstract = True

