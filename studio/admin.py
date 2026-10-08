from django.contrib import admin
from .models import SiteSettings, Room, Activity, BlogPost

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [('Homepage & assets', {'fields': ('hero_title', 'hero_description', 'homepage_photo', 'graphic_element', 'booking_url')}), ('Business & contact', {'fields': ('business_name', 'registration_number', 'business_address', 'contact_email', 'contact_phone')}), ('Policies', {'fields': ('policies_approved', 'privacy_text', 'cookie_text', 'terms_text')})]
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ['name']}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'order']
    list_editable = ['published', 'order']
    search_fields = ['title', 'body']

admin.site.site_header = 'Crew Lopez — Website admin'
admin.site.site_title = 'Crew Lopez'
