from django import template
from todofamily.menu import menu
from django.utils import timezone

register = template.Library()


@register.inclusion_tag('todofamily/menu.html')
def show_menu(page=None):
    res = []
    if page:
        for i in menu:
            if page in i['view']:
                res.append(i)
    return {'menu': res}


@register.filter
def compare_date(date):
    if not date:
        return False
    return date < timezone.now()
