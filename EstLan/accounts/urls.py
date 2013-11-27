from django.conf.urls import patterns, url
from django.contrib.auth.views import logout_then_login


urlpatterns = patterns(
    'accounts.views',
    #url(r'^login/', 'login', name='login'),
    url(r'^logout/', logout_then_login, name='logout'),
)
