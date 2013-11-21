# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __unicode__(self):
        return u"User: %s" % self.get_name()

    def get_name(self):
        if self.first_name:
            return self.get_full_name()
        else:
            return self.email