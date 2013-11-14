from django.conf.urls import patterns, url

from estlan.views import FrontPageView, ArticleView


urlpatterns = patterns('estlan.views',
    url(r'^$', FrontPageView.as_view(), name="frontpage"),

    url(r'^category/(?P<category_slug>[-\w]+)/?$', FrontPageView.as_view(), name="category"),

    url(r'^(?P<article_id>\d+)$', ArticleView.as_view(), name="article"),
    url(r'^article/(?P<article_slug>[-\w]+)/?$', ArticleView.as_view(), name="article_slug"),
)
