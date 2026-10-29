"""Read-only audit of image references and their configured storage."""
from django.apps import apps
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db.models import FileField


class Command(BaseCommand):
    help = 'Check saved image references for missing or unreadable files (does not modify storage).'

    def handle(self, *args, **options):
        self.stdout.write(f'Storage backend: {default_storage.__class__.__name__}')
        checked = missing = inaccessible = 0
        for model in apps.get_app_config('studio').get_models():
            if model._meta.proxy:
                continue
            for field in model._meta.fields:
                if not isinstance(field, FileField):
                    continue
                for record in model.objects.exclude(**{field.name: ''}).iterator():
                    image = getattr(record, field.name)
                    if not image:
                        continue
                    checked += 1
                    label = f'{model.__name__} #{record.pk} / {field.name}'
                    try:
                        if not image.storage.exists(image.name):
                            missing += 1
                            self.stdout.write(f'MISSING: {label}')
                            continue
                        with image.storage.open(image.name, 'rb') as stream:
                            if not stream.read(1):
                                missing += 1
                                self.stdout.write(f'EMPTY: {label}')
                    except Exception as error:
                        # Never print signed URLs, credentials or raw provider responses.
                        inaccessible += 1
                        self.stdout.write(f'UNREADABLE: {label} ({type(error).__name__})')
        self.stdout.write(f'Checked {checked} saved image references; {missing} missing/empty; {inaccessible} unreadable.')
        if missing or inaccessible:
            raise CommandError('Image storage check failed. No records or files were changed.')
        if not checked:
            self.stdout.write(self.style.WARNING('No uploaded images are recorded in this database. Check that this is the intended environment.'))
        else:
            self.stdout.write(self.style.SUCCESS('All saved images exist and can be read by the application. Browser delivery must be checked separately.'))
