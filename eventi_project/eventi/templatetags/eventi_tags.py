from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def page_url(context, page_number):
    """Generate pagination URL while preserving all other query parameters"""
    request = context["request"]
    query_dict = request.GET.copy()
    query_dict["page"] = page_number

    return f"?{query_dict.urlencode()}"
