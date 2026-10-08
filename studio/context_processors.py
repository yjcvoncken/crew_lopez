from .models import SiteSettings

def site_content(request):
    return {'site': SiteSettings.objects.first()}
