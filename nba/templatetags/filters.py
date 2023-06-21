from django import template
from datetime import date

register = template.Library()


@register.filter
def divide(value, arg):
    if arg != 0:
        return value / arg
    else:
        return None


@register.filter
def percent(value, arg):
    if arg != 0:
        return 100 * value / arg
    else:
        return None


@register.filter
def years_old(value):
    now = date.today()
    dif = now - value
    return dif.days // 365


register.filter("divide", divide)
register.filter("percent", percent)
register.filter("years_old", years_old)
