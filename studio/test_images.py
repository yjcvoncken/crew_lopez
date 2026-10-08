import json
import tempfile
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.templatetags.static import static
from .image_widgets import ImageAdminForm
from .models import SiteImage


class SiteImageForm(ImageAdminForm):
    class Meta:
        model = SiteImage
        fields = ['name', 'image']


class ImageEditingTests(TestCase):
    def test_bundled_image_preview_and_crop_without_upload(self):
        image = SiteImage.objects.get(key='studio/villa-breakfast.png')
        form = SiteImageForm(instance=image)
        self.assertIn(static(image.key), str(form['image']))
        with tempfile.TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
            with Image.open('studio/static/studio/villa-breakfast.png') as original:
                width, height = original.size
            form = SiteImageForm({'name': image.name, 'image_crop': json.dumps({'x': 0, 'y': 0, 'w': .5, 'h': .5})}, instance=image)
            self.assertTrue(form.is_valid(), form.errors)
            saved = form.save()
            self.assertTrue(saved.image.name.startswith('site-images/'))
            with Image.open(saved.image) as cropped:
                self.assertEqual(cropped.size, (round(width*.5), round(height*.5)))
            clear = SiteImageForm({'name': image.name, 'image-clear': 'on'}, instance=saved)
            self.assertTrue(clear.is_valid(), clear.errors)
            self.assertFalse(clear.save().image)

    def test_upload_crop_and_recrop_stored_image(self):
        with tempfile.TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
            output = BytesIO()
            Image.new('RGB', (400, 200), 'red').save(output, 'JPEG')
            image = SiteImage.objects.create(name='Test', key='test')
            form = SiteImageForm({'name': 'Test', 'image_crop': json.dumps({'x': .25, 'y': 0, 'w': .5, 'h': 1})},
                                 {'image': SimpleUploadedFile('photo.jpg', output.getvalue(), 'image/jpeg')}, instance=image)
            self.assertTrue(form.is_valid(), form.errors)
            saved = form.save()
            with Image.open(saved.image) as cropped:
                self.assertEqual(cropped.size, (200, 200))
            form = SiteImageForm({'name': 'Test', 'image_crop': json.dumps({'x': 0, 'y': 0, 'w': .5, 'h': 1})}, instance=saved)
            self.assertTrue(form.is_valid(), form.errors)
            with Image.open(form.save().image) as cropped:
                self.assertEqual(cropped.size, (100, 200))

    def test_site_image_override_is_used_on_homepage(self):
        image = SiteImage.objects.get(key='studio/villa-breakfast.png')
        image.image = 'site-images/replacement.png'
        image.save()
        response = self.client.get('/')
        self.assertContains(response, '/media/site-images/replacement.png')
