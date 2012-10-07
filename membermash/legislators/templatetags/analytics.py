from django import template

import os

register = template.Library()

@register.inclusion_tag('legislators/analytics.html')
def analytics():
    return {
        "GOOGLE_ANALYTICS_ID": os.environ.get("GOOGLE_ANALYTICS_ID", ''),
    }
