from django import template
register = template.Library()

@register.filter(name='bootstrap_tags')
def bootstrap_tags(tags):
    return 'danger' if tags == 'error' else tags
    return 'success' if tags == 'success' else tags