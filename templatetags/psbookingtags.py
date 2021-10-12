from django import template
from django.template import defaultfilters
from utils.text import plural_form

register = template.Library()


@register.filter
def psbookingdate(date):
    return defaultfilters.date(date, "d.m.Y г.")


@register.filter
def pluralo(value, arg):
    args = arg.split(",")
    return plural_form(value, args[0], args[1], args[2])
