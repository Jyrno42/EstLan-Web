from django.contrib import admin
from django.contrib.flatpages.models import FlatPage

from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld

from django import forms
from tinymce import widgets as tinymce_widgets

from django.contrib import admin

from models import *

admin.site.register(Location)
admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(ObjectComment)

class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=tinymce_widgets.AdminTinyMCE())
    class Meta:
        model = FlatPage # this is not automatically inherited from FlatpageFormOld


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


# We have to unregister the normal admin, and then reregister ours
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
