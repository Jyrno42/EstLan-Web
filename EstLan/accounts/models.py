# -*- coding: utf-8 -*-
import httplib
import logging
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.templatetags.static import static

from social.apps.django_app.default.models import UserSocialAuth

import hashlib
import requests


def exists(url):
    try:
        r = requests.head(url)
        return r.status_code in [200, 301, 302,]
    except Exception:
        return False


class User(AbstractUser):
    AVATAR_CACHE_TIMEOUT = 60*60*24*5 # Cache for 5 days
    AVATAR_CACHE_KEY = 'user:avatar:%s'

    def __unicode__(self):
        return u"User: %s" % self.get_name()

    def get_name(self):
        if self.first_name:
            return self.get_full_name()
        else:
            return self.email

    def get_avatar(self):
        cache_key = self.AVATAR_CACHE_KEY % self.id
        avatar = cache.get(cache_key)

        if not avatar:
            try:
                auth = UserSocialAuth.objects.get(user=self, provider='facebook')
                avatar = "http://graph.facebook.com/%s/picture?type=large" % auth.uid
                assert exists(avatar)
            except UserSocialAuth.DoesNotExist:
                assert self.email
                m = hashlib.md5()
                m.update(self.email)
                avatar = "http://www.gravatar.com/avatar/%s" % m.hexdigest().lower()
                assert exists(avatar)
            except AssertionError:
                avatar = static('Hulkify/images/no_avatar.png')
            finally:
                cache.set(cache_key, avatar, timeout=self.AVATAR_CACHE_TIMEOUT)

        return avatar

