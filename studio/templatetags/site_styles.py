"""Keep the core design available even when static assets cannot be fetched."""
from pathlib import Path
from django import template
from django.utils.safestring import mark_safe

register = template.Library()
STYLESHEET = Path(__file__).resolve().parent.parent / 'static' / 'studio' / 'styles.css'

@register.simple_tag
def inline_site_styles():
    # This is a repository-owned stylesheet, never user-provided content.
    css = STYLESHEET.read_text(encoding='utf-8').replace('</style', '<\\/style')
    return mark_safe('<style id="crew-site-styles">' + css + '</style>')
