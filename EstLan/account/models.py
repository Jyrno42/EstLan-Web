from django.contrib.auth.models import User
from django.db import models

class AccountProfile(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u"Profile: %s" % self.get_name()

    def get_name(self):
        if self.user.first_name:
            return self.user.get_full_name()
        else:
            return self.user.email

