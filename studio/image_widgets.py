import json
from io import BytesIO

from django import forms
from django.core.files.base import ContentFile
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.utils.html import format_html


class CropImageWidget(forms.ClearableFileInput):
    fallback_key = None
    class Media:
        js = ('studio/admin-images.js',)
        css = {'all': ('studio/admin-images.css',)}

    def render(self, name, value, attrs=None, renderer=None):
        field = super().render(name, value, attrs, renderer)
        url = value.url if value and hasattr(value, 'url') else (static(self.fallback_key) if self.fallback_key else '')
        return format_html(
            '<div class="image-editor" data-preview="{}">{}'
            '<input type="hidden" name="{}_crop" class="crop-data">'
            '<div class="crop-controls"><p>Drag the existing picture to crop it, or choose a file to replace it. Zoom to cut tighter. '
            'The frame stays the same size on the website. Cropping is applied when you save.</p>'
            '<img class="crop-preview" alt="Image crop preview" draggable="false">'
            '<label>Zoom <input class="crop-zoom" type="range" min="1" max="4" step="0.01" value="1"></label>'
            '<label>Frame <select class="crop-ratio"><option value="original">Original proportions</option><option value="1.5">Landscape (3:2)</option>'
            '<option value="1.7777778">Wide (16:9)</option><option value="1">Square</option>'
            '<option value="0.75">Portrait (3:4)</option></select></label>'
            '<button type="button" class="crop-reset">Reset crop</button>'
            '<p class="crop-status" aria-live="polite"></p></div></div>', url, field, name)


class ImageAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, forms.FileField):
                field.widget = CropImageWidget()
                if name == 'image' and hasattr(self.instance, 'key'):
                    field.widget.fallback_key = self.instance.key

    def clean(self):
        cleaned = super().clean()
        from PIL import Image, ImageOps, UnidentifiedImageError
        for name, field in self.fields.items():
            if not isinstance(field, forms.FileField):
                continue
            value = cleaned.get(name)
            crop = self.data.get(name + '_crop')
            if value is False or not crop:
                continue
            fallback = False
            try:
                if not value and field.widget.fallback_key:
                    path = finders.find(field.widget.fallback_key)
                    if not path:
                        raise ValueError('Original image unavailable')
                    with open(path, 'rb') as source:
                        value = ContentFile(source.read(), name=field.widget.fallback_key)
                    fallback = True
                if not value:
                    continue
                coords = json.loads(crop)
                value.open('rb')
                with Image.open(value) as original:
                    image = ImageOps.exif_transpose(original)
                    width, height = image.size
                    x, y, w, h = [float(coords[key]) for key in ('x', 'y', 'w', 'h')]
                    if not (0 <= x < 1 and 0 <= y < 1 and w > 0 and h > 0 and x+w <= 1.001 and y+h <= 1.001):
                        raise ValueError('Invalid crop')
                    image = image.crop((round(x*width), round(y*height), round((x+w)*width), round((y+h)*height)))
                    image.thumbnail((2400, 2400))
                    output = BytesIO()
                    image.save(output, format='PNG')
                cleaned[name] = ContentFile(output.getvalue(), name=value.name.rsplit('/', 1)[-1].rsplit('.', 1)[0] + '-crop.png')
            except (ValueError, KeyError, TypeError, OSError, UnidentifiedImageError, Image.DecompressionBombError):
                self.add_error(name, 'Could not crop this image. Choose a PNG, JPG or WebP photo and try again.')
            finally:
                if fallback:
                    value.close()
                elif hasattr(value, 'seek'):
                    value.seek(0)
        return cleaned
