from django import template

register = template.Library()


@register.filter  # register the template filter with django
def split_value(value):  # Only one argument.
    print('The value is %s with type %s' % (value, type(value)))
    return '' if value is None else value.split('|')
