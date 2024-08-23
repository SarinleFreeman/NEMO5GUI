from django import template
register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    attrs = {'class': arg}
    return value.as_widget(attrs=attrs)