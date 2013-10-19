# coding:utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template import RequestContext
from django.utils.timezone import datetime as d_datetime
from django.shortcuts import get_object_or_404
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

        return self.render_to_response(RequestContext(request, {
            'articles': articles
        }))


class ArticleView(TemplateView):
    template_name = 'Hulkify/article.html'
    ARTICLES_PER_PAGE = 1

    def dispatch(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id', None)
        article_slug = kwargs.get('article_slug', None)

        if article_slug:
            article = get_object_or_404(Article, slug=article_slug)
        elif article_id:
            article = get_object_or_404(Article, id=article_id)
        else:
            raise Http404

        return self.render_to_response(RequestContext(request, {
            'article': article
        }))


