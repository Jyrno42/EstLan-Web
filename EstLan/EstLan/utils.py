from EstLan.models import SiteMenu, CustomPage


def get_menu_items(tag='TOP'):
    try:
        menu = SiteMenu.objects.get(tag__iexact=tag)
        return CustomPage.objects.filter(menu=menu).exclude(draft=True).order_by('order')
    except SiteMenu.DoesNotExist:
        return []
