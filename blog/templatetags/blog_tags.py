from ..models import Post,Category
from django import template

register = template.Library()

@register.simple_tag
def get_recent_post(num=6):
    return Post.objects.all()[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('create_time','month',order='DESC')

@register.simple_tag()
def get_categories():
    return Category.objects.all()