from io import StringIO
from unittest.mock import patch
from django.core.management import call_command, CommandError
from django.test import TestCase
from .models import Room


class ImageStorageAuditTests(TestCase):
    def setUp(self):
        self.room = Room.objects.first()
        self.room.photo = 'rooms/saved.webp'
        self.room.save()

    def test_missing_file_is_reported_without_changing_reference(self):
        output = StringIO()
        with patch.object(self.room.photo.storage, 'exists', return_value=False):
            with self.assertRaises(CommandError):
                call_command('check_image_storage', stdout=output)
        self.assertIn('MISSING: Room #', output.getvalue())
        self.room.refresh_from_db()
        self.assertEqual(self.room.photo.name, 'rooms/saved.webp')

    def test_storage_error_is_distinct_and_does_not_expose_error_details(self):
        output = StringIO()
        with patch.object(self.room.photo.storage, 'exists', side_effect=OSError('secret-provider-details')):
            with self.assertRaises(CommandError):
                call_command('check_image_storage', stdout=output)
        self.assertIn('UNREADABLE: Room #', output.getvalue())
        self.assertNotIn('secret-provider-details', output.getvalue())
