from django import template
from django.templatetags.static import static

register = template.Library()


@register.simple_tag(takes_context=True)
def site_image(context, key):
    image = context.get('site_images', {}).get(key)
    return image.image.url if image and image.image else static(key)
