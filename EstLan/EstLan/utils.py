import logging
from bs4 import BeautifulSoup, Comment

from django.core.cache import cache


MENU_CACHE_KEY = 'EstLan:menu:%s'
MENU_CACHE_VERSION = 2

CUSTOM_PAGE_CACHE_KEY_ID = 'EstLan:custom_page:id:%s'
CUSTOM_PAGE_CACHE_KEY_SLUG = 'EstLan:custom_page:slug:%s'
CUSTOM_PAGE_CACHE_VERSION = 2

FEATURED_POSTS_CACHE_KEY = 'EstLan:featured:posts'
FEATURED_POSTS_CACHE_VERSION = 1

COMMENT_COUNT_CACHE_KEY = 'EstLan:article:comment:count:%s'
COMMENT_COUNT_CACHE_VERSION = 1

ARTICLE_CATEGORIES_CACHE_KEY = 'EstLan:article:categories:%s'
ARTICLE_CATEGORIES_CACHE_VERSION = 1

CATEGORIES_CACHE_KEY = 'EstLan:categories:list'
CATEGORIES_CACHE_VERSION = 1

def reset_menu_cache(tag):
    logging.info('reset menu cache: %s', tag)
    cache.delete(MENU_CACHE_KEY % tag, version=MENU_CACHE_VERSION)

def reset_custom_page_cache(instance):
    logging.info('reset custom page cache: %s', instance.id)
    cache.delete(CUSTOM_PAGE_CACHE_KEY_ID % instance.id, version=CUSTOM_PAGE_CACHE_VERSION)
    cache.delete(CUSTOM_PAGE_CACHE_KEY_SLUG % instance.slug, version=CUSTOM_PAGE_CACHE_VERSION)

def reset_featured_cache():
    logging.info('reset featured cache')
    cache.delete(FEATURED_POSTS_CACHE_KEY, version=FEATURED_POSTS_CACHE_VERSION)

def reset_comment_count_cache(instance_id):
    logging.info('reset comment count cache: %s', instance_id)
    cache.delete( COMMENT_COUNT_CACHE_KEY % instance_id, version=COMMENT_COUNT_CACHE_VERSION)

def reset_categories_cache(instance_id):
    logging.info('reset categories cache: %s', instance_id)
    cache.delete( ARTICLE_CATEGORIES_CACHE_KEY % instance_id, version=ARTICLE_CATEGORIES_CACHE_VERSION)

def get_menu_items(tag='TOP'):
    from EstLan.models import SiteMenu, CustomPage
    cache_key = MENU_CACHE_KEY % tag

    menu = cache.get(cache_key, version=MENU_CACHE_VERSION)

    if not menu:
        try:
            menu = SiteMenu.objects.get(tag__iexact=tag)
            menu = CustomPage.objects.filter(menu=menu).exclude(draft=True).order_by('order')
        except SiteMenu.DoesNotExist:
            menu = []

    if menu is not None:
        cache.set(cache_key, menu, version=MENU_CACHE_VERSION)

    return menu

def sanitize_html(value, tags='p i strong b u a h1 h2 h3 pre br img', attrs='href src'):
    valid_tags = tags.split()
    valid_attrs = attrs.split()
    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True

        tag.attrs = dict((attr, val) for attr, val in tag.attrs.items() if attr in valid_attrs)
    return soup.renderContents().decode('utf8').replace('javascript:', '')
