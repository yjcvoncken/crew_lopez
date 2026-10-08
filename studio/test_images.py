import json
import tempfile
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.templatetags.static import static
from django.contrib.auth.models import User, Permission
from .image_widgets import ImageAdminForm
from .models import SiteImage


class SiteImageForm(ImageAdminForm):
    class Meta:
        model = SiteImage
        fields = ['name', 'image']


class ImageEditingTests(TestCase):
    def test_initial_image_import_preserves_replacements(self):
        import importlib
        from django.apps import apps
        from django.db import connection
        image = SiteImage.objects.get(key='studio/villa-pool.png')
        image.image = 'site-images/owners-pool.png'
        image.save()
        importlib.import_module('studio.migrations.0007_seed_site_images').seed(apps, connection.schema_editor())
        image.refresh_from_db()
        self.assertEqual(image.image.name, 'site-images/owners-pool.png')

    def test_gallery_updates_original_record_and_respects_permissions(self):
        from .models import Room
        user = User.objects.create_user('photo-editor', password='test', is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='change_room'))
        self.client.force_login(user)
        room = Room.objects.first()
        response = self.client.get('/admin/studio/photos/')
        self.assertContains(response, f'Room: {room.name}')
        self.assertNotContains(response, 'Homepage hero')
        output = BytesIO()
        Image.new('RGB', (400, 300), 'blue').save(output, 'PNG')
        with tempfile.TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
            response = self.client.post('/admin/studio/photos/', {
                'photo_target': f'room-{room.pk}-photo',
                'photo_crop': json.dumps({'x': 0, 'y': 0, 'w': 1, 'h': 1}),
                'photo': SimpleUploadedFile('room.png', output.getvalue(), 'image/png'),
            })
            self.assertEqual(response.status_code, 302)
            room.refresh_from_db()
            self.assertTrue(room.photo)
            self.assertContains(self.client.get('/rooms/'), room.photo.url)
        self.assertEqual(self.client.post('/admin/studio/photos/', {'photo_target': 'sitesettings-1-homepage_photo'}).status_code, 403)

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
