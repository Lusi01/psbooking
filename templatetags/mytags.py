from django import template

register = template.Library()

##
# Ключевые слова Python 3:
# and, as, assert, break, class, continue,
# def, del, elif, else, except,
# False, finally, for, from, global,
# if, import, in, is, lambda, None,
# nonlocal, not, or, pass,
# raise, return, True, try, while, with, yield
##

@register.simple_tag
def changeStatement(status):
    return not status


@register.filter
def plural_ttt(value, arg="отзыв,отзыва,отзывов"):
    args = arg.split(",")
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]
