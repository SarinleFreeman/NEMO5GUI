from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    if hasattr(value, 'field'):
        css_classes = value.field.widget.attrs.get('class', '')
        css_classes += ' ' + arg
        value.field.widget.attrs['class'] = css_classes
        return value
    else:
        return value  # Return the original value if it's not a form field