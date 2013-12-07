# coding:utf-8
from django.db.models import Q
from django.contrib.flatpages.models import FlatPage
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.utils.timezone import datetime
from django.utils.translation import ugettext
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from EstLan.forms import ArticleCommentForm
from EstLan.models import Article, ArticleCategory, CustomPage
from EstLan.utils import get_menu_items


class FrontPageView(TemplateView):
    template_name = 'Hulkify/base.html'
    ARTICLES_PER_PAGE = 15

    @staticmethod
    def handle_cat(categories):
        ret = list()

        for cat in categories:
            inner = {
                'item': cat,
                'children': list()
            }
            child = cat.get_children()
            if child:
                inner['children'] = FrontPageView.handle_cat(child)
            ret.append(inner)
        return ret

    def get(self, request, *args, **kwargs):
        queryset = Article.objects.filter(draft=False).order_by('-publish_date')

        # Fixes #10
        featured_posts = queryset.filter(pinned=True).exclude(cover_image__isnull=True, cover_image='')
        featured_posts = filter(lambda x: x.cover_image.name != '', featured_posts)

        query = request.GET.get('query', '')

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(short_text__icontains=query) | Q(content__icontains=query))

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

        categories = FrontPageView.handle_cat(ArticleCategory.objects.filter(parent=None).order_by('name'))

        return self.render_to_response(RequestContext(request, {
            'articles': articles,
            'categories': categories,
            'featured_posts': featured_posts,
            'show_hero_unit': not query and not cat_slug,
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

        form = ArticleCommentForm(data=request.POST or None, user=request.user, article=article)

        if request.POST:
            if form.is_valid():
                form.save()

                return HttpResponseRedirect(reverse('article', kwargs={'article_id': article.id}))

        try:
            comment_desc = FlatPage.objects.get(url=ugettext('/comments/description/'))
        except FlatPage.DoesNotExist:
            comment_desc = None

        categories = FrontPageView.handle_cat(ArticleCategory.objects.filter(parent=None).order_by('name'))

        return self.render_to_response(RequestContext(request, {
            'article': article,
            'comment_desc': comment_desc,
            'comments': article.comments.all().order_by('-timestamp'),
            'categories': categories,
            'form': form,
        }))


class CustomPageView(TemplateView):
    template_name = 'flatpages/default.html'

    def dispatch(self, request, *args, **kwargs):
        page_id = kwargs.get('page_id', None)
        page_slug = kwargs.get('page_slug', None)

        if page_slug:
            page = get_object_or_404(CustomPage, slug=page_slug)
        elif page_id:
            page = get_object_or_404(CustomPage, id=page_id)
        else:
            raise Http404

        categories = FrontPageView.handle_cat(ArticleCategory.objects.filter(parent=None).order_by('name'))

        return self.render_to_response(RequestContext(request, {
            'flatpage': page,
            'categories': categories,
        }))
