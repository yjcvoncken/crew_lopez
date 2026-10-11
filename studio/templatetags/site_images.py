from django import template
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from functools import lru_cache


@lru_cache(maxsize=128)
def bundled_image(key):
    optimized = key.rsplit(".", 1)[0] + ".webp"
    return optimized if finders.find(optimized) else key

register = template.Library()


@register.simple_tag(takes_context=True)
def site_image(context, key):
    image = context.get('site_images', {}).get(key)
    return image.image.url if image and image.image else static(bundled_image(key))
