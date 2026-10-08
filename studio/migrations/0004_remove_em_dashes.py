from django.db import migrations, models


def clean_content(apps, schema_editor):
    for name in ('SiteSettings', 'Room', 'Activity', 'BlogPost'):
        model = apps.get_model('studio', name)
        fields = [field.name for field in model._meta.fields
                  if isinstance(field, (models.CharField, models.TextField))]
        for record in model.objects.using(schema_editor.connection.alias).all().iterator():
            changed = []
            for field in fields:
                value = getattr(record, field)
                if isinstance(value, str) and '\u2014' in value:
                    setattr(record, field, value.replace(' \u2014 ', ' - ').replace('\u2014', ', '))
                    changed.append(field)
            if changed:
                record.save(using=schema_editor.connection.alias, update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [('studio', '0003_owner_confirmed_content')]
    operations = [migrations.RunPython(clean_content, migrations.RunPython.noop)]
