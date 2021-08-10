from django import template
register = template.Library()

@register.filter
def next(some_list, current_index):
    try:
        return some_list[int(current_index)%4]
    except:
        return ''