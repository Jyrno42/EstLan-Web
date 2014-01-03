from django.contrib import admin

from models import (Location, Article, ArticleCategory, SiteMenu, ObjectComment, CustomPage)

# Register our models
admin.site.register(Location)
admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(ObjectComment)
admin.site.register(SiteMenu)
admin.site.register(CustomPage)
