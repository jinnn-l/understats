#author: Wang Junwei (https://github.com/wjunwei2001/django_decision_tree/blob/main/questions/templatetags/index.py)

from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]