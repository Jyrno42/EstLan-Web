from django.contrib.auth import get_user_model
from django.contrib.auth.views import login as django_login
from django.views.generic import DetailView

from accounts.forms import LoginForm


class ProfileView(DetailView):
    """Displays the Profile of a user"""
    model = get_user_model()
    template_name = 'accounts/profile.html'
    pk_url_kwarg = 'profile_id'
    slug_url_kwarg = 'profile_slug'


def login(request):
    response = django_login(request, template_name='accounts/login.html', authentication_form=LoginForm)

    return response
