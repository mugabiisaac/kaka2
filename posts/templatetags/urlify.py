from urllib import quote_plus
from django import template

register = template.Library()


@register.filter
def urlify(value):
    return quote_plus(value)

template.add_to_builtins('sorl.thumbnail.templatetags.thumbnail')
