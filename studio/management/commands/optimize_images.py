"""Optimize stored photos, retaining the original objects for recovery."""
import logging
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models
from studio.image_optimization import optimize_image

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Compress existing uploaded images. Old files are retained; reruns skip optimized files.'

    def handle(self, *args, **options):
        updated = 0
        failed = 0
        for model in apps.get_app_config('studio').get_models():
            if model._meta.proxy:
                continue
            for field in model._meta.fields:
                if not isinstance(field, models.FileField):
                    continue
                for record in model.objects.exclude(**{field.name: ''}).iterator():
                    photo = getattr(record, field.name)
                    if photo.name.endswith('-web.webp'):
                        continue
                    original_name = photo.name
                    try:
                        optimized = optimize_image(photo)
                        if optimized:
                            photo.save(optimized.name, optimized, save=False)
                            # Don't overwrite an owner edit made during conversion.
                            changed = model.objects.filter(pk=record.pk, **{field.name: original_name}).update(**{field.name: photo.name})
                            updated += changed
                    except Exception:
                        failed += 1
                        logger.exception('Image optimization failed for %s %s %s', model._meta.label, record.pk, field.name)
                    finally:
                        photo.close()
        self.stdout.write(f'Optimized {updated} images; {failed} failed. Original files retained.')
        if failed:
            self.stderr.write('Failed photos were left unchanged. Check logs and storage credentials, then retry.')
