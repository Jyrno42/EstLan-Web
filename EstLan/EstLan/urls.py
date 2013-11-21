from django.conf.urls import patterns, include, url

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from views import FrontPageView, ArticleView


admin.autodiscover()

urlpatterns = patterns(
    '',

    (r'^hulkify/', include(admin.site.urls)),
    (r'^hulkify/', include('admin_tools.urls')),

    url(r'', include('accounts.urls')),

    # EstLan urls
    url(r'^$', FrontPageView.as_view(), name="frontpage"),

    url(r'^category/(?P<category_slug>[-\w]+)/?$', FrontPageView.as_view(), name="category"),

    url(r'^(?P<article_id>\d+)$', ArticleView.as_view(), name="article"),
    url(r'^article/(?P<article_slug>[-\w]+)/?$', ArticleView.as_view(), name="article_slug"),
    # End: EstLan urls

    url('', include('social.apps.django_app.urls', namespace='social')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()
