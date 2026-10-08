"""One admin gallery, backed by the original content records."""
from django import forms
from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from .image_widgets import ImageAdminForm, CropImageWidget
from .models import Photos, SiteImage, SiteSettings, Room, Activity


NAMES = {
    'crew-lopez-hero': 'About us image / default homepage hero',
    'crew-lopez-logo': 'Website logo (header and footer)',
    'villa-exterior': 'Villa exterior', 'villa-pool': 'Villa swimming pool',
    'villa-breakfast': 'Breakfast / shared dinner image',
    'villa-yoga': 'Homepage yoga image',
    'graphic-palm': 'Villa and footer palm illustration',
    'graphic-surf-car': 'Welcome and activities illustration',
    'graphic-wave': 'Homepage wave illustration',
    'graphic-sunset': 'Homepage location illustration',
}


def fallback_for(record, field):
    if isinstance(record, SiteImage):
        return record.key
    if isinstance(record, SiteSettings) and field == 'homepage_photo':
        return 'studio/crew-lopez-hero.png'
    if isinstance(record, Activity):
        return 'studio/activities/' + record.slug + '.jpg'
    if isinstance(record, Room):
        position = list(Room.objects.values_list('pk', flat=True)).index(record.pk) + 1
        prefix = 'twin' if position == 1 else 'shared' if position == 2 else 'dorm'
        return 'studio/room-' + prefix + '-illustration.png'


class PhotoGalleryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return any(model_admin.has_change_permission(request) for model, model_admin in self.admin_site._registry.items() if model is not Photos and model._meta.app_label == 'studio')

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return super().has_view_permission(request, obj)
        return self.has_module_permission(request)

    def get_model_perms(self, request):
        return {'view': self.has_module_permission(request)}

    def changelist_view(self, request, extra_context=None):
        items = []
        # Discover file fields on registered content models so future article/team
        # photos use their own records and permission checks too.
        for model, model_admin in self.admin_site._registry.items():
            if model is Photos or model._meta.app_label != 'studio':
                continue
            fields = [field.name for field in model._meta.fields if isinstance(field, models.FileField)]
            if not fields or not model_admin.has_change_permission(request):
                continue
            for record in model_admin.get_queryset(request):
                if not model_admin.has_change_permission(request, record):
                    continue
                for field in fields:
                    token = f'{model._meta.model_name}-{record.pk}-{field}'
                    title = str(record)
                    if isinstance(record, SiteSettings):
                        title = 'Homepage hero' if field == 'homepage_photo' else 'Homepage brand artwork'
                    elif isinstance(record, SiteImage):
                        stem = record.key.rsplit('/', 1)[-1].rsplit('.', 1)[0]
                        title = NAMES.get(stem, record.name + ' (default image)')
                    else:
                        title = f'{model._meta.verbose_name.title()}: {record}'
                    form_class = forms.modelform_factory(model, form=ImageAdminForm, fields=[field])
                    selected = request.method == 'POST' and request.POST.get('photo_target') == token
                    form = form_class(request.POST if selected else None, request.FILES if selected else None, instance=record, auto_id=f'id_{token}_%s')
                    widget = form.fields[field].widget
                    widget.fallback_key = fallback_for(record, field)
                    widget.fixed_ratio = '1.3333333333' if isinstance(record, Room) else '1.5' if isinstance(record, Activity) else 'original'
                    if widget.fallback_key:
                        fallback = SiteImage.objects.filter(key=widget.fallback_key).first()
                        if fallback and fallback.image and not getattr(record, field):
                            widget.fallback_file = fallback.image
                    if selected and form.is_valid():
                        form.save()
                        messages.success(request, f'{title} updated.')
                        return redirect(reverse('admin:studio_siteimage_changelist'))
                    page = '/'
                    selector = ''
                    if isinstance(record, Room):
                        page = '/rooms/'
                        position = list(Room.objects.values_list('pk', flat=True)).index(record.pk) + 1
                        selector = f'#room-{position} .stay-image img'
                    elif isinstance(record, Activity):
                        page = '/activities/'
                    elif isinstance(record, SiteSettings) and field == 'homepage_photo':
                        selector = '.hero > img'
                    elif isinstance(record, SiteImage):
                        if 'activities/' in record.key:
                            page = '/activities/'
                        elif 'room-' in record.key:
                            page = '/rooms/'
                        elif 'villa-exterior' in record.key or 'villa-pool' in record.key:
                            page = '/villa/'
                        elif 'crew-lopez-hero' in record.key:
                            page = '/about/'
                    items.append({'title': title, 'token': token, 'form': form, 'field': form[field], 'page': page, 'selector': selector, 'record_url': reverse(f'admin:studio_{model._meta.model_name}_change', args=[record.pk])})
        if request.method == 'POST' and not any(item['token'] == request.POST.get('photo_target') for item in items):
            raise PermissionDenied
        context = {**self.admin_site.each_context(request), 'title': 'Site images', 'items': items,
                   'media': CropImageWidget().media, 'opts': self.model._meta}
        # Empty forms have no image widgets; collect media from a real form.
        if items:
            context['media'] = items[0]['form'].media
        return TemplateResponse(request, 'admin/studio/photos.html', context)
