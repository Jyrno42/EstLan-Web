# coding:utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.utils.timezone import datetime as d_datetime
from django.views.generic.base import TemplateView

from estlan.models import Article

from datetime import timedelta


class FrontPageView(TemplateView):
    template_name = 'Hulkify/base.html'
    ARTICLES_PER_PAGE = 1

    def get(self, request, *args, **kwargs):
        articles_list = Article.objects.filter(draft=False).order_by('publish_date')
        paginator = Paginator(articles_list, self.ARTICLES_PER_PAGE)

        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        '''
        articles = [    {
                'id': 2,
                'title': 'FIFA Tournament',
                'short_text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                'publish_date': d_datetime.now(),
                'draft': False,
                'cover_image': None
            },
            {
                'id': 1,
                'title': 'Uus Web Live',
                'short_text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                'publish_date': d_datetime.now() - timedelta(days=7),
                'draft': False,
                'cover_image': None
            }
        ]
        '''

        return self.render_to_response(RequestContext(request, {
            'articles': articles
        }))


