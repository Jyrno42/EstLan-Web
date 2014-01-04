from django import template

from EstLan.utils import sanitize_html, fix_html as utils_fix_html

register = template.Library()


def short_text(value):
    return sanitize_html(value, tags='i strong b u a')


def fix_html(value):
    return utils_fix_html(value)


def comment_text(value):
    return sanitize_html(value, tags='p i strong b u a pre br', attrs='href')

register.filter('short_text', short_text)
register.filter('fix_html', fix_html)
register.filter('comment_text', comment_text)