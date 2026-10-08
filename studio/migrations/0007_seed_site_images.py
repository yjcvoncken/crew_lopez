from django.db import migrations


def seed(apps, schema_editor):
    model = apps.get_model("studio", "SiteImage")
    for key, name in [('studio/activities/four-by-four.jpg', 'Four By Four'), ('studio/activities/hikes.jpg', 'Hikes'), ('studio/activities/kite.jpg', 'Kite'), ('studio/activities/skate.jpg', 'Skate'), ('studio/activities/snorkeling.jpg', 'Snorkeling'), ('studio/activities/stargazing.jpg', 'Stargazing'), ('studio/activities/surf.jpg', 'Surf'), ('studio/activities/surfskate.jpg', 'Surfskate'), ('studio/crew-lopez-hero.png', 'Crew Lopez Hero'), ('studio/crew-lopez-logo.png', 'Crew Lopez Logo'), ('studio/graphic-palm.png', 'Graphic Palm'), ('studio/graphic-sunset.png', 'Graphic Sunset'), ('studio/graphic-surf-car.png', 'Graphic Surf Car'), ('studio/graphic-wave.png', 'Graphic Wave'), ('studio/room-dorm-illustration.png', 'Room Dorm Illustration'), ('studio/room-shared-illustration.png', 'Room Shared Illustration'), ('studio/room-twin-illustration.png', 'Room Twin Illustration'), ('studio/villa-breakfast.png', 'Villa Breakfast'), ('studio/villa-exterior.png', 'Villa Exterior'), ('studio/villa-pool.png', 'Villa Pool'), ('studio/villa-yoga.png', 'Villa Yoga')]:
        model.objects.using(schema_editor.connection.alias).get_or_create(key=key, defaults={"name": name})


class Migration(migrations.Migration):
    dependencies = [("studio", "0006_siteimage")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
