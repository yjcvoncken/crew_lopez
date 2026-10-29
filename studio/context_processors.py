from .models import SiteSettings, SiteImage, ContentText

def site_content(request):
    return {'page_text': page_text_content(request), 'whatsapp_url': 'https://wa.me/393294535535', 'site': SiteSettings.objects.first(), 'site_images': {image.key: image for image in SiteImage.objects.all()}}


def page_text_content(request):
    if not hasattr(request, '_page_text_content'):
        request._page_text_content = {item['key']: item for item in ContentText.objects.values('key', 'text', 'default_text')}
    return request._page_text_content
