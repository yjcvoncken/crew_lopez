from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html
from .models import SiteSettings, SiteImage, Room, Activity, BlogPost
from .image_widgets import ImageAdminForm

@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    form = ImageAdminForm
    list_display = ['picture', 'name']
    list_display_links = ['picture', 'name']
    search_fields = ['name', 'key']
    fields = ['name', 'image']
    @admin.display(description='Current picture')
    def picture(self, obj):
        url = obj.image.url if obj.image else static(obj.key)
        return format_html('<img src="{}" alt="{}" style="width:140px;height:90px;object-fit:contain;background:#f6f3eb;border-radius:8px">', url, obj.name)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = ImageAdminForm
    fieldsets = [('Homepage & assets', {'fields': ('hero_title', 'hero_description', 'homepage_photo', 'graphic_element', 'booking_url')}), ('Business & contact', {'fields': ('business_name', 'registration_number', 'business_address', 'contact_email', 'contact_phone')}), ('Policies', {'fields': ('policies_approved', 'privacy_text', 'cookie_text', 'terms_text')})]
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    form = ImageAdminForm
    list_display = ['name', 'order']
    list_editable = ['order']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    form = ImageAdminForm
    list_display = ['name', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ['name']}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'order']
    list_editable = ['published', 'order']
    search_fields = ['title', 'body']

admin.site.site_header = 'Crew Lopez - Website admin'
admin.site.site_title = 'Crew Lopez'
