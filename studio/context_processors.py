from .models import SiteSettings, SiteImage

def site_content(request):
    return {'site': SiteSettings.objects.first(), 'site_images': {image.key: image for image in SiteImage.objects.all()}}
