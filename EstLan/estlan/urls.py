from django.conf.urls import patterns, url

from estlan.views import FrontPageView


urlpatterns = patterns('estlan.views',
    url(r'^lan/all$', FrontPageView.as_view(), name="frontpage")
)