from django import template

from EstLan.utils import get_menu_items


register = template.Library()

def show_menu(context, tag):
    return {'menu_items': get_menu_items(tag), 'path': context['request'].path}
register.inclusion_tag('menu_item.html', takes_context=True)(show_menu)