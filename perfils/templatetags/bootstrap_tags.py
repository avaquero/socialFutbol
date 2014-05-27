from django import template
register = template.Library()

@register.assignment_tag
def bootstrap_tags(tags):
    return 'danger' if tags == 'error' else tags
    return 'success' if tags == 'success' else tags
    return 'notice' if tags == 'info' else tags