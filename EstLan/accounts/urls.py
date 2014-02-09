from django.conf.urls import patterns, url
from django.contrib.auth.views import logout_then_login

from views import ProfileView


urlpatterns = patterns(
    'accounts.views',
    #url(r'^login/', 'login', name='login'),
    url(r'^profile/(?P<profile_id>\d+)/', ProfileView.as_view(), name='profile_id'),
    url(r'^profile/(?P<profile_slug>[A-Za-z0-9\-\_]+)/', ProfileView.as_view(), name='profile_slug'),

    url(r'^logout/', logout_then_login, name='logout'),
)
