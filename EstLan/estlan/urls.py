from django.conf.urls import patterns, url

from estlan.views import FrontPageView


urlpatterns = patterns('estlan.views',
    url(r'^$', FrontPageView.as_view(), name="frontpage")
)
