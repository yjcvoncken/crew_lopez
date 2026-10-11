import tempfile
from io import BytesIO, StringIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from .image_optimization import optimize_image
from .models import VillaPhoto
from .image_widgets import ImageAdminForm


class VillaPhotoForm(ImageAdminForm):
    class Meta:
        model = VillaPhoto
        fields = ['image', 'caption', 'order']


class ImageOptimizationTests(TestCase):
    def test_large_upload_is_resized_without_crop(self):
        output = BytesIO()
        Image.new('RGB', (3000, 1500), 'blue').save(output, 'PNG')
        form = VillaPhotoForm({'caption': '', 'order': 0}, {
            'image': SimpleUploadedFile('large.png', output.getvalue(), 'image/png'),
        })
        self.assertTrue(form.is_valid(), form.errors)
        optimized = form.cleaned_data['image']
        self.assertTrue(optimized.name.endswith('-web.webp'))
        with Image.open(optimized) as image:
            self.assertEqual(image.size, (1920, 960))

    def test_transparency_and_animation_are_preserved(self):
        output = BytesIO()
        Image.new('RGBA', (2100, 100), (255, 0, 0, 0)).save(output, 'PNG')
        optimized = optimize_image(ContentFile(output.getvalue(), name='transparent.png'))
        with Image.open(optimized) as image:
            self.assertEqual(image.convert('RGBA').getpixel((0, 0))[3], 0)
        output = BytesIO()
        frames = [Image.new('RGB', (20, 20), color) for color in ['red', 'blue']]
        frames[0].save(output, 'GIF', save_all=True, append_images=frames[1:], duration=100, loop=0)
        self.assertIsNone(optimize_image(ContentFile(output.getvalue(), name='animated.gif')))
        self.assertIsNone(optimize_image(ContentFile(b'<svg/>', name='art.svg')))

    def test_existing_image_command_keeps_original_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
            output = BytesIO()
            Image.new('RGB', (3000, 1500), 'blue').save(output, 'PNG')
            photo = VillaPhoto.objects.create(image=ContentFile(output.getvalue(), name='old.png'))
            original = photo.image.name
            call_command('optimize_images', stdout=StringIO())
            photo.refresh_from_db()
            self.assertTrue(photo.image.name.endswith('-web.webp'))
            self.assertTrue(photo.image.storage.exists(original))
            optimized = photo.image.name
            call_command('optimize_images', stdout=StringIO())
            photo.refresh_from_db()
            self.assertEqual(photo.image.name, optimized)
