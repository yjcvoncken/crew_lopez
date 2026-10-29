from .models import SiteSettings, SiteImage

def site_content(request):
    return {'whatsapp_url': 'https://wa.me/393294535535', 'site': SiteSettings.objects.first(), 'site_images': {image.key: image for image in SiteImage.objects.all()}}
