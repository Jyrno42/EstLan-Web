# coding:utf-8
from django.contrib.flatpages.models import FlatPage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template import RequestContext
from django.utils.timezone import datetime
from django.utils.translation import ugettext
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from estlan.models import Article, ArticleCategory


class FrontPageView(TemplateView):
    template_name = 'Hulkify/base.html'
    ARTICLES_PER_PAGE = 15

    def handle_cat(self, categories):
        ret = list()

        for cat in categories:
            inner = {
                'item': cat,
                'children': list()
            }
            child = cat.get_children()
            if child:
                inner['children'] = self.handle_cat(child)
            ret.append(inner)
        return ret

    def get(self, request, *args, **kwargs):
        queryset = Article.objects.filter(draft=False).order_by('-publish_date')

        featured_posts = queryset.filter(pinned=True).exclude(cover_image=None)

        cat_slug = kwargs.get('category_slug', False)
        if cat_slug:
            queryset = queryset.filter(categories__slug=cat_slug)

        paginator = Paginator(queryset, self.ARTICLES_PER_PAGE)

        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        for article in articles:
            setattr(article, 'comment_count', article.comments.all().count())

        categories = self.handle_cat(ArticleCategory.objects.filter(parent=None).order_by('name'))

        return self.render_to_response(RequestContext(request, {
            'articles': articles,
            'categories': categories,
            'featured_posts': featured_posts,
        }))


class ArticleView(TemplateView):
    template_name = 'Hulkify/article_view.html'
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

        try:
            comment_desc = FlatPage.objects.get(url=ugettext('/comments/description/'))
        except FlatPage.DoesNotExist:
            comment_desc = None

        return self.render_to_response(RequestContext(request, {
            'article': article,
            'comment_desc': comment_desc,
        }))


