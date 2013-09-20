# coding:utf-8
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.utils.timezone import datetime as d_datetime

from datetime import timedelta


class FrontPageView(TemplateView):
    template_name = 'Hulkify/base.html'

    def get(self, request, *args, **kwargs):
        articles = [
            {
                'id': 2,
                'name': 'FIFA Tournament',
                'short_text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                'publish_date': d_datetime.now(),
                'draft': False,
                'cover_image': None
            },
            {
                'id': 1,
                'name': 'Uus Web Live',
                'short_text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                'publish_date': d_datetime.now() - timedelta(days=7),
                'draft': False,
                'cover_image': None
            }
        ]


        return self.render_to_response(RequestContext(request, {
            'articles': articles
        }))


