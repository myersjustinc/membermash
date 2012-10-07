from django import template
from django.core.cache import cache

from ..models import Legislator

register = template.Library()

@register.inclusion_tag('legislators/custom_mash.html')
def custom_mash():
    cache_key = "custom_mash"
    cache_timeout = 60 * 60 * 24
    context = cache.get(cache_key)
    if context is None:
        legislators = Legislator.objects.filter(is_active=True).order_by(
            'last_name')
        context = {'legislators': legislators}
    
    return context
