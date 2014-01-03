from django.conf.urls import patterns, include, url

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from views import FrontPageView, ArticleView, CustomPageView


admin.autodiscover()

urlpatterns = patterns(
    '',

    (r'^hulkify/', include(admin.site.urls)),
    (r'^hulkify/', include('admin_tools.urls')),
    (r'^ckeditor/', include('ckeditor.urls')),

    url(r'', include('accounts.urls')),

    # EstLan urls
    url(r'^$', FrontPageView.as_view(), name="frontpage"),

    url(r'^category/(?P<category_slug>[-\w]+)/?$', FrontPageView.as_view(), name="category"),

    url(r'^(?P<article_id>\d+)$', ArticleView.as_view(), name="article"),
    url(r'^article/(?P<article_slug>[-\w]+)/?$', ArticleView.as_view(), name="article_slug"),

    url(r'^page/(?P<page_id>\d+)$', CustomPageView.as_view(), name="page"),
    url(r'^p/(?P<page_slug>[-\w]+)/?$', CustomPageView.as_view(), name="page_slug"),
    # End: EstLan urls

    url('', include('social.apps.django_app.urls', namespace='social')),
    (r'^i18n/', include('django.conf.urls.i18n')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()
