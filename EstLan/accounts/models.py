# -*- coding: utf-8 -*-
import logging
import hashlib

from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from social.apps.django_app.default.models import UserSocialAuth
import requests


def exists(url):
    try:
        r = requests.head(url)
        return r.status_code in [200, 301, 302,]
    except Exception:
        return False


class EstLanUser(AbstractUser):
    AVATAR_CACHE_TIMEOUT = 60*60*24*5 # Cache for 5 days
    AVATAR_CACHE_KEY = 'user:avatar:%s'
    AVATAR_CACHE_VERSION = 2

    GENDER_MALE = u'm'
    GENDER_FEMALE = u'f'

    GENDER_CHOICES = (
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female')),
    )

    AVATAR_TYPE_NONE = u'no'
    AVATAR_TYPE_FACEBOOK = u'fb'
    AVATAR_TYPE_GRAVATAR = u'gr'

    AVATAR_TYPE_CHOICES = (
        (AVATAR_TYPE_NONE, _('No Avatar')),
        (AVATAR_TYPE_FACEBOOK, _('Facebook Profile Image')),
        (AVATAR_TYPE_GRAVATAR, _('Gravatar')),
    )

    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES, default=GENDER_MALE)
    date_of_birth = models.DateField(_('Birthday'), null=True, blank=True)

    slug = models.SlugField(max_length=16, unique=True, blank=True)

    selected_avatar = models.CharField(_('Avatar'), max_length=2, choices=AVATAR_TYPE_CHOICES,
                                       default=AVATAR_TYPE_FACEBOOK)

    show_email = models.BooleanField(_('Show Email in public profile'), default=True)
    show_age = models.BooleanField(_('Show Age in public profile'), default=True)

    def __unicode__(self):
        return u"User: %s" % self.get_name()

    def get_name(self):
        if self.first_name:
            return self.get_full_name()
        else:
            return self.email

    def get_avatar(self):
        cache_key = self.AVATAR_CACHE_KEY % self.id
        avatar = cache.get(cache_key, version=self.AVATAR_CACHE_VERSION)
        avatar_choice = self.selected_avatar

        cached_type = avatar.get('avatar_choice') if avatar else None

        if not avatar or (cached_type != avatar_choice):
            avatar = {
                'image': None,
                'avatar_choice': avatar_choice,
            }

            if avatar_choice == self.AVATAR_TYPE_FACEBOOK:
                try:
                    auth = UserSocialAuth.objects.get(user=self, provider='facebook')
                    avatar['image'] = "http://graph.facebook.com/%s/picture?type=large" % auth.uid
                    avatar['avatar_choice'] = avatar_choice
                    assert exists(avatar['image'])
                except (UserSocialAuth.DoesNotExist, AssertionError):
                    pass

            if avatar_choice == self.AVATAR_TYPE_GRAVATAR:
                try:
                    assert self.email
                    m = hashlib.md5()
                    m.update(self.email)
                    avatar['image'] = "http://www.gravatar.com/avatar/%s?s=159" % m.hexdigest().lower()
                    avatar['avatar_choice'] = avatar_choice
                    assert exists(avatar['image'])
                except AssertionError:
                    pass

            if not avatar:
                avatar = {
                    'image': static('Hulkify/images/no_avatar.png'),
                    'avatar_choice': self.AVATAR_TYPE_NONE,
                }
                self.selected_avatar = self.AVATAR_TYPE_NONE
                self.save()

            cache.set(cache_key, avatar, timeout=self.AVATAR_CACHE_TIMEOUT, version=self.AVATAR_CACHE_VERSION)

        return avatar.get('image')

    @models.permalink
    def get_absolute_url(self):
        if self.slug:
            return "profile_slug", [self.slug, ]
        else:
            return "profile_id", [self.pk, ]


def reset_user_avatar(user):
    logging.info('reset avatar cache: %s', user.id)
    cache.delete(EstLanUser.AVATAR_CACHE_KEY % user.id)


@receiver(pre_save, sender=EstLanUser)
def clear_avatar_post_email_change(sender, instance, **kwargs):
    if instance.id:
        old_user = EstLanUser.objects.get(pk=instance.id)
        if old_user.email != instance.email:
            reset_user_avatar(instance)